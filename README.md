# AssetTrack — Asset Management System

## Files in this folder
```
assettrack/
├── index.html      ← The app (open this in browser)
├── server.py       ← Local server (run this first!)
├── START.bat       ← Double-click to start on Windows
├── UPDATE_INDEX.bat← Update index.html only from public GitHub
├── data.json       ← Your data (auto-created on first run)
└── README.md       ← This file
```

## How to run

### Windows (easiest)
Double-click **START.bat**
Then open your browser at: http://localhost:8765

### Mac / Linux
Open Terminal in this folder and run:
```
python3 server.py
```
Then open your browser at: http://localhost:8765

## Requirements
- Python 3 (free download: https://www.python.org)
- Any modern browser (Chrome, Firefox, Edge)

## Transferring to another computer
Just copy the ENTIRE folder to your flashdisk.
The data.json file contains all your data.

## Update index.html only (without Git)
1. Edit `UPDATE_INDEX.bat` and set your raw GitHub URL:
   `https://raw.githubusercontent.com/USERNAME/REPO/main/index.html`
2. Double-click `UPDATE_INDEX.bat`
3. It will:
   - backup current `index.html` to `index.backup.html`
   - download latest `index.html`
   - keep `data.json` untouched

## Default login
- Username: admin
- Password: admin123
