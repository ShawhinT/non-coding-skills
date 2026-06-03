"""Transcribe a video file using AssemblyAI and write word-level timestamps to JSON."""

import json
import os
import subprocess
import sys
from pathlib import Path

import assemblyai as aai
from dotenv import load_dotenv

VIDEO_EXTS = {".mp4", ".mov", ".mkv", ".m4v", ".avi", ".webm", ".mts", ".m2ts"}


def find_project_root(start: str) -> str:
    """Walk up from start to find the project root (contains .git or .claude)."""
    current = Path(start).resolve()
    if current.is_file():
        current = current.parent
    while current != current.parent:
        if (current / ".git").exists() or (current / ".claude").exists():
            return str(current)
        current = current.parent
    return str(Path(start).resolve().parent)


def extract_audio(video_path: str, output_dir: str) -> str:
    """Extract audio from a video file to MP3 in output_dir. Returns the mp3 path.

    Uploading raw video to AssemblyAI is slow and 500s on large files. The MP3
    is sample-accurate against the source video, so downstream word timestamps
    still align with the original timeline.
    """
    stem = Path(video_path).stem
    audio_path = os.path.join(output_dir, f"{stem}.mp3")
    os.makedirs(output_dir, exist_ok=True)
    print(f"Extracting audio: {video_path} -> {audio_path}")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", video_path,
         "-vn", "-acodec", "libmp3lame", "-b:a", "128k", audio_path],
        check=True,
    )
    return audio_path


def transcribe(video_path: str, output_dir: str) -> str:
    """Transcribe video and write <stem>_transcript.json to output_dir. Returns output path."""
    load_dotenv(Path(__file__).parent.parent / ".env")
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    upload_path = video_path
    if Path(video_path).suffix.lower() in VIDEO_EXTS:
        upload_path = extract_audio(video_path, output_dir)

    print(f"Transcribing: {upload_path}")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        upload_path,
        aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"],
            disfluencies=True,
        ),
    )

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    words = [
        {"word": w.text, "start": w.start / 1000, "end": w.end / 1000}
        for w in transcript.words
    ]

    os.makedirs(output_dir, exist_ok=True)
    stem = Path(video_path).stem  # always name after source video, not the intermediate mp3
    out_path = os.path.join(output_dir, f"{stem}_transcript.json")
    with open(out_path, "w") as f:
        json.dump({"words": words}, f, indent=2)

    print(f"Transcript saved to {out_path} ({len(words)} words)")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/transcribe.py <video_path> [--output-dir <dir>]")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            i += 1

    if output_dir is None:
        root = find_project_root(os.path.abspath(video_path))
        output_dir = os.path.join(root, "claude-edits")

    transcribe(video_path, output_dir)
