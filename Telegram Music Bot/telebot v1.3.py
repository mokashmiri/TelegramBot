from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

BOT_TOKEN = "token"
GROUP_CHAT_ID = -000000000
ADMIN_USER_ID = 11111111111111
ALLOWED_USERS = [ADMIN_USER_ID]  



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    await update.message.reply_text('Hello! Send me a music file.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        return
    help_text = "Use this bot to upload and categorize music files. Here's how you can use it:\n"
    help_text += "If you want to get access to use the bot, you have to get your ID number from this bot, @myidbot (it contains 8 characters), and then send the number to the admin ID, @mokashmiri.\n"
    help_text += "/start - Begin interacting with the bot.\n"
    help_text += "/help - Display this message.\n"
    help_text += "/about - Learn about this bot.\n"
    help_text += "/report - Generate a usage report (admin only)."
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = "Bot Information:\n"
    about_text += "Version: 1.3\n"
    about_text += "Owner: Mo kashmiri\n"
    about_text += "Launch Date: February 16, 2024\n"
    about_text += "This bot helps you categorize and forward music files. Enjoy using it!"
    await update.message.reply_text(about_text)

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have access to this command.")
        return
    report_text = "Report: \n- Custom report data here."
    await update.message.reply_text(report_text)

async def handle_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    
    # Your existing logic for handling music uploads
    context.user_data['music_file_id'] = update.message.message_id
    keyboard = [
        [InlineKeyboardButton("#Chill", callback_data='genre_#Chill')],
        [InlineKeyboardButton("#Latin", callback_data='genre_#Latin')],
        [InlineKeyboardButton("#Indian", callback_data='genre_#Indian')],
        [InlineKeyboardButton("#HIGH_TEMPO", callback_data='genre_#HIGH_TEMPO')],
        [InlineKeyboardButton("#FA_VINTAGE", callback_data='genre_#FA_VINTAGE')],
        [InlineKeyboardButton("#EN_VINTAGE", callback_data='genre_#EN_VINTAGE')],
        [InlineKeyboardButton("#HipHop", callback_data='genre_#HipHop')],
        [InlineKeyboardButton("#Birthday", callback_data='genre_#Birthday')],
        [InlineKeyboardButton("#AfterParty", callback_data='genre_#AfterParty')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose the genre of the music:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if update.effective_user.id not in ALLOWED_USERS:
        await query.edit_message_text(text="Sorry, you do not have permission to use this feature.")
        return

    if data.startswith('genre_'):
        context.user_data['selected_genre'] = data
        await confirm_forward(update, context)
    elif data == 'confirm_forward':
        await forward_music(update, context)
    elif data == 'add_another':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm waiting for the next one :)")
    elif data == 'done':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Catch you later. Thanks for using me!")

async def confirm_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes, forward it", callback_data='confirm_forward')],
        [InlineKeyboardButton("Choose again", callback_data='choose_again')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Confirm to forward with this genre?", reply_markup=reply_markup)

async def forward_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    music_file_id = context.user_data.get('music_file_id')
    selected_genre = context.user_data.get('selected_genre').replace('genre_', '')
    user = update.effective_user
    sender_name = user.first_name + (" " + user.last_name if user.last_name else "")
    caption = f"{selected_genre}\nSender: {sender_name}"
    await context.bot.copy_message(chat_id=GROUP_CHAT_ID,
                                   from_chat_id=update.effective_chat.id,
                                   message_id=music_file_id,
                                   caption=caption)
    await ask_user_next_step(update, context)

async def ask_user_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes, add another one", callback_data='add_another')],
        [InlineKeyboardButton("No, I'm done", callback_data='done')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Do you want to continue or are you done with this?", reply_markup=reply_markup)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(MessageHandler(filters.AUDIO, handle_music))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
