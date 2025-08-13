@echo off
REM Windows batch script to run video concatenation
REM Usage: concatenate.bat "path\to\folder" [output_filename]

setlocal enabledelayedexpansion

if "%~1"=="" (
    echo Usage: concatenate.bat "path\to\folder" [output_filename]
    echo Example: concatenate.bat "C:\Videos\ToMerge"
    echo Example: concatenate.bat "C:\Videos\ToMerge" "my_video.mp4"
    exit /b 1
)

set "input_folder=%~1"
set "output_file=%~2"

if "%output_file%"=="" (
    set "output_file=concatenated_output.mp4"
)

echo Running video concatenation...
echo Input folder: %input_folder%
echo Output file: %output_file%
echo.

python concatenate_videos.py "%input_folder%" --output "%output_file%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! Video saved as: %output_file%
) else (
    echo.
    echo Error occurred during concatenation.
)

pause
