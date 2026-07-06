# Bank Status Bot

A Telegram bot for coordinating access to a shared banking client.

The bot was created to solve a real workflow problem in an accounting team: several employees may need to work with the same banking client, but simultaneous access should be avoided.

## Features

- Shows whether the banking client is currently available
- Allows a user to mark the bank as occupied
- Displays the name of the current user
- Prevents another user from taking over an occupied bank
- Prevents users from ending another user's session
- Shows a reminder after 15 minutes of continuous work
- Provides an emergency `/reset` command
- Saves the current state between bot restarts

## Tech Stack

- Python
- aiogram
- asyncio
- Telegram Bot API
- JSON
- PyInstaller

## How It Works

When a user enters the bank, the bot stores their Telegram ID and name.

The bank remains occupied until the same user leaves. After 15 minutes, the status message changes to indicate that the banking client has been in use for more than 15 minutes.

The current state is saved to a JSON file, allowing the bot to restore the active user after a restart.

## Configuration

Create a `config.py` file:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

The `config.py` file is excluded from Git and should never be committed.

## Run

Install dependencies:

```bash
pip install aiogram
```

Run the bot:

```bash
python main.py
```

## Deployment

The bot can be packaged as a standalone Windows executable using PyInstaller:

```bash
pyinstaller --onefile main.py
```