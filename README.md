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
- [Deployment and Maintenance](#deployment-and-maintenance)
  - [AWS EC2 Deployment](#aws-ec2-deployment)
  - [Maintenance and Monitoring](#maintenance-and-monitoring)
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
| **Cloud Platform** | AWS EC2 |
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

## Deployment and Maintenance

### AWS EC2 Deployment

The bot can be deployed and maintained on AWS EC2 for reliable, scalable, and cost-effective hosting.

#### Prerequisites for EC2 Deployment

- AWS Account with EC2 access
- EC2 instance (Ubuntu 20.04 LTS or Amazon Linux 2 recommended)
- Security Group configured to allow necessary traffic
- SSH access to the EC2 instance

#### EC2 Instance Setup

1. **Launch EC2 Instance**:
   - Choose an appropriate instance type (t2.micro or t3.micro for small bots)
   - Select Ubuntu Server 20.04 LTS or Amazon Linux 2 AMI
   - Configure security group to allow SSH (port 22)
   - Create or select a key pair for SSH access

2. **Connect to EC2 Instance**:
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip-address
```

3. **Install Dependencies**:
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip -y

# Install git
sudo apt install git -y
```

4. **Clone and Setup Bot**:
```bash
# Clone repository
git clone https://github.com/mokashmiri/TelegramBot.git
cd TelegramBot/Telegram\ Music\ Bot

# Install Python dependencies
pip3 install -r requirements.txt

# Create .env file with configuration
nano .env
```

5. **Configure Environment Variables**:
   - Add all required environment variables to `.env` file
   - Ensure BOT_TOKEN, API_ID, API_HASH, and other credentials are set

6. **Run Bot in Background**:
```bash
# Using nohup
nohup python3 bot.py > bot.log 2>&1 &

# Or using screen (recommended)
screen -S telegrambot
python3 bot.py
# Press Ctrl+A then D to detach
```

#### Using systemd for Service Management

Create a systemd service for better process management:

1. **Create Service File**:
```bash
sudo nano /etc/systemd/system/telegrambot.service
```

2. **Service Configuration**:
```ini
[Unit]
Description=Telegram Music Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TelegramBot/Telegram Music Bot
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 /home/ubuntu/TelegramBot/Telegram\ Music\ Bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. **Enable and Start Service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegrambot
sudo systemctl start telegrambot
```

4. **Check Service Status**:
```bash
sudo systemctl status telegrambot
```

### Maintenance and Monitoring

#### Monitoring Bot Status

1. **Check Bot Logs**:
```bash
# If using systemd
sudo journalctl -u telegrambot -f

# If using nohup
tail -f bot.log

# If using screen
screen -r telegrambot
```

2. **Monitor System Resources**:
```bash
# Check CPU and memory usage
htop

# Check disk space
df -h

# Check bot process
ps aux | grep bot.py
```

#### Regular Maintenance Tasks

1. **Update Bot Code**:
```bash
cd TelegramBot
git pull origin main
# Restart service if using systemd
sudo systemctl restart telegrambot
```

2. **Update System Packages**:
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Rotate Logs**:
   - Implement log rotation to prevent disk space issues
   - Use `logrotate` or manual cleanup of old log files

4. **Backup Configuration**:
   - Regularly backup `.env` file and configuration
   - Store backups in S3 or another secure location

#### EC2 Cost Optimization

- Use EC2 Spot Instances for cost savings (with appropriate handling)
- Monitor instance usage and resize if needed
- Set up CloudWatch alarms for cost monitoring
- Use Reserved Instances for long-term deployments

#### Security Best Practices

1. **SSH Security**:
   - Use key-based authentication only
   - Disable password authentication
   - Regularly rotate SSH keys

2. **Firewall Configuration**:
   - Only open necessary ports
   - Use Security Groups effectively
   - Implement VPC for network isolation

3. **Environment Variables**:
   - Never commit `.env` file to repository
   - Use AWS Systems Manager Parameter Store or Secrets Manager for sensitive data
   - Regularly rotate API keys and tokens

4. **Access Control**:
   - Use IAM roles for EC2 instance permissions
   - Implement least privilege principle
   - Enable CloudTrail for audit logging

#### Troubleshooting

1. **Bot Not Responding**:
   - Check service status: `sudo systemctl status telegrambot`
   - Review logs for errors
   - Verify network connectivity
   - Check Telegram API status

2. **High Resource Usage**:
   - Monitor with `htop` or CloudWatch
   - Check for memory leaks
   - Consider upgrading instance type if needed

3. **Connection Issues**:
   - Verify security group rules
   - Check bot token validity
   - Ensure internet connectivity on EC2 instance

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
