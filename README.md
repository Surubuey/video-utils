# Video Utils

A collection of utilities to manage video files using Python and ffmpeg.

## Features

- **Concatenate MP4 files**: Merge all MP4 files in a folder into a single video file

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

### Options

- `--output`: Specify output filename (default: output/[INPUT_FOLDER_NAME].mp4)
- `--sort`: Sort method (alphabetical, date_created, date_modified)

## Examples

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

## Testing

To test the functionality, you can create sample videos:

```bash
python create_test_videos.py
```

This will create three test videos in a `test_videos` folder and automatically run the concatenation script to demonstrate the functionality.

## Notes

- The script uses ffmpeg's concat demuxer for fast concatenation without re-encoding
- All videos should have the same codec, resolution, and frame rate for best results
- The script will automatically sort files alphabetically by default
- File paths with spaces and special characters are properly handled
