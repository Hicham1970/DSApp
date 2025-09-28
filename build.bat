@echo off
echo ===================================================
echo      Building DraftSurveyApp Executable
echo ===================================================

echo.
echo Cleaning up old build files...
if exist "dist" (
    rmdir /s /q dist
    echo "dist" folder removed.
)
if exist "build" (
    rmdir /s /q build
    echo "build" folder removed.
)
if exist "DraftSurveyApp.spec" (
    del DraftSurveyApp.spec
    echo "spec" file removed.
)

echo.
echo Running PyInstaller...
pyinstaller --name "DraftSurveyApp" --onefile --windowed --icon="images/ico.ico" --add-data "images;images" main.py

echo.
echo ===================================================
echo      Build process finished.
echo ===================================================
echo.
echo Your executable is located in the 'dist' folder.
echo.

pause