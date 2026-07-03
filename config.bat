@echo off
:: =====================================================================
:: Configuration Parameters for Database Download
:: =====================================================================

:: Google Drive File ID for db.sqlite3
set "FILE_ID=12c5Y6INCsb4TUmY2c_VRuGQgkHnkpFwp"

:: Local path where the database will be saved
set "DB_PATH=%~dp0db.sqlite3"

:: Direct download link constructed from FILE_ID
set "DOWNLOAD_URL=https://drive.google.com/uc?export=download&id=%FILE_ID%"

:: Git Configuration Parameters
set "GIT_USER_NAME=keoinn"
set "GIT_USER_EMAIL=keoinn@gmail.com"

