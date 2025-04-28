from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API key
with open('api.txt', 'r') as f:
    API_KEY = f.read().strip()

# Chapter information
chapters = {
    1: ("Installation and Setup", "https://www.youtube.com/watch?v=irqbmMNs2Bo"),
    2: ("Variables, Data types + Input/Output", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=612s"),
    3: ("Instructions & Operators", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=3114s"),
    4: ("Conditional Statements", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=7275s"),
    5: ("Loop Control Statements", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=9936s"),
    6: ("Functions & Recursion", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=13894s"),
    7: ("Pointers", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=19290s"),
    8: ("Arrays", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=22730s"),
    9: ("Strings", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=26549s"),
    10: ("Structures", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=30380s"),
    11: ("File I/O", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=33735s"),
    12: ("Dynamic Memory Allocation", "https://www.youtube.com/watch?v=irqbmMNs2Bo&t=36300s")
}

# Handle /start
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton(f"Chapter {i}: {name}", callback_data=f"chapter_{i}")]
        for i, (name, _) in chapters.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Select a chapter:', reply_markup=reply_markup)

# Handle chapter selection
def chapter_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    chapter_number = int(query.data.split('_')[1])
    chapter_name, link = chapters[chapter_number]

    context.user_data['chapter'] = chapter_number

    # Send tutorial link and ask if completed
    keyboard = [
        [
            InlineKeyboardButton("✅ Completed", callback_data="completed"),
            InlineKeyboardButton("❌ Not yet", callback_data="not_completed")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(f"Chapter {chapter_number}: {chapter_name}\n\nTutorial: {link}\n\nHave you completed it?", reply_markup=reply_markup)

# Handle after tutorial completion
def after_tutorial(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    response = query.data

    if response == "completed":
        chapter_number = context.user_data.get('chapter')
        homeworks = get_challenges_for_chapter(chapter_number)
        if homeworks:
            hw_text = '\n'.join(homeworks)
            query.message.reply_text(f"Here is your homework for Chapter {chapter_number}:\n\n{hw_text}")
        else:
            query.message.reply_text("No homework assigned for this chapter.")
    else:
        query.message.reply_text("No problem! Watch the tutorial and come back when ready.")

# Read challenges for a chapter
def get_challenges_for_chapter(chapter_number):
    challenges = []
    current_chapter = None

    with open('challenges.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('# Chapter'):
                if f'# Chapter {chapter_number}:' in line:
                    current_chapter = chapter_number
                    continue
                elif current_chapter is not None:
                    break
            elif current_chapter is not None and line:
                challenges.append(line)

    return challenges

# Main function
def main():
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(chapter_selected, pattern="^chapter_"))
    dp.add_handler(CallbackQueryHandler(after_tutorial, pattern="^(completed|not_completed)$"))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
