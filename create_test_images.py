#!/usr/bin/env python3
"""
Create test images for overlay testing.
Uses ffmpeg to generate simple logo/watermark images.
"""

import os
import subprocess
import sys


def create_test_logo(output_path: str, text: str = "LOGO", width: int = 200, height: int = 100, color: str = "red") -> bool:
    """
    Create a test logo image using ffmpeg.
    
    Args:
        output_path: Path where the logo image will be saved
        text: Text to display in the logo
        width: Width of the logo
        height: Height of the logo
        color: Background color of the logo
    
    Returns:
        True if successful, False otherwise
    """
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color={color}:size={width}x{height}:duration=1',
        '-vf', f'drawtext=fontsize=24:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2:text={text}',
        '-frames:v', '1',
        '-y',  # Overwrite if exists
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def create_transparent_watermark(output_path: str, text: str = "WATERMARK", size: int = 300) -> bool:
    """
    Create a transparent watermark PNG using ffmpeg.
    
    Args:
        output_path: Path where the watermark will be saved
        text: Text to display in the watermark
        size: Size of the square watermark
    
    Returns:
        True if successful, False otherwise
    """
    cmd = [
        'ffmpeg',
        '-f', 'lavfi',
        '-i', f'color=c=black@0.0:s={size}x{size}:d=1',
        '-vf', f'drawtext=fontsize=36:fontcolor=white@0.8:x=(w-text_w)/2:y=(h-text_h)/2:text={text}',
        '-frames:v', '1',
        '-y',  # Overwrite if exists
        output_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def main():
    """Create test images for overlay testing."""
    print("Creating test images for overlay functionality...")
    
    # Create test images directory
    test_dir = "test_images"
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test images
    test_images = [
        ("logo.png", lambda: create_test_logo(
            os.path.join(test_dir, "logo.png"), 
            text="MY LOGO", 
            width=150, 
            height=80, 
            color="blue"
        )),
        ("watermark.png", lambda: create_transparent_watermark(
            os.path.join(test_dir, "watermark.png"), 
            text="WATERMARK", 
            size=200
        )),
        ("small_logo.png", lambda: create_test_logo(
            os.path.join(test_dir, "small_logo.png"), 
            text="©", 
            width=50, 
            height=50, 
            color="gray"
        ))
    ]
    
    created_images = []
    for filename, create_func in test_images:
        print(f"Creating {filename}...")
        
        if create_func():
            print(f"✅ Created {filename}")
            created_images.append(filename)
        else:
            print(f"❌ Failed to create {filename}")
    
    if created_images:
        print(f"\n✅ Created {len(created_images)} test images in '{test_dir}' folder")
        print("\nNow you can test the overlay script:")
        
        # Check if we have test videos
        if os.path.exists("test_videos") and os.path.exists("output/test_videos.mp4"):
            print(f"python overlay_image.py \"output/test_videos.mp4\" \"{test_dir}/logo.png\"")
            print(f"python overlay_image.py \"output/test_videos.mp4\" \"{test_dir}/watermark.png\" --position center --opacity 0.7")
            print(f"python overlay_image.py \"output/test_videos.mp4\" \"{test_dir}/small_logo.png\" --position bottom-right")
        else:
            print("First create test videos with: python create_test_videos.py")
            print("Then run: python concatenate_videos.py test_videos")
            print(f"Finally test overlay: python overlay_image.py \"output/test_videos.mp4\" \"{test_dir}/logo.png\"")
        
        # Optional: Run overlay automatically
        if os.path.exists("output/test_videos.mp4"):
            response = input("\nWould you like to run a test overlay now? (y/n): ")
            if response.lower() == 'y':
                cmd = [sys.executable, "overlay_image.py", "output/test_videos.mp4", f"{test_dir}/logo.png", "--position", "top-right"]
                subprocess.run(cmd)
    else:
        print("❌ No test images were created. Check that ffmpeg is properly installed.")


if __name__ == "__main__":
    main()
