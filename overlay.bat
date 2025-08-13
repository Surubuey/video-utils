@echo off
REM Windows batch script to run image overlay on video
REM Usage: overlay.bat "video_file" "image_file" [output_filename] [position]

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Usage: overlay.bat "video_file" "image_file" [output_filename] [position]
    echo.
    echo Examples:
    echo   overlay.bat "video.mp4" "logo.png"
    echo   overlay.bat "video.mp4" "logo.png" "branded_video.mp4"
    echo   overlay.bat "video.mp4" "watermark.png" "output.mp4" "center"
    echo.
    echo Available positions: top-left, top-right, bottom-left, bottom-right, center
    exit /b 1
)

if "%~2"=="" (
    echo Error: Both video file and image file are required.
    echo Usage: overlay.bat "video_file" "image_file" [output_filename] [position]
    exit /b 1
)

set "video_file=%~1"
set "image_file=%~2"
set "output_file=%~3"
set "position=%~4"

REM Set default output filename if not provided
if "%output_file%"=="" (
    for %%I in ("%video_file%") do (
        set "video_name=%%~nI"
        set "video_ext=%%~xI"
    )
    set "output_file=output\!video_name!_overlay!video_ext!"
)

REM Set default position if not provided
if "%position%"=="" (
    set "position=top-right"
)

echo Running image overlay...
echo Video: %video_file%
echo Image: %image_file%
echo Output: %output_file%
echo Position: %position%
echo.

python overlay_image.py "%video_file%" "%image_file%" --output "%output_file%" --position "%position%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! Video with overlay saved as: %output_file%
) else (
    echo.
    echo Error occurred during overlay process.
)

pause
