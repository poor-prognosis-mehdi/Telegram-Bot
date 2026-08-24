# Personal Telegram Bot

A Telegram bot for personal introduction and educational content about viral sexually transmitted infections (HPV, HIV, HBV, HSV), with an anonymous messaging feature for users.

## Features

- 👤 **About Me** — displays a short personal introduction
- 📱 **Contact Me** — direct link to personal Telegram account
- 🪪 **View Card** — link to a personal profile page (Linktree)
- ✉️ **Personal Message** — users can send anonymous questions; the admin can reply without ever seeing the user's identity
- 🎬 Educational buttons with YouTube videos about HPV, HIV, HBV, and HSV
- 🧪 **Diagnostic Tests** — information about relevant lab tests for each disease
- 🌐 **Trusted Medical Sources** — links to CDC, WHO, and Mayo Clinic

## Requirements

- Python 3.9 or higher
- A bot token from [@BotFather](https://t.me/BotFather)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/USERNAME/REPO_NAME.git
   cd REPO_NAME
   ```

2. Install the required library:
   ```bash
   pip install pyTelegramBotAPI
   ```

3. Set your bot token and admin ID in `bot.py`:
   ```python
   TOKEN = "your_bot_token"
   ADMIN_ID = your_telegram_numeric_id
   ```

   > ⚠️ **Security warning:** Never commit your real bot token to a public GitHub repository. It's recommended to load the token from an environment variable instead.

4. Run the bot:
   ```bash
   python bot.py
   ```

## Anonymous Message Reply System

When a user sends a question via the "Personal Message" button:

- The question is forwarded to the admin along with a **question code** (no name or username is shown)
- The admin replies by sending the following command in the chat with the bot:
  ```
  /reply question_code your_answer
  ```
- The reply is automatically sent to that user, without revealing their identity to the admin

> ℹ️ Question codes are stored in memory (RAM) only and will be lost if the bot restarts.

## Project Structure

```
.
├── bot.py          # Main bot code
└── README.md       # This file
```

## Running Continuously on a Server (VPS)

To keep the bot running 24/7, use a process manager such as `systemd`, `screen`, `tmux`, or `pm2` so it stays active after the terminal closes or the server restarts.

## Disclaimer

The information provided by this bot is for general educational purposes only and is not a substitute for professional medical advice.
