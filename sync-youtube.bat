@echo off
echo ===================================================
echo     Sub-Record Studio - YouTube Portfolio Sync
echo ===================================================
echo.
echo Sedang mengambil data video terbaru dari YouTube channel...
echo Channel: @subrecordstudio
echo.
python scripts/sync-youtube.py
echo.
echo ===================================================
echo Selesai! Buka index.html atau latest-releases.html
echo di browser untuk melihat hasil update.
echo ===================================================
pause
