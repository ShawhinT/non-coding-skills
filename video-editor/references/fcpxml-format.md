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
