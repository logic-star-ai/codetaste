# Refactor terminology from Resume/Pause to Start/Stop

## Summary
Rename all user-facing instances of "Resume/Pause" terminology to "Start/Stop" throughout the application to provide clearer, more intuitive semantics for torrent control actions.

## Changes

### Core API & Backend
- Renamed torrent control methods:
  - `pause()` → `stop()`
  - `resume()` → `start()`
  - `isPaused()` → `isStopped()`
  - `isResumed()` → `isRunning()`
- Renamed torrent states:
  - `PausedDownloading` → `StoppedDownloading`
  - `PausedUploading` → `StoppedUploading`
- Updated settings keys:
  - `AddTorrentPaused` → `AddTorrentStopped`
  - Added migration handler (version 8)

### GUI
- Updated menu items, buttons, and actions:
  - "Resume" → "Start", "Resume All" → "Start All"
  - "Pause" → "Stop", "Pause All" → "Stop All"
  - "Force Resume" → "Force Start"
- Renamed UI elements throughout:
  - MainWindow, TransferListWidget, OptionsDialog...
  - Keyboard shortcuts preserved (Ctrl+P, Ctrl+S)
- Updated context menus for torrents, categories, tags, trackers
- Renamed filters:
  - "Resumed"/"Paused" → "Running"/"Stopped"

### WebUI
- Renamed API endpoints:
  - `/api/v2/torrents/pause` → `/api/v2/torrents/stop`
  - `/api/v2/torrents/resume` → `/api/v2/torrents/start`
- Updated WebUI interface elements (JavaScript, HTML)
- Bumped API version: 2.10.4 → 2.11.0
- Renamed WebUI states: `pausedDL`/`pausedUP` → `stoppedDL`/`stoppedUP`

### CLI & Other
- Command-line option: `--add-paused` → `--add-stopped`
- Updated RSS auto-downloader terminology
- Updated log messages throughout

### Visual Assets
- Renamed/added icons:
  - `paused.svg`, `pause-session.svg` (new)
  - Updated `stopped.svg`, `torrent-stop.svg` to use square icon instead of pause bars

## Migration
Added settings migration (version 8) to automatically convert `AddTorrentPaused` → `AddTorrentStopped` on upgrade.