import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
import time
from datetime import datetime

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_ID = 27218759
GROUP_CHAT_ID = -1001317756719

# Load allowed users from a file or create the file if it doesn't exist
def load_allowed_users():
    try:
        with open('allowed_users.txt', 'r') as file:
            return {int(line.split()[0]): line.split()[1] if len(line.split()) > 1 else "Unknown" for line in file if line.strip()}
    except FileNotFoundError:
        with open('allowed_users.txt', 'w') as file:
            pass
        return {ADMIN_USER_ID: datetime.now().strftime('%Y-%m-%d')}

# Save allowed users back to the file
def save_allowed_users():
    with open('allowed_users.txt', 'w') as file:
        for user_id, date_added in ALLOWED_USERS.items():
            file.write(f"{user_id} {date_added}\n")

ALLOWED_USERS = load_allowed_users()
USER_INTERACTIONS = {user_id: 0 for user_id in ALLOWED_USERS}
BROADCAST_HISTORY = []

ADD_USER, REMOVE_USER, BROADCAST = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    USER_INTERACTIONS[user_id] = USER_INTERACTIONS.get(user_id, 0) + 1
    await update.message.reply_text('Hello! Send me a music file.')

async def add_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to add users.")
        return ConversationHandler.END

    await update.message.reply_text("Please provide the user ID to add.")
    return ADD_USER

async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        new_user_id = int(update.message.text)
        if new_user_id not in ALLOWED_USERS:
            ALLOWED_USERS[new_user_id] = datetime.now().strftime('%Y-%m-%d')
            USER_INTERACTIONS[new_user_id] = 0
            save_allowed_users()
            await update.message.reply_text(f"User {new_user_id} has been added.")
        else:
            await update.message.reply_text(f"User {new_user_id} is already allowed.")
    except ValueError:
        await update.message.reply_text("Please provide a valid user ID.")
    return ConversationHandler.END

async def remove_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to remove users.")
        return ConversationHandler.END

    await update.message.reply_text("Please provide the user ID to remove.")
    return REMOVE_USER

async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        user_id_to_remove = int(update.message.text)
        if user_id_to_remove in ALLOWED_USERS:
            del ALLOWED_USERS[user_id_to_remove]
            USER_INTERACTIONS.pop(user_id_to_remove, None)
            save_allowed_users()
            await update.message.reply_text(f"User {user_id_to_remove} has been removed.")
        else:
            await update.message.reply_text(f"User {user_id_to_remove} is not in the allowed users list.")
    except ValueError:
        await update.message.reply_text("Please provide a valid user ID.")
    return ConversationHandler.END

