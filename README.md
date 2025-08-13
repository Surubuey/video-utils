# Video Utils

A collection of utilities to manage video files using Python and ffmpeg.

## Features

- **Concatenate MP4 files**: Merge all MP4 files in a folder into a single video file
- **Image Overlay**: Add logos, watermarks, or images onto videos with flexible positioning and timing

## Requirements

- Python 3.7+
- ffmpeg (must be installed and available in system PATH)

## Installation

1. Clone or download this repository
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Concatenate MP4 Files

#### Python Script (Recommended)
```bash
python concatenate_videos.py /path/to/folder/with/mp4/files
```

#### Windows Batch Script (Alternative)
```cmd
concatenate.bat "C:\Videos\ToMerge"
```

This will:
- Find all .mp4 files in the specified folder
- Sort them alphabetically by default
- Concatenate them into a single video file named `[INPUT_FOLDER_NAME].mp4` in the `output/` folder

### Image Overlay

#### Python Script (Recommended)
```bash
python overlay_image.py video.mp4 logo.png
```

#### Windows Batch Script (Alternative)
```cmd
overlay.bat "video.mp4" "logo.png"
```

This will:
- Overlay the image onto the video
- Default position is top-right corner
- Output saved as `[VIDEO_NAME]_overlay.[ext]` in the `output/` folder

### Options

#### Concatenation
- `--output`: Specify output filename (default: output/[INPUT_FOLDER_NAME].mp4)
- `--sort`: Sort method (alphabetical, date_created, date_modified)

#### Image Overlay
- `--output`: Output filename (default: output/[VIDEO_NAME]_overlay.[ext])
- `--position`: Position of overlay (top-left, top-right, bottom-left, bottom-right, center, custom)
- `--scale`: Scale overlay image (e.g., "100:100", "50%", "iw*0.5:ih*0.5")
- `--opacity`: Opacity of overlay (0.0 to 1.0)
- `--offset-x/y`: Position offsets for fine-tuning
- `--start-time`: Start time for overlay (HH:MM:SS)
- `--duration`: Duration of overlay (HH:MM:SS)

## Examples

### Video Concatenation
```bash
# Basic concatenation (output will be output/ToMerge.mp4)
python concatenate_videos.py "C:\Videos\ToMerge"

# Custom output name
python concatenate_videos.py "C:\Videos\ToMerge" --output "output/my_merged_video.mp4"

# Sort by creation date (output will be output/ToMerge.mp4)
python concatenate_videos.py "C:\Videos\ToMerge" --sort date_created

# Windows batch script examples
concatenate.bat "C:\Videos\ToMerge"
concatenate.bat "C:\Videos\ToMerge" "output/custom_name.mp4"
```

### Image Overlay
```bash
# Basic overlay (top-right corner)
python overlay_image.py video.mp4 logo.png

# Custom position and transparency
python overlay_image.py video.mp4 watermark.png --position center --opacity 0.7

# Scaled overlay in bottom-left
python overlay_image.py video.mp4 logo.png --position bottom-left --scale 50%

# Timed overlay (start at 10s, show for 30s)
python overlay_image.py video.mp4 logo.png --start-time 00:00:10 --duration 00:00:30

# Custom positioning with pixel offsets
python overlay_image.py video.mp4 logo.png --position custom --offset-x 100 --offset-y 50

# Windows batch script examples
overlay.bat "video.mp4" "logo.png"
overlay.bat "video.mp4" "watermark.png" "branded_video.mp4" "center"
```

## Testing

To test the functionality, you can create sample videos and images:

```bash
# Create test videos
python create_test_videos.py

# Create test images for overlay
python create_test_images.py

# Test concatenation
python concatenate_videos.py test_videos

# Test overlay
python overlay_image.py "output/test_videos.mp4" "test_images/logo.png"
```

This will create test videos and images, then demonstrate both concatenation and overlay functionality.

## Notes

- The script uses ffmpeg's concat demuxer for fast concatenation without re-encoding
- All videos should have the same codec, resolution, and frame rate for best results
- The script will automatically sort files alphabetically by default
- File paths with spaces and special characters are properly handled
