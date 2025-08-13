#!/usr/bin/env python3
"""
Video Concatenation Utility

This script finds all .mp4 files in a given folder and concatenates them
into a single video file using ffmpeg.
"""

import os
import sys
import argparse
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional


def find_mp4_files(folder_path: str, sort_method: str = "alphabetical") -> List[Path]:
    """
    Find all .mp4 files in the given folder and sort them.
    
    Args:
        folder_path: Path to the folder containing MP4 files
        sort_method: Method to sort files ("alphabetical", "date_created", "date_modified")
    
    Returns:
        List of Path objects for MP4 files
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder_path}")
    
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder_path}")
    
    # Find all .mp4 files (case insensitive)
    mp4_files = []
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == '.mp4':
            mp4_files.append(file_path)
    
    if not mp4_files:
        raise ValueError(f"No MP4 files found in folder: {folder_path}")
    
    # Sort files based on the specified method
    if sort_method == "alphabetical":
        mp4_files.sort(key=lambda x: x.name.lower())
    elif sort_method == "date_created":
        mp4_files.sort(key=lambda x: x.stat().st_ctime)
    elif sort_method == "date_modified":
        mp4_files.sort(key=lambda x: x.stat().st_mtime)
    else:
        raise ValueError(f"Invalid sort method: {sort_method}")
    
    return mp4_files


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


def create_concat_file(mp4_files: List[Path], temp_dir: str) -> str:
    """
    Create a temporary file listing all videos to concatenate.
    
    Args:
        mp4_files: List of MP4 file paths
        temp_dir: Temporary directory path
    
    Returns:
        Path to the temporary concat file
    """
    concat_file_path = os.path.join(temp_dir, 'concat_list.txt')
    
    with open(concat_file_path, 'w', encoding='utf-8') as f:
        for mp4_file in mp4_files:
            # Get absolute path and convert to forward slashes for ffmpeg
            abs_path = str(mp4_file.resolve()).replace('\\', '/')
            # Escape single quotes in file paths for ffmpeg
            escaped_path = abs_path.replace("'", r"\'")
            f.write(f"file '{escaped_path}'\n")
    
    return concat_file_path


def concatenate_videos(mp4_files: List[Path], output_path: str) -> bool:
    """
    Concatenate MP4 files using ffmpeg.
    
    Args:
        mp4_files: List of MP4 file paths to concatenate
        output_path: Path for the output concatenated video
    
    Returns:
        True if successful, False otherwise
    """
    print(f"Found {len(mp4_files)} MP4 files to concatenate:")
    for i, file_path in enumerate(mp4_files, 1):
        print(f"  {i}. {file_path.name}")
    
    print(f"\nConcatenating videos into: {output_path}")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Create the concat file
            concat_file_path = create_concat_file(mp4_files, temp_dir)
            
            # Run ffmpeg concatenation
            cmd = [
                'ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', concat_file_path,
                '-c', 'copy',  # Copy streams without re-encoding for speed
                '-y',  # Overwrite output file if it exists
                output_path
            ]
            
            print("\nRunning ffmpeg concatenation...")
            print(f"Command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\n✅ Successfully concatenated videos to: {output_path}")
                return True
            else:
                print(f"\n❌ Error during concatenation:")
                print(f"Error output: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"\n❌ Error during concatenation: {str(e)}")
            return False


def main():
    """Main function to handle command line arguments and execute concatenation."""
    parser = argparse.ArgumentParser(
        description="Concatenate all MP4 files in a folder into a single video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python concatenate_videos.py "C:\\Videos\\ToMerge"  # Output: output/ToMerge.mp4
  python concatenate_videos.py "/home/user/videos" --output "output/merged.mp4"
  python concatenate_videos.py "./videos" --sort date_created
        """
    )
    
    parser.add_argument(
        'folder',
        help='Path to folder containing MP4 files to concatenate'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Output filename (default: output/[INPUT_FOLDER_NAME].mp4)'
    )
    
    parser.add_argument(
        '--sort', '-s',
        choices=['alphabetical', 'date_created', 'date_modified'],
        default='alphabetical',
        help='Method to sort files before concatenation (default: alphabetical)'
    )
    
    args = parser.parse_args()
    
    # Check if ffmpeg is available
    if not check_ffmpeg():
        print("❌ Error: ffmpeg is not installed or not available in system PATH")
        print("Please install ffmpeg and ensure it's accessible from command line")
        sys.exit(1)
    
    try:
        # Find MP4 files
        mp4_files = find_mp4_files(args.folder, args.sort)
        
        # Generate output path if not specified
        if args.output is None:
            # Get the folder name from the input path
            folder_name = os.path.basename(os.path.abspath(args.folder))
            args.output = f"output/{folder_name}.mp4"
        
        # Create output path (absolute)
        output_path = os.path.abspath(args.output)
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Concatenate videos
        success = concatenate_videos(mp4_files, output_path)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