async def list_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to view the user list.")
        return

    users_list = '\n'.join([f"{user_id} (added on {date_added})" for user_id, date_added in ALLOWED_USERS.items()])
    await update.message.reply_text(f"Allowed users:\n{users_list}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        return
    USER_INTERACTIONS[update.effective_user.id] += 1
    help_text = ("Use this bot to upload and categorize music files. Here's how you can use it:\n"
                 "/start - Begin interacting with the bot.\n"
                 "/help - Display this message.\n"
                 "/about - Learn about this bot.\n"
                 "/add_user - Add a new user (admin only).\n"
                 "/remove_user - Remove an allowed user (admin only).\n"
                 "/list_users - List all allowed users (admin only).\n"
                 "/broadcast - Send a message to all users (admin only).\n"
                 "/report - Generate a usage report (admin only).")
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    USER_INTERACTIONS[update.effective_user.id] += 1
    about_text = ("Bot Information:\n"
                  "Version: 1.6\n"
                  "Owner: Mo Kashmiri\n"
                  "Launch Date: February 16, 2024\n"
                  "<<last update: 02 Oct 2024>>\n"
                  "This bot helps you categorize and forward music files. Enjoy using it!")
    await update.message.reply_text(about_text)

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to send broadcast messages.")
        return ConversationHandler.END

    await update.message.reply_text("Please provide the message to broadcast.")
    return BROADCAST

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = update.message.text
    if not message:
        await update.message.reply_text("Please provide a message to broadcast.")
        return ConversationHandler.END

    BROADCAST_HISTORY.append((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))
    for user_id in ALLOWED_USERS:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    await update.message.reply_text("Broadcast message sent.")
    return ConversationHandler.END

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You are not authorized to generate a report.")
        return

    report_text = "Usage Report:\n"
    report_text += f"Total allowed users: {len(ALLOWED_USERS)}\n"
    report_text += "Allowed Users:\n" + '\n'.join([f"{user_id} (added on {date_added})" for user_id, date_added in ALLOWED_USERS.items()])
    report_text += "\n\nUser Interactions:\n"
    report_text += '\n'.join([f"User {user_id}: {count} interactions" for user_id, count in USER_INTERACTIONS.items()])
    report_text += "\n\nBroadcast History:\n"
    report_text += '\n'.join([f"{timestamp}: {message}" for timestamp, message in BROADCAST_HISTORY])

    await update.message.reply_text(report_text)

async def handle_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return

    USER_INTERACTIONS[update.effective_user.id] += 1
    context.user_data['music_file_id'] = update.message.message_id
    await show_genres(update.message, context)

async def show_genres(message, context: ContextTypes.DEFAULT_TYPE) -> None:
    genres = [
        "#Chill", "#Latin", "#Dance", "#HipHop", "#HIGH_TEMPO",
        "#FA_VINTAGE", "#EN_VINTAGE", "#Birthday", "#AfterParty",
        "#Khaltoor", "#Arabic", "#Turki", "#Pop_Chosnale", "#Indian"
    ]

    genre_buttons = [[InlineKeyboardButton(genre, callback_data=f'genre_{genre}')]
                     for genre in genres]

    reply_markup = InlineKeyboardMarkup(genre_buttons)
    sent_message = await message.reply_text('Please choose the genre of the music:', reply_markup=reply_markup)
    context.user_data['last_message_id'] = sent_message.message_id

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('genre_'):
        context.user_data['selected_genre'] = data
        await query.message.delete()
        await confirm_forward(update, context)
    elif data == 'confirm_forward':
        await forward_music(update, context)
    elif data == 'choose_again':
        await show_genres(update.callback_query.message, context)

async def confirm_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes, forward it", callback_data='confirm_forward')],
        [InlineKeyboardButton("Choose again", callback_data='choose_again')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Confirm to forward with this genre?", reply_markup=reply_markup)

async def forward_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    music_file_id = context.user_data.get('music_file_id')
    selected_genre = context.user_data.get('selected_genre')
    genre_name = selected_genre.replace('genre_#', '')

    user = update.effective_user
    sender_name = user.full_name

    caption = f"#{genre_name}\nSender: {sender_name}"

    await context.bot.copy_message(chat_id=GROUP_CHAT_ID,
                                   from_chat_id=update.effective_chat.id,
                                   message_id=music_file_id,
                                   caption=caption)

    try:
        await query.message.delete()
    except Exception as e:
        print(f"Error deleting confirmation message: {e}")

    thank_you_text = "Thank you for reaching out, catch you later and have a nice day!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=thank_you_text)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    add_user_handler = ConversationHandler(
        entry_points=[CommandHandler('add_user', add_user_command)],
        states={
            ADD_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_user)],
        },
        fallbacks=[]
    )

    remove_user_handler = ConversationHandler(
        entry_points=[CommandHandler('remove_user', remove_user_command)],
        states={
            REMOVE_USER: [MessageHandler(filters.TEXT & ~filters.COMMAND, remove_user)],
        },
        fallbacks=[]
    )

    broadcast_handler = ConversationHandler(
        entry_points=[CommandHandler('broadcast', broadcast_command)],
        states={
            BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast)],
        },
        fallbacks=[]
    )

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("list_users", list_users_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(add_user_handler)
    application.add_handler(remove_user_handler)
    application.add_handler(broadcast_handler)
    application.add_handler(MessageHandler(filters.AUDIO, handle_music))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error occurred: {e}")
            print("Bot restarting in 10 seconds...")
            time.sleep(10)
