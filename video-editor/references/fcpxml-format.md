# FCPXML Format Reference

FCPXML v1.11 (Final Cut Pro 10.6+) structure reference for generating timeline edits.

## Document Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE fcpxml>
<fcpxml version="1.11">
    <resources>
        <format id="r1" name="FFVideoFormat..." width="W" height="H" frameDuration="1001/30000s"/>
        <asset id="r2" name="clip_name" start="0s" duration="Ds" hasVideo="1" hasAudio="1">
            <media-rep kind="original-media" src="file:///path/to/video.mov"/>
        </asset>
    </resources>
    <library>
        <event name="Edit">
            <project name="ProjectName">
                <sequence format="r1" duration="Ds" tcStart="0s" tcFormat="NDF">
                    <spine>
                        <!-- clips go here -->
                    </spine>
                </sequence>
            </project>
        </event>
    </library>
</fcpxml>
```

## Rational Time Format

FCPXML uses rational numbers for time values: `numerator/denominator s`

Common framerates:
- **29.97fps (NTSC):** frameDuration = `1001/30000s`, times in 1001/30000 units
- **30fps:** frameDuration = `100/3000s`
- **23.976fps:** frameDuration = `1001/24000s`
- **24fps:** frameDuration = `100/2400s`
- **25fps (PAL):** frameDuration = `100/2500s`
- **59.94fps:** frameDuration = `1001/60000s`
- **60fps:** frameDuration = `100/6000s`

Converting seconds to rational time:
```python
from fractions import Fraction

def seconds_to_rational(seconds, fps_num, fps_den):
    """Convert seconds to FCPXML rational time string.

    For 29.97fps: fps_num=30000, fps_den=1001
    For 30fps: fps_num=3000, fps_den=100
    """
    frame_duration = Fraction(fps_den, fps_num)
    total_frames = round(Fraction(seconds) / frame_duration)
    rational = total_frames * frame_duration
    return f"{rational.numerator}/{rational.denominator}s"
```

## Clip Element

```xml
<clip name="Segment 1" offset="timeline_pos" duration="clip_dur" start="source_start" tcFormat="NDF">
    <asset-clip ref="r2" offset="timeline_pos" name="clip_name" duration="clip_dur" start="source_start" tcFormat="NDF">
        <adjust-volume amount="3dB"/>
    </asset-clip>
</clip>
```

Key attributes:
- `offset`: Position on the timeline (where this clip starts in the output)
- `start`: Position in the source media (in-point)
- `duration`: Length of the clip
- `ref`: References an `<asset>` in `<resources>`

## Volume Adjustment

```xml
<adjust-volume amount="-3dB"/>
```
- Positive values = louder, negative = quieter
- Applied inside `<asset-clip>` or `<clip>`

## Format IDs

The `<format>` element defines the sequence format. Common values:

| Resolution | Framerate | Format Name |
|-----------|-----------|-------------|
| 1920x1080 | 29.97fps | FFVideoFormat1080p2997 |
| 1920x1080 | 30fps | FFVideoFormat1080p30 |
| 1920x1080 | 24fps | FFVideoFormat1080p24 |
| 3840x2160 | 29.97fps | FFVideoFormat2160p2997 |
| 3840x2160 | 30fps | FFVideoFormat2160p30 |

## Simplified Clip Approach

For basic cuts (no transitions), use `<asset-clip>` directly in the spine:

```xml
<spine>
    <asset-clip ref="r2" offset="0s" name="Segment 1" duration="10010/30000s" start="5005/30000s" tcFormat="NDF"/>
    <asset-clip ref="r2" offset="10010/30000s" name="Segment 2" duration="20020/30000s" start="30030/30000s" tcFormat="NDF"/>
</spine>
```

Each `<asset-clip>`:
- `ref` points to the source asset
- `offset` is cumulative position on timeline
- `start` is where to begin in the source
- `duration` is how long the segment plays

## Important Notes
- All time values MUST use rational format matching the source framerate
- `tcFormat="NDF"` for non-drop-frame (most common)
- `tcFormat="DF"` for drop-frame (29.97fps broadcast)
- File paths must be absolute `file:///` URLs
- Asset media location is specified via `<media-rep>` children (not `src` attribute on `<asset>`)

