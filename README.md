# Wizard Lizard Discord Bot

Wizard Lizard is a multi-purpose Discord bot built with Python and `discord.py`. The current implementation provides a variety of functionalities including server moderation, a local economy system, Reddit integrations for memes and facts, and an AI-powered conversational interface. It is structured to run continuously, using Flask to maintain uptime via an HTTP endpoint (often useful in environments like Replit).

The bot organizes its features into a modular Cog architecture, making it easy to extend or manage separate domains like economy or moderation without disrupting the main event loop.

## Table of Contents
- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Folder Structure](#folder-structure)
- [Important Code Concepts](#important-code-concepts)
- [Architectural Decisions](#architectural-decisions)
- [Data Model](#data-model)
- [Main User Flows](#main-user-flows)
- [Setup Instructions](#setup-instructions)
- [Configuration Notes](#configuration-notes)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [License](#license)

## About the Project
This project acts as a functional Discord bot for server administration and user engagement. It solves the problem of needing multiple different bots for moderation, fun/memes, and economy by consolidating these features into a single configurable instance.

The intended use case is for Discord server administrators who want a straightforward, self-hosted bot that handles common community management tasks. A server member can use the bot to check their bank balance, fetch a random shower thought from Reddit, or interact with an AI. Moderators can use it to issue polls, lock channels, and manage slow modes. The project currently uses flat JSON files for some state management (like prefixes and the economy) and an SQLite database for the AI channel configuration, which is appropriate for a local or prototype-stage bot.

## Key Features

### Modular Commands (Cogs)
The bot separates its logic into different Cogs (e.g., `economy`, `fun`, `moderation`, `reddit`). This allows different sets of commands to be loaded, unloaded, or reloaded independently.

### Moderation System
Moderators with the appropriate permissions can manage the server through commands. The current codebase supports locking/unlocking channels, adjusting slow mode delays, checking server bans, and generating simple embed-based polls using reactions.

### Economy System
A localized economy allows users to track a "wallet" and a "bank" balance. The current implementation uses a local JSON file (`bank.json`) to persist account data. Users can check their balances, deposit funds from their wallet into their bank, and (partially implemented) withdraw funds.

### Reddit Integration
Users can request content directly from various subreddits. The bot utilizes `asyncpraw` to asynchronously fetch random hot posts from subreddits like `r/fact`, `r/Animemes`, `r/tifu`, `r/teenagers`, and `r/showerthoughts`.

### Conversational AI
The bot incorporates the `prsaw` (RandomStuff) library to respond to messages. When configured to listen in a specific channel (tracked via the SQLite database `main.db`), the bot will asynchronously fetch an AI-generated response and reply to the user.

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| **Language** | Python 3 | Core application language |
| **Discord API** | `discord.py` | Wrapper for interacting with the Discord gateway and REST API |
| **Web Server** | Flask | Provides a simple HTTP server (`keep_alive`) to maintain uptime in containerized hosting |
| **Data Persistence** | JSON & SQLite3 | `prefixes.json` and `bank.json` store simple key-value state, while SQLite tracks AI channel configurations |
| **API Wrapper** | `asyncpraw` / `aiohttp` | Asynchronous HTTP clients for fetching Reddit posts and random cat images |
| **Package Manager**| Poetry | Manages dependencies and virtual environments via `pyproject.toml` |

## System Architecture
The application runs as a continuous asynchronous event loop managed by `discord.py`.

1. **Entry Point:** `main.py` initializes the bot, loads the configured prefix mapping from `prefixes.json`, connects to the Discord gateway, and loads all extensions (Cogs) from the `cogs/` directory.
2. **Web Server Thread:** A secondary thread runs a simple Flask server (`webserver.py`) on port 8080 to listen for incoming HTTP requests.
3. **Command Processing:** When a message is received, the main loop checks if it starts with the guild's specific prefix. If so, it routes the message to the appropriate loaded Cog.
4. **AI Processing:** If a message is sent in a channel designated for AI chat (checked against `main.db`), the bot intercepts the message, cleans up mentions, and queries the RandomStuff API before returning the response to the channel.

## Folder Structure

```txt
.
├── main.py                 # Bot entry point and core event listeners
├── webserver.py            # Flask app to keep the process alive
├── pyproject.toml          # Poetry dependency configuration
├── prefixes.json           # JSON store for per-guild command prefixes
├── cogs/                   # Directory containing all modular extensions
│   ├── commands.py         # General commands
│   ├── economy.py          # Economy system logic (balance, deposit, etc.)
│   ├── fun.py              # Fun and miscellaneous commands
│   ├── Moderation_Commands.py # Commands for locking channels, slowmode, bans
│   ├── reddit.py           # Commands interacting with the Reddit API
│   ├── json/               # Folder containing local JSON state
│   │   └── bank.json       # Economy data store
│   └── dbs/                # Folder containing local database files
│       └── main.db         # SQLite database for AI channel tracking
```

## Important Code Concepts

### Asynchronous Cog Loading
The bot dynamically loads all `.py` files inside the `cogs/` directory on startup. This is a standard `discord.py` pattern that keeps the main application file clean and allows command logic to be encapsulated.

### JSON-Based State Management
For simpler configuration like custom server prefixes and user bank balances, the bot reads and writes directly to local JSON files (`prefixes.json`, `cogs/json/bank.json`). While not highly scalable for large distributed deployments, it provides a fast, file-based persistence layer for a single-instance bot.

### Background Web Server
The inclusion of a Flask web server running on a separate thread (`keep_alive`) is a common pattern for hosting bots on services like Replit that will sleep a process if it doesn't receive HTTP traffic.

## Architectural Decisions

**Using File-Based Storage for the Economy**
The current implementation uses `bank.json` for economy balances. This choice makes sense for the prototype stage as it avoids the overhead of managing a relational database schema while the commands are being developed. The tradeoff is that concurrent writes to the JSON file could lead to data loss under high load, which would eventually require migrating to a robust database like PostgreSQL or expanding the SQLite implementation.

**Hardcoded API Keys in Source**
The current codebase includes hardcoded credentials for Reddit (`praw` client ID/secret), Statcord, and the Discord bot token (though currently invalid/revoked). This approach suggests the bot was developed in a private environment. Moving these to environment variables is a critical next step for security.

**SQLite for AI Channel Tracking**
The bot connects to `cogs/dbs/main.db` to check if a channel should trigger the AI response loop. Using SQLite here is a good intermediate step, providing structured querying without needing an external database service.

## Data Model

**Bank Account (JSON)**
A dictionary mapping user IDs to their financial state.
- `wallet`: Integer representing on-hand currency.
- `bank`: Integer representing stored currency.

**Guild Prefix (JSON)**
A dictionary mapping guild IDs (strings) to their designated command prefix (e.g., `w!`).

## Main User Flows

**Changing a Server Prefix**
1. An administrator uses the command `w!changeprefix <new_prefix>`.
2. The bot reads `prefixes.json`.
3. The bot updates the key corresponding to the guild ID with the new prefix.
4. The bot writes the updated dictionary back to the JSON file.
5. All future command parsing for that guild uses the new prefix.

**Depositing Currency**
1. A user runs `w!deposit 100`.
2. The `Economy` cog loads `bank.json`.
3. It checks if the user has an account; if not, one is initialized with 0 balances.
4. It verifies the user has enough in their `wallet`.
5. It subtracts the amount from `wallet`, adds it to `bank`, and saves the file.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher.
- A Discord Developer Portal account with a registered bot and its token.
- A Reddit account with API credentials (Client ID and Secret) for `asyncpraw`.

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Install dependencies using Poetry (based on `pyproject.toml`):
```bash
poetry install
```
Alternatively, you can install the core packages via pip:
```bash
pip install discord.py praw aiohttp asyncpraw prsaw flask statcord.py
```

### Environment Variables
The codebase currently hardcodes several keys, but for a proper deployment, you should refactor the code to use the `os` module. You will need:
- `DISCORD_BOT_TOKEN`
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USERNAME`
- `REDDIT_PASSWORD`
- `STATCORD_KEY`

### Running Locally

Activate your virtual environment and start the bot:
```bash
poetry run python main.py
```
Or, if not using poetry directly:
```bash
python main.py
```

## Configuration Notes
- **`pyproject.toml`**: Configures the Poetry environment and lists project dependencies (e.g., `discord`, `praw`, `flask`).
- **`prefixes.json`**: This file must be readable and writable by the bot process, as it is updated dynamically when the bot joins a new server or an admin changes the prefix.

## Future Improvements

- **Remove Hardcoded Credentials:** Refactor all API keys, bot tokens, and passwords out of the source files (`main.py`, `cogs/reddit.py`) and into environment variables (e.g., using `dotenv`).
- **Database Migration:** Transition the `bank.json` and `prefixes.json` state into a robust database (like PostgreSQL or expanding the SQLite usage) to prevent data corruption during concurrent file writes.
- **Error Handling:** Implement comprehensive error handlers (e.g., `on_command_error`) to gracefully inform users when a command fails or permissions are missing.
- **Finish Pending Implementations:** Complete the `withdraw` command in the economy module, which is currently stubbed out but lacks the final logic to update and save the balances.
- **Remove Blocking Calls:** Ensure that file I/O operations (like reading/writing `prefixes.json`) are handled asynchronously or offloaded to a thread pool, as synchronous file operations can block the `discord.py` event loop.

## Learning Outcomes
This project demonstrates an understanding of event-driven asynchronous programming in Python. It highlights how to build a scalable bot using a modular architecture (Cogs) to separate concerns across domains like moderation, external API integrations, and local state management. The project also shows practical awareness of deployment strategies, evidenced by the inclusion of a lightweight web server to maintain process uptime.

## License
License information has not been specified yet.
