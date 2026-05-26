<div align="center">

# AssetTrack — Asset Management System

![Python](https://img.shields.io/badge/Python-3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES2017-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![bcrypt](https://img.shields.io/badge/bcrypt-4A90D9?style=for-the-badge&logo=lock&logoColor=white)
![JSON](https://img.shields.io/badge/Storage-JSON-000000?style=for-the-badge&logo=json&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A fully self-contained asset management web app for **BNNK Sleman** (government agency).  
Zero external dependencies — just Python 3 and a browser.

---

</div>

## Features

| Feature | Description |
|---------|-------------|
| **Authentication** | Login/logout with bcrypt-hashed passwords; Administrator and Viewer roles |
| **Dashboard** | Statistics cards, insight tables (by location/type/source), recent assets, PDF print |
| **Master Data** | Full CRUD for Locations, Asset Types, and Asset Sources with hierarchical support |
| **Asset Management** | CRUD with auto-generated codes, file attachments (images + documents), image lightbox |
| **Condition Monitoring** | Create quarterly monitoring reports, snapshots, auto-update asset conditions |
| **Reports & Printing** | Asset list, monitoring report, room inventory (formal government format), barcode stickers |
| **Excel Export** | All printed reports also exportable as `.xls` |
| **Document Management** | Folder-based file organization with upload, download, and delete |
| **Variable Settings** | Key-value configuration store, auto-generate asset codes |
| **Offline-Ready** | Works without internet (Google Fonts loaded once on first visit) |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3 — standard library (`http.server`, zero pip dependencies) |
| **Frontend** | Vanilla JavaScript ES2017 — no frameworks (no React, Vue, jQuery) |
| **Styling** | Custom CSS + IBM Plex Sans & Mono (Google Fonts) |
| **Password Hashing** | bcrypt.js (standalone, ~19 KB) |
| **Data Storage** | JSON flat file (`data.json`) |
| **File Uploads** | Custom multipart/form-data parser (no external library) |
| **Session** | `localStorage` |

## Project Structure

```
simple-asset-management/
├── index.html           ← Single-page app (all HTML/CSS/JS, ~3500 lines)
├── server.py            ← Python 3 HTTP server + REST API (260 lines)
├── bcrypt.min.js        ← Standalone bcrypt library
├── data.json            ← Auto-created on first run (all data, gitignored)
├── logo.png             ← Logo BNNK Sleman
├── logo_pemda.png       ← Logo Pemda
├── START.bat            ← Windows launcher (double-click to start)
├── UPDATE_INDEX.bat     ← Update index.html from GitHub (preserves data)
└── README.md            ← This file
```

## Installation

### Prerequisites

- **Python 3** — [Download here](https://www.python.org/downloads/)
- Any modern browser (Chrome, Firefox, Edge)

### 1. Download the project

Clone the repo or download the ZIP and extract it:

```bash
git clone https://github.com/YOUR_USERNAME/simple-asset-management.git
cd simple-asset-management
```

### 2. Start the server

**Windows** — Double-click `START.bat`

**Mac / Linux** — Open a terminal in the project folder:

```bash
python3 server.py
```

### 3. Open in browser

Navigate to: **http://localhost:8765**

### 4. Login

| User | Password | Role |
|------|----------|------|
| `admin` | `admin123` | Administrator (full access) |

> Change the password after your first login via Variable Settings.

## Transferring to Another Computer

Just copy the entire folder to a flash drive. The `data.json` file contains all your data — no database setup needed.

## Updating index.html (Without Git)

Edit `UPDATE_INDEX.bat` and set your raw GitHub URL, then double-click it:

```
https://raw.githubusercontent.com/USERNAME/REPO/main/index.html
```

The script will:
- Backup current `index.html` → `index.backup.html`
- Download the latest `index.html` from GitHub
- Keep `data.json` untouched

## License

MIT
