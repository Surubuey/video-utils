#!/usr/bin/env python3
"""
Image Overlay Utility

This script overlays an image (like a logo or watermark) onto a video file
using ffmpeg with various positioning and scaling options.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Tuple


def check_ffmpeg() -> bool:
    """
    Check if ffmpeg is available in the system PATH.
    
    Returns:
        True if ffmpeg is available, False otherwise
    """
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def validate_files(video_path: str, image_path: str) -> Tuple[Path, Path]:
    """
    Validate that input video and image files exist.
    
    Args:
        video_path: Path to the input video file
        image_path: Path to the overlay image file
    
    Returns:
        Tuple of validated Path objects for video and image
    
    Raises:
        FileNotFoundError: If either file doesn't exist
        ValueError: If files have invalid extensions
    """
    video_file = Path(video_path)
    image_file = Path(image_path)
    
    # Check if files exist
    if not video_file.exists():
        raise FileNotFoundError(f"Video file does not exist: {video_path}")
    
    if not image_file.exists():
        raise FileNotFoundError(f"Image file does not exist: {image_path}")
    
    # Check video file extension
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.m4v'}
    if video_file.suffix.lower() not in video_extensions:
        raise ValueError(f"Unsupported video format: {video_file.suffix}")
    
    # Check image file extension
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
    if image_file.suffix.lower() not in image_extensions:
        raise ValueError(f"Unsupported image format: {image_file.suffix}")
    
    return video_file, image_file


def get_position_filter(position: str, offset_x: int = 10, offset_y: int = 10) -> str:
    """
    Generate the position filter string for ffmpeg overlay.
    
    Args:
        position: Position preset (top-left, top-right, bottom-left, bottom-right, center, custom)
        offset_x: X offset from the edge (for edge positions) or absolute X position (for custom)
        offset_y: Y offset from the edge (for edge positions) or absolute Y position (for custom)
    
    Returns:
        Position filter string for ffmpeg
    """
    position_map = {
        'top-left': f'{offset_x}:{offset_y}',
        'top-right': f'main_w-overlay_w-{offset_x}:{offset_y}',
        'bottom-left': f'{offset_x}:main_h-overlay_h-{offset_y}',
        'bottom-right': f'main_w-overlay_w-{offset_x}:main_h-overlay_h-{offset_y}',
        'center': '(main_w-overlay_w)/2:(main_h-overlay_h)/2',
        'custom': f'{offset_x}:{offset_y}'
    }
    
    return position_map.get(position, position_map['top-right'])


def overlay_image_on_video(
    video_file: Path, 
    image_file: Path, 
    output_path: str,
    position: str = 'top-right',
    scale: Optional[str] = None,
    opacity: float = 1.0,
    offset_x: int = 10,
    offset_y: int = 10,
    start_time: Optional[str] = None,
    duration: Optional[str] = None
) -> bool:
    """
    Overlay an image onto a video using ffmpeg.
    
    Args:
        video_file: Path to the input video file
        image_file: Path to the overlay image file
        output_path: Path for the output video file
        position: Where to place the overlay (top-left, top-right, bottom-left, bottom-right, center, custom)
        scale: Scale the image (e.g., '100:100', '50%', 'iw*0.5:ih*0.5')
        opacity: Opacity of the overlay (0.0 to 1.0)
        offset_x: X offset from edge or absolute X position for custom
        offset_y: Y offset from edge or absolute Y position for custom
        start_time: Start time for overlay (e.g., '00:00:10')
        duration: Duration of overlay (e.g., '00:00:30')
    
    Returns:
        True if successful, False otherwise
    """
    print(f"Overlaying image: {image_file.name}")
    print(f"On video: {video_file.name}")
    print(f"Position: {position}")
    print(f"Output: {output_path}")
    
    # Build the filter complex
    filter_parts = []
    
    # Scale the overlay image if specified
    if scale:
        if scale.endswith('%'):
            # Handle percentage scaling
            scale_factor = float(scale[:-1]) / 100
            scale_filter = f"scale=iw*{scale_factor}:ih*{scale_factor}"
        else:
            # Handle explicit dimensions
            scale_filter = f"scale={scale}"
        filter_parts.append(f"[1:v]{scale_filter}[scaled]")
        overlay_input = "[scaled]"
    else:
        overlay_input = "[1:v]"
    
    # Set opacity if not fully opaque
    if opacity < 1.0:
        if scale:
            filter_parts.append(f"[scaled]format=rgba,colorchannelmixer=aa={opacity}[transparent]")
            overlay_input = "[transparent]"
        else:
            filter_parts.append(f"[1:v]format=rgba,colorchannelmixer=aa={opacity}[transparent]")
            overlay_input = "[transparent]"
    
    # Get position
    position_filter = get_position_filter(position, offset_x, offset_y)
    
    # Add time constraints if specified
    overlay_options = []
    if start_time:
        # Convert time to seconds for enable option
        overlay_options.append(f"enable='gte(t,{parse_time_to_seconds(start_time)})'")
    
    if duration and start_time:
        end_time = parse_time_to_seconds(start_time) + parse_time_to_seconds(duration)
        overlay_options.append(f"enable='between(t,{parse_time_to_seconds(start_time)},{end_time})'")
    
    # Build overlay filter
    overlay_filter = f"[0:v]{overlay_input}overlay={position_filter}"
    if overlay_options:
        overlay_filter += ":" + ":".join(overlay_options)
    
    filter_parts.append(overlay_filter)
    
    # Combine all filters
    filter_complex = ";".join(filter_parts)
    
    # Build ffmpeg command
    cmd = [
        'ffmpeg',
        '-i', str(video_file),
        '-i', str(image_file),
        '-filter_complex', filter_complex,
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-y',  # Overwrite output file if it exists
        output_path
    ]
    
    print(f"\nRunning ffmpeg overlay...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"\n✅ Successfully created video with overlay: {output_path}")
            return True
        else:
            print(f"\n❌ Error during overlay:")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error during overlay: {str(e)}")
        return False


def parse_time_to_seconds(time_str: str) -> float:
    """
    Parse time string (HH:MM:SS or MM:SS or SS) to seconds.
    
    Args:
        time_str: Time string in various formats
    
    Returns:
        Time in seconds as float
    """
    parts = time_str.split(':')
    if len(parts) == 3:  # HH:MM:SS
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:  # MM:SS
        return float(parts[0]) * 60 + float(parts[1])
    else:  # SS
        return float(parts[0])


def main():
    """Main function to handle command line arguments and execute overlay."""
    parser = argparse.ArgumentParser(
        description="Overlay an image (watermark/logo) onto a video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic overlay (top-right corner)
  python overlay_image.py video.mp4 logo.png
  
  # Custom position and scale
  python overlay_image.py video.mp4 logo.png --position bottom-left --scale 150:100
  
  # Semi-transparent overlay
  python overlay_image.py video.mp4 watermark.png --opacity 0.7 --position center
  
  # Timed overlay (start at 10s, show for 30s)
  python overlay_image.py video.mp4 logo.png --start-time 00:00:10 --duration 00:00:30
  
  # Custom positioning with offsets
  python overlay_image.py video.mp4 logo.png --position custom --offset-x 100 --offset-y 50
        """
    )
    
    parser.add_argument(
        'video',
        help='Path to input video file'
    )
    
    parser.add_argument(
        'image',
        help='Path to overlay image file (PNG, JPG, etc.)'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Output video filename (default: output/[VIDEO_NAME]_overlay.[ext])'
    )
    
    parser.add_argument(
        '--position', '-p',
        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center', 'custom'],
        default='top-right',
        help='Position of overlay (default: top-right)'
    )
    
    parser.add_argument(
        '--scale', '-s',
        help='Scale overlay image (e.g., "100:100", "50%%", "iw*0.5:ih*0.5")'
    )
    
    parser.add_argument(
        '--opacity',
        type=float,
        default=1.0,
        help='Opacity of overlay (0.0 to 1.0, default: 1.0)'
    )
    
    parser.add_argument(
        '--offset-x',
        type=int,
        default=10,
        help='X offset from edge (for edge positions) or absolute X (for custom) (default: 10)'
    )
    
    parser.add_argument(
        '--offset-y',
        type=int,
        default=10,
        help='Y offset from edge (for edge positions) or absolute Y (for custom) (default: 10)'
    )
    
    parser.add_argument(
        '--start-time',
        help='Start time for overlay (format: HH:MM:SS, MM:SS, or SS)'
    )
    
    parser.add_argument(
        '--duration',
        help='Duration of overlay (format: HH:MM:SS, MM:SS, or SS)'
    )
    
    args = parser.parse_args()
    
    # Validate opacity
    if not 0.0 <= args.opacity <= 1.0:
        print("❌ Error: Opacity must be between 0.0 and 1.0")
        sys.exit(1)
    
    # Check if ffmpeg is available
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed or not available in system PATH")
        print("Please install ffmpeg and ensure it's accessible from command line")
        sys.exit(1)
    
    try:
        # Validate input files
        video_file, image_file = validate_files(args.video, args.image)
        
        # Generate output filename if not specified
        if args.output is None:
            video_stem = video_file.stem
            video_ext = video_file.suffix
            args.output = f"output/{video_stem}_overlay{video_ext}"
        
        # Create output path (absolute)
        output_path = os.path.abspath(args.output)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Overlay image on video
        success = overlay_image_on_video(
            video_file=video_file,
            image_file=image_file,
            output_path=output_path,
            position=args.position,
            scale=args.scale,
            opacity=args.opacity,
            offset_x=args.offset_x,
            offset_y=args.offset_y,
            start_time=args.start_time,
            duration=args.duration
        )
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
