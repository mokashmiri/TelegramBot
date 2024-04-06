from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

BOT_TOKEN = "token"  # Replace with your actual bot token
GROUP_CHAT_ID = -00000000
ADMIN_USER_ID = 000000  # Replace with your Telegram user ID
ALLOWED_USERS = [ADMIN_USER_ID]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    await update.message.reply_text('Hello! Send me a music file.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        return
    help_text = ("Use this bot to upload and categorize music files. Here's how you can use it:\n"
                 "If you want to get access to use the bot, you have to get your ID number from this bot, @myidbot (it contains 8 characters), and then send the number to the admin ID, @mokashmiri.\n"
                 "/start - Begin interacting with the bot.\n"
                 "/help - Display this message.\n"
                 "/about - Learn about this bot.\n"
                 "/report - Generate a usage report (admin only).")
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = ("Bot Information:\n"
                  "Version: 1.5\n"
                  "Owner: Mo Kashmiri\n"
                  "Launch Date: February 16, 2024\n"
                  "<<last update: 16 March 24>>\n"
                  "This bot helps you categorize and forward music files. Enjoy using it!")
    await update.message.reply_text(about_text)

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("You do not have access to this command.")
        return
    report_text = "Report: \n- Custom report data here."
    await update.message.reply_text(report_text)

async def delete_previous_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    last_message_id = context.user_data.get('last_message_id')
    if last_message_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=last_message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")
        finally:
            context.user_data['last_message_id'] = None

async def handle_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in ALLOWED_USERS:
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return
    
    context.user_data['music_file_id'] = update.message.message_id
    await show_genres(update.message, context)

async def show_genres(message, context: ContextTypes.DEFAULT_TYPE) -> None:
    genres = [
        "#Chill", "#Latin", "#Dance", "#HipHop", "#HIGH_TEMPO", 
        "#FA_VINTAGE", "#EN_VINTAGE", "#Birthday", "#AfterParty", 
        "#Khaltoor", "#Arabic", "#Turki", "#Pop_Chosnale", "#Indian"
    ]

    genre_buttons = [[InlineKeyboardButton(genre, callback_data=f'genre_{genre}'), InlineKeyboardButton(genres[i+1], callback_data=f'genre_{genres[i+1]}')]
                     for i, genre in enumerate(genres) if i % 2 == 0 and i < len(genres) - 1]

    # Add the last genre button if the total number is odd
    if len(genres) % 2 != 0:
        genre_buttons.append([InlineKeyboardButton(genres[-1], callback_data=f'genre_{genres[-1]}')])

    reply_markup = InlineKeyboardMarkup(genre_buttons)
    sent_message = await message.reply_text('Please choose the genre of the music:', reply_markup=reply_markup)
    context.user_data['last_message_id'] = sent_message.message_id

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith('genre_'):
        context.user_data['selected_genre'] = data
        await query.message.delete()  # Clean up by deleting the genre selection message
        await confirm_forward(update, context)  # Proceed to confirmation
    elif data == 'confirm_forward':
        await forward_music(update, context)  # Forward the music to the group
    elif data == 'choose_again':
        await show_genres(update.callback_query.message, context)  # Show genres again for re-selection

async def confirm_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Yes, forward it", callback_data='confirm_forward')],
        [InlineKeyboardButton("Choose again", callback_data='choose_again')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Here, use the query's message to reply directly to it, ensuring context is maintained
    await update.callback_query.message.reply_text("Confirm to forward with this genre?", reply_markup=reply_markup)

async def forward_music(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    music_file_id = context.user_data.get('music_file_id')
    selected_genre = context.user_data.get('selected_genre')

    # Assume selected_genre contains the prefix 'genre_', strip it out along with the hash
    # to only get the word, for example 'Latin' from 'genre_#Latin'
    genre_name = selected_genre.replace('genre_#', '')  # Remove 'genre_#' to extract just the genre name

    # Get the full name of the sender
    user = update.effective_user
    sender_name = user.full_name  # Using full_name attribute

    # Create the caption with genre in the first line, sender's name in the second
    caption = f"#{genre_name}\nSender: {sender_name}"
    
    # Forward the music file to the designated group chat
    await context.bot.copy_message(chat_id=GROUP_CHAT_ID,
                                   from_chat_id=update.effective_chat.id,
                                   message_id=music_file_id,
                                   caption=caption)

    # Delete the confirmation message
    try:
        await query.message.delete()
    except Exception as e:
        print(f"Error deleting confirmation message: {e}")

    # Send a thank-you message to the user
    thank_you_text = "Thank you for reaching out, catch you later and have a nice day!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=thank_you_text)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("report", report_command))
    application.add_handler(MessageHandler(filters.AUDIO, handle_music))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
