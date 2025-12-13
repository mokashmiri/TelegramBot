# Telegram Music Bot - Genre Classification System

> An interactive Telegram bot designed to streamline music categorization and organization through automated genre classification and group-based file management.

GenreBot is a Python-based Telegram bot that provides a user-friendly interface for uploading music files and classifying them by genre. The bot features a robust validation system to ensure only authorized users can interact with it, and automatically tags uploaded files with user information and selected genres before forwarding them to predefined groups.

---

## Table of Contents

- [Technologies](#technologies)
- [Features](#features)
- [Architecture](#architecture)
- [Key Concepts](#key-concepts)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)

---

## Technologies

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.x |
| **Framework** | python-telegram-bot or Pyrogram |
| **API** | Telegram Bot API |
| **Paradigm** | Event-driven Programming, Object-Oriented Programming |
| **Version Control** | Git (GitHub) |

---

## Features

### Music File Management
- **File Upload**: Users can upload music files through the bot interface
- **Genre Classification**: Interactive button-based genre selection system
- **Automatic Tagging**: Files are tagged with user name and selected genre
- **Group Forwarding**: Classified files are automatically forwarded to designated groups

### User Authentication
- **Authorization System**: Robust validation to restrict bot access to authorized users only
- **User Verification**: Secure user authentication mechanism
- **Access Control**: Prevents unauthorized usage

### User Interface
- **Button-Based Interaction**: Simple and intuitive button interface for genre selection
- **User-Friendly Design**: Clear prompts and easy-to-use controls
- **Interactive Feedback**: Real-time responses to user actions

### File Organization
- **Genre-Based Categorization**: Music files organized by musical genre
- **Metadata Tagging**: User and genre information embedded in file metadata
- **Structured Group Management**: Files forwarded to appropriate genre-specific groups

---

## Architecture

### Bot Framework
The bot is built using Python Telegram Bot libraries:
- Event-driven architecture for handling user interactions
- Command handlers for bot commands
- Callback query handlers for button interactions
- File handling for music file processing

### Key Components

**Bot Core**
- Main bot initialization and configuration
- Event loop management
- Command registration and handling

**Authentication Module**
- User authorization logic
- Access control implementation
- User validation system

**File Processing Module**
- Music file upload handling
- File metadata extraction and modification
- File forwarding logic

**Genre Management**
- Genre selection interface
- Genre-to-group mapping
- Classification logic

---

## Key Concepts

- **Telegram Bot API**: Integration with Telegram's bot framework
- **Event-Driven Programming**: Handling user interactions through events
- **File Handling**: Processing and managing music file uploads
- **User Authentication**: Secure access control mechanisms
- **Metadata Management**: Tagging files with user and genre information
- **Group Management**: Automated file forwarding to organized groups
- **Button Interfaces**: Interactive inline keyboard for user interaction

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Telegram Bot Token (obtain from @BotFather)
- Telegram API credentials (if using Pyrogram)
- Access to Telegram groups for file forwarding

### Installation

1. Clone the repository:
```bash
git clone https://github.com/mokashmiri/TelegramBot.git
cd TelegramBot
```

2. Navigate to the Telegram Music Bot directory:
```bash
cd "Telegram Music Bot"
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the bot (see Configuration section)

5. Run the bot:
```bash
python bot.py
```

Or use the appropriate main file name for your implementation.

---

## Configuration

### Environment Variables

Create a `.env` file or configuration file with the following variables:

- **BOT_TOKEN**: Your Telegram bot token from @BotFather
- **API_ID**: Telegram API ID (if using Pyrogram)
- **API_HASH**: Telegram API Hash (if using Pyrogram)
- **AUTHORIZED_USERS**: List of authorized user IDs
- **TARGET_GROUPS**: Group IDs for genre-based file forwarding
- **GENRE_MAPPING**: Mapping of genres to group IDs

### Bot Setup

1. Create a bot through @BotFather on Telegram
2. Obtain the bot token
3. Add the bot to your target groups with appropriate permissions
4. Configure authorized users list
5. Set up genre-to-group mappings

---

## Project Structure

```
Telegram Music Bot/
├── bot.py (or main bot file)
├── config.py (configuration management)
├── handlers/
│   ├── command_handlers.py
│   ├── callback_handlers.py
│   └── file_handlers.py
├── utils/
│   ├── auth.py (authentication utilities)
│   ├── file_processor.py (file handling)
│   └── genre_manager.py (genre classification)
├── requirements.txt
├── .env (environment variables)
└── README.md
```

**Key Components**:
- Main bot file with initialization
- Handler modules for different interaction types
- Utility modules for core functionality
- Configuration files

---

## Usage

### For Users

1. **Start the Bot**: Send `/start` command to the bot
2. **Upload Music File**: Send a music file to the bot
3. **Select Genre**: Use the interactive buttons to choose the appropriate genre
4. **Automatic Processing**: The bot tags and forwards the file to the designated group

### Bot Commands

- `/start`: Initialize interaction with the bot
- `/help`: Display help information and usage instructions
- `/genres`: View available genre options

### Genre Selection

When a music file is uploaded:
1. The bot presents genre selection buttons
2. User clicks the appropriate genre button
3. Bot processes the file with selected genre
4. File is tagged and forwarded automatically

### Authorization

Only users in the authorized list can:
- Upload files to the bot
- Interact with genre selection
- Use bot features

Unauthorized users receive an appropriate message.

---

## Technical Implementation

### File Processing

The bot handles music files by:
- Receiving file uploads through Telegram
- Extracting file metadata
- Adding user and genre tags
- Processing file information
- Forwarding to appropriate groups

### Genre Classification

Genre management includes:
- Predefined genre list
- Interactive button interface
- Genre-to-group mapping
- Classification logic execution

### Security Features

Authentication system provides:
- User ID verification
- Access control enforcement
- Secure interaction validation

---

## Notes

- The bot requires appropriate permissions in target groups
- Music file formats supported depend on Telegram's limitations
- Group IDs must be configured correctly for file forwarding
- User authorization list should be maintained for security
- The bot follows Telegram Bot API best practices

---

## License

Educational project developed for learning and demonstration purposes.

---

## Author

Developed as part of Python programming and Telegram bot development practice.

---

**Repository Status**: Active development
