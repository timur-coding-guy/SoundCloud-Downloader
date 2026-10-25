# SoundCloud Downloader

Telegram bot for downloading audio from SoundCloud with original metadata and quality.
No logs and saving data at all, so all userdata is safe. Created with AI. 

## Configuration

Create a `.env` file in the project root.

Add your Telegram bot token to `.env`:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

Get your bot token from [@BotFather](https://t.me/botfather) on Telegram.

## Installation

### Windows

#### Prerequisites

Install FFmpeg. Two options:

**Option 1: Chocolatey (recommended)**

Run PowerShell as Administrator:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 1; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Then install FFmpeg:

```powershell
choco install ffmpeg
```

**Option 2: Manual installation**

Download FFmpeg from https://ffmpeg.org/download.html, extract it, and add the `bin` folder to your PATH environment variable.

#### Setup

Install uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Install dependencies:

```powershell
uv sync
```

Run the bot:

```powershell
uv run python src/main.py
```

### macOS

#### Prerequisites

Install FFmpeg:

```bash
brew install ffmpeg
```

If you don't have Homebrew, install it first:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Setup

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```bash
uv sync
```

Run the bot:

```bash
uv run python src/main.py
```

### Linux (Ubuntu/Debian)

#### Prerequisites

Install FFmpeg:

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Setup

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```bash
uv sync
```

Run the bot:

```bash
uv run python src/main.py
```

### Linux (Arch)

#### Prerequisites

Install FFmpeg:

```bash
sudo pacman -S ffmpeg
```

#### Setup

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install dependencies:

```bash
uv sync
```

Run the bot:

```bash
uv run python src/main.py
```

## Docker

Docker includes FFmpeg in the container, so no local installation required.

Build and run:

```bash
cd docker; docker-compose up -d --build
```

Stop and remove container and image:

```bash
cd docker; docker-compose down --rmi all
```

## Usage

1. Send a Soundcloud link to the bot
2. Bot downloads the audio with original metadata
3. MP3 file is sent with:
   - 🖼️ button opens the artwork
   - Change Metadata button lets you edit title and artist


## Project Structure

```
src/
├── bot/
│   ├── __init__.py
│   └── handlers.py
├── core/
│   ├── __init__.py
│   └── config.py
├── services/
│   ├── __init__.py
│   └── downloader.py
├── __init__.py
└── main.py
docker/
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```
