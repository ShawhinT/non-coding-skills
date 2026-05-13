"""
Render an HTML animation file to a YouTube-ready MP4.

Frame-accurate: pauses all CSS animations and seeks each one to the target
time before screenshotting each frame.

CRITICAL: Do NOT pass animations="disabled" to page.screenshot(). That option
treats animations as not started and overrides the manual currentTime seek,
which freezes every frame at the initial state. Don't add it back.

Usage (run from the skill folder so it uses the skill's own venv):
  uv run --project ~/.claude/skills/animation-builder \
    ~/.claude/skills/animation-builder/scripts/render.py /abs/path/to/animation.html

  # Or alias the long invocation in the shell, e.g.:
  #   alias animrender='uv run --project ~/.claude/skills/animation-builder \
  #     ~/.claude/skills/animation-builder/scripts/render.py'
  # then: animrender /abs/path/to/animation.html --duration 5 --out clip.mp4

Defaults:
  duration = 3.6s (one canonical loop)
  fps      = 30
  output   = <input>.mp4 next to the input HTML (override with --out)
  size     = 1920x1080

Output goes next to the input HTML by default, NOT into the skill folder.
Use absolute paths or paths relative to your shell's cwd.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

from playwright.sync_api import sync_playwright

WIDTH, HEIGHT = 1920, 1080

# Filesystems where screenshot writes are slow to surface to ffmpeg. We stage
# frames in /tmp/ for these and move the final MP4 to its requested --out at
# the end. (Spotted on Google Drive CloudStorage; iCloud Drive likely similar.)
CLOUD_PREFIXES = (
    str(Path.home() / "Library" / "CloudStorage"),
    str(Path.home() / "Library" / "Mobile Documents"),  # iCloud Drive
)


def _is_cloud_path(path: Path) -> bool:
    p = str(path.resolve())
    return any(p.startswith(prefix) for prefix in CLOUD_PREFIXES)


def render(html_path: Path, duration: float, fps: int, out_path: Path) -> None:
    # Per-invocation UUID-suffixed frames dir. Two parallel renders of sibling
    # HTMLs would otherwise share `.frames/` and overwrite each other's PNGs,
    # producing Frankenstein MP4s. Don't drop the suffix.
    suffix = uuid.uuid4().hex[:8]

    if _is_cloud_path(html_path):
        # Stage in /tmp/ to dodge CloudStorage's filesystem virtualization
        # (screenshots can lag behind their write call by seconds on Drive).
        frames_dir = Path(tempfile.gettempdir()) / f"animbuilder-{suffix}"
    else:
        frames_dir = html_path.parent / f".frames-{suffix}"

    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)

    total_frames = int(round(duration * fps))
    frame_ms = 1000.0 / fps

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": WIDTH, "height": HEIGHT})
        page = context.new_page()
        page.goto(html_path.resolve().as_uri())

        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.evaluate("""() => {
            for (const a of document.getAnimations()) a.pause();
        }""")

        for i in range(total_frames):
            t = i * frame_ms
            page.evaluate(
                "(t) => { for (const a of document.getAnimations()) a.currentTime = t; }",
                t,
            )
            # NB: no animations="disabled" — that flag would override the seek.
            page.screenshot(path=str(frames_dir / f"frame_{i:05d}.png"))
            if (i + 1) % 30 == 0 or i == total_frames - 1:
                print(f"  frame {i + 1}/{total_frames}")

        browser.close()

    print(f"\nEncoding {out_path.name} with ffmpeg...")

    # When staging in /tmp/ (CloudStorage paths), encode to a local MP4 first,
    # then move it to the requested out_path. Avoids the same Drive sync lag
    # for the final encoded file.
    encode_target = (
        frames_dir.parent / f"{frames_dir.name}.mp4"
        if frames_dir.parent == Path(tempfile.gettempdir())
        else out_path
    )

    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", str(frames_dir / "frame_%05d.png"),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-r", str(fps),
        str(encode_target),
    ]
    subprocess.run(cmd, check=True)

    if encode_target != out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(encode_target), str(out_path))

    shutil.rmtree(frames_dir, ignore_errors=True)
    print(f"\nDone: {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="Path to HTML animation file")
    ap.add_argument("--duration", type=float, default=3.6, help="Seconds (default 3.6)")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    html_path = Path(args.html)
    if not html_path.exists():
        sys.exit(f"Not found: {html_path}")

    out = Path(args.out) if args.out else html_path.with_suffix(".mp4")
    render(html_path, args.duration, args.fps, out)


if __name__ == "__main__":
    main()