## Connected Clips and Lanes (Overlays / B-Roll)

The spine is the primary storyline. Anything on `lane="1"` (or higher) sits visually above the spine; negative lanes sit below. These are called **connected clips** and they cannot be direct children of `<spine>` — they must be nested **inside the primary spine clip they anchor to**. FCP renders them at the host clip's timeline position, but their `offset` attribute is expressed in the host's *source-time* coordinate system, not absolute timeline time:

```
overlay.offset = host.start + (target_timeline_pos - host.offset)
```

Example: a 1080p overlay attached to a 4K spine clip:

```xml
<asset-clip ref="r2" offset="0s" name="Segment 5"
            start="3185182/30000s" duration="116116/30000s" format="r1">
    <asset-clip ref="r10" lane="1"
                offset="3215182/30000s"   <!-- host.start + 30000/30000 (1s in) -->
                name="overlay" start="0s"
                duration="150150/30000s" format="r4"/>
    <audio-channel-source srcCh="1, 2" role="dialogue.dialogue-1"/>
</asset-clip>
```

If a connected clip is placed as a top-level sibling of `<spine>` with an absolute timeline offset, FCP silently ignores it — the import succeeds but the clip never appears on the timeline.

## DTD Content Order Inside `<asset-clip>`

Children of `<asset-clip>` must appear in this order (any block may be empty):

1. `note?`
2. `(conform-rate?, timeMap?)`
3. Adjustments: `object-tracker*, adjust-crop?, adjust-corners?, adjust-conform?, adjust-transform?, adjust-blend?, adjust-stabilization?, adjust-rollingShutter?, adjust-360-transform?, adjust-reorient?, adjust-orientation?, adjust-cinematic?, adjust-colorConform?, adjust-stereo-3D?, adjust-volume?, adjust-panner?`
4. **Storyline children:** `(audio | video | clip | title | caption | mc-clip | ref-clip | sync-clip | asset-clip)*`
5. **Trailing content:** `audio-channel-source*, filter-video*, filter-audio*, metadata?, marker*`

A connected `<asset-clip>` is a storyline child (group 4), and `<audio-channel-source>` is in group 5. When inserting an overlay into a host that already has `<audio-channel-source>` children, insert the overlay **before** the first audio-channel-source — appending to the end places it in group 5 territory and FCP rejects the import:

> *DTD validation failed. Element asset-clip content does not follow the DTD, expecting (note?, (conform-rate?, timeMap?), ((object-tracker?, adjust-crop?, …, adjust-panner?), (audio | video | clip | title | caption | mc-clip | ref-clip | sync-clip | asset-clip…)**

That error message means a child element is out of order, not malformed.

## Mixed Formats In One Project

When overlay assets don't match the spine's resolution or framerate (e.g., 1920×1080@30 overlays on a 3840×2160@29.97 spine), declare a separate `<format>` resource and have the overlay assets and clips reference it:

```xml
<format id="r1" name="FFVideoFormat2160p2997" frameDuration="1001/30000s"
        width="3840" height="2160"/>
<format id="r4" name="FFVideoFormat1080p30" frameDuration="100/3000s"
        width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>

<asset id="r10" name="overlay" format="r4"
       hasVideo="1" videoSources="1" hasAudio="0"
       start="0s" duration="500/100s">
    <media-rep kind="original-media" src="file:///abs/path/overlay.mp4"/>
</asset>
```

The overlay asset's own `duration` can use its native frame grid (e.g., `100/3000s` units for 30 fps). The **timeline-side** `offset` and `duration` on the connected `<asset-clip>` should still align to the sequence's frame grid — FCP conforms the overlay to the timeline's framerate. If the spine and overlays share the same format, no extra `<format>` is needed.

## Project / Event Naming on Export

`<event name="...">` and `<project name="...">` become the labels in Final Cut when the XML is imported. They default to the source media stem in generated FCPXMLs, which is rarely the intended project name. When emitting (or rewriting) an FCPXML, set both to the desired FCP project name — typically matching the output file's stem.
