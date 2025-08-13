#!/usr/bin/env python3
"""
Test script for the video concatenation utility.
Creates sample video files for testing (requires ffmpeg).
"""

import os
import subprocess
import tempfile
import sys
from pathlib import Path


def create_test_video(output_path: str, duration: int = 5, color: str = "red", text: str = "Test") -> bool:
    """
    Create a test video file using ffmpeg.
    
    Args:
        output_path: Path where the test video will be saved
        duration: Duration of the video in seconds
        color: Background color of the test video
        text: Text to display in the video
    
    Returns:
        True if successful, False otherwise
    """
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color={color}:size=640x480:duration={duration}',
        '-vf', f'drawtext=fontsize=30:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:text={text}',
        '-y',  # Overwrite if exists
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def main():
    """Create test videos and demonstrate the concatenation utility."""
    print("Creating test videos for concatenation demo...")
    
    # Create a temporary directory for test videos
    test_dir = "test_videos"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test videos
    test_videos = [
        ("video1_intro.mp4", "red", "Video 1 - Intro"),
        ("video2_middle.mp4", "green", "Video 2 - Middle"),
        ("video3_outro.mp4", "blue", "Video 3 - Outro")
    ]
    
    created_videos = []
    for filename, color, text in test_videos:
        video_path = os.path.join(test_dir, filename)
        print(f"Creating {filename}...")
        
        if create_test_video(video_path, duration=3, color=color, text=text):
            print(f"✅ Created {filename}")
            created_videos.append(filename)
        else:
            print(f"❌ Failed to create {filename}")
    
    if created_videos:
        print(f"\n✅ Created {len(created_videos)} test videos in '{test_dir}' folder")
        print("\nNow you can test the concatenation script:")
        print(f"python concatenate_videos.py \"{test_dir}\" --output \"test_concatenated.mp4\"")
        
        # Optional: Run the concatenation automatically
        response = input("\nWould you like to run the concatenation now? (y/n): ")
        if response.lower() == 'y':
            cmd = [sys.executable, "concatenate_videos.py", test_dir, "--output", "test_concatenated.mp4"]
            subprocess.run(cmd)
    else:
        print("❌ No test videos were created. Check that ffmpeg is properly installed.")


if __name__ == "__main__":
    main()
