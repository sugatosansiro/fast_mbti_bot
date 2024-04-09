import os
from dotenv import load_dotenv
import logging
import requests
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, Bot
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler

load_dotenv()
bot_token = os.getenv('TOKEN')

URL = 'https://api.thecatapi.com/v1/images/search'
URL_2 = 'https://api.thedogapi.com/v1/images/search'


logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        # Печатать информацию в консоль теперь не нужно:
        # всё необходимое будет в логах
        # print(error)
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_2)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

async def new_cat(update, context):
    chat_id=update.effective_chat.id
    await context.bot.send_photo(chat_id, get_new_image())


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)  # Отправим содержимое update в консоль
    name = update.message.chat.first_name
    chat_id=update.effective_chat.id
    # Вот она, наша кнопка.
    # Обратите внимание: в класс передаётся список, вложенный в список, 
    # даже если кнопка всего одна.
    # button = ReplyKeyboardMarkup([['Показать фото котика']])
    # Каждый вложенный список определяет
    # новый ряд кнопок в интерфейсе бота.
    # Здесь описаны две кнопки в первом ряду и одна - во втором.
    # buttons = ReplyKeyboardMarkup([
    #             ['Который час?', 'Определи мой ip'],
    #             ['/random_digit']
    #         ])
    # За счёт параметра resize_keyboard=True сделаем кнопки поменьше
    # buttons = ReplyKeyboardMarkup([['/one_more_cat']], resize_keyboard=True)

    await context.bot.send_message(
        chat_id,
        text= "I'm a bot. Please check out this gorgeous fluffy I found for you, {}!".format(name),
    )

    await context.bot.send_photo(chat_id, get_new_image())
    
    buttons = ReplyKeyboardMarkup([
                ['/start_mbti_testing', '/one_more_cat']
            ], resize_keyboard=True)

    await context.bot.send_message(
        chat_id,
        text= (
            "Ice breaking session is over))"
            "Are you ready for our relaxed testing?"
            ),
        # Добавим кнопку в содержимое отправляемого сообщения
        reply_markup=buttons
    )
#//////////////////////////////////////////////////////////////////////////////////
async def start_mbti_testing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    SCORE = 0
    text= (
        'Please select which answer is closer to you\n'
        '1 -wefwef\n'
        '2 - ewfwefef\n'
        '3 - wdfwef\n'
    )
    buttons = ReplyKeyboardMarkup([
                ['1', '2', '3']
            ])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=buttons
    )
    # text_pesponse = ' '.join(context.args).upper()

    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    
    await update.message.reply_text(update.message)

#//////////////////////////////////////////////////////////////////////////////////
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.chat.first_name
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Pardon me, {}, but I didn't understand that command %)".format(name)
    )



if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    new_cat_handler = CommandHandler('one_more_cat', new_cat)
    application.add_handler(new_cat_handler)   

    start_mbti_testing_handler = CommandHandler('start_mbti_testing', start_mbti_testing)
    application.add_handler(start_mbti_testing_handler)   

    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), )
    # application.add_handler(echo_handler)
    
    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)
    
    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown) # must be the last one
    application.add_handler(unknown_handler) # must be the last one

    application.run_polling()
