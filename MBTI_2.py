"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
from dotenv import load_dotenv
import logging
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO,
    filename='main.log',
    filemode='w'
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
bot_token = os.getenv('TOKEN')

EXTRAVERT_INTROVERT, SENSORY_INTUITIVE, THINKER_FEELER, JUDGER_PERCEIVER = range(4)
E_I, S_N, T_F, J_P, MBTI = range(5)
URL = 'https://api.thecatapi.com/v1/images/search'
URL_2 = 'https://api.thedogapi.com/v1/images/search'

def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(URL_2)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

async def new_cat(update, context):
    chat_id=update.effective_chat.id
    await context.bot.send_photo(chat_id, get_new_image())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their extravertion /introvertion."""
    print(update)
    name = update.message.chat.first_name
    chat_id=update.effective_chat.id
    reply_keyboard = [['1', '2', '3','4']]

    await context.bot.send_message(
        chat_id,
        text=(
            'Здравствуйте! Этот экспресс-тест по методике MBTI поможет Вам немного изучить себя.\n'
            'Пока готовитесь к тесту, посмотрите какие замечательные пушистики, {}!'.format(name))
    )

    await context.bot.send_photo(chat_id, get_new_image())

    await update.message.reply_text(
        'Начнём... или еще пушистика /one_more_cat ))?\n'
        'При ответах на вопросы здесь постарайтесь зафиксировать сразу ответ, который первым приходит Вам на ум)\n'
        'Итак, какой способ отдыха наилучшим образом позволит Вам отдохнуть, восстановить силы после эмоциональной нагрузки ?\n'
        'Выберите номер ответа который Вам ближе всего:\n\n'
        '1 - Погулять в одиночестве на природе, побродить по городу.\n'
        '2 - Лучше всего помогает физическая нагрузка.\n'
        '3 - Общение с друзьями.\n'
        '4 - Отправлюсь на вечеринку, в бар или на какое-то общественное мероприятие.\n\n'
        'Да, кстати, ты в любой момент можешь прекратить тестирование командой /cancel.\n\n'
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Как отдохнём?"
        ),
    )
    return EXTRAVERT_INTROVERT


async def extravert_introvert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected extravert_introvert and asks for a sensory_intuitive."""
    global E_I
    user = update.message.from_user
    user_response = update.message.text
    if user_response in ('1','2'):
        E_I = 'I'
    else:
        E_I = 'E'
    print(E_I)
    logger.info("extravertion/introvertion of %s: %s", user.first_name, E_I)
    reply_keyboard = [['1','2','3','4']]
    await update.message.reply_text(
        'Следующий вопрос - что в перую очередь Вам приходит на ум, когда слышите слово "роза" ?\n'
        'Снова, выберите номер ответа который Вам ближе всего:\n\n'
        '1 - Красный цвет, шипы, лепестки.\n'
        '2 - Любовь, красота, ну или может быть, наоборот, пошлость.\n'
        '3 - Женское имя.\n'
        '4 - О, точно же, скоро 8 марта/Свидание/День рождения/, надо подкопить деньжат)\n'
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Как познаем мир?"
        ),
    )

    return SENSORY_INTUITIVE

async def sensory_intuitive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected sensory_intuitive and asks for thinker_feeler."""
    global S_N
    user = update.message.from_user
    if update.message.text in '1':
        S_N = 'S'
    else:
        S_N = 'N'
    print(S_N)
    logger.info("sensory_intuitive of %s: %s", user.first_name, S_N)
    reply_keyboard = [['1','2','3']]
    await update.message.reply_text(
        'Вопрос № 3. Ситуация: Земле грозит скорая гибель!\n'
        'Вам, и только Вам, доверено право набрать команду последних 20 людей,\n'
        'которые выживут и полетят к далёкой планете, пригодной для жизни.\n'
        'Снова, выберите номер ответа который Вам ближе всего:\n\n'
        '1 - Возьму с собой свою семью, любимых людей, близких друзей в первую очередь.\n\n'
        '2 - Нужно взять самых полезных для этой миссии людей - молодых: инженеров, биологов, врачей, математиков, военных, психологов, строителей. Пополам: юноши и девушки.\n\n'
        '3 - Возьму с собой 10 самых привлекательных предстваителей противоположного пола разных рас ... ну и в морозильнике генофонд планеты + инструкции как все это потом налаживать + 9 роботов-помощников.\n'
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True, input_field_placeholder="Как принимаем решения?"
        ),
    )
    return THINKER_FEELER


async def thinker_feeler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the thinker_feeler and asks for judger_perceiver."""
    global T_F
    user = update.message.from_user
    if update.message.text in '1':
        T_F = 'F'
    else:
        T_F = 'T'
    print(T_F)
    logger.info("thinker/feeler of %s: %s", user.first_name, T_F)
    reply_keyboard = [['1','2','3']]
    await update.message.reply_text(
        'Заключительный вопрос. И снова ситуация))\n'
        'Впереди Ваш долгожданный отпуск - как Вы будете к нему готовиться?\n'
        'Снова, выберите номер ответа который Вам ближе всего:\n\n'
        '1 - Планирование отпуска - это особое удовольствие! Детально распланирую все активности наперед.\n\n'
        '2 - Поеду точно не в одиночку. Нужно собраться вместе и обсудить наши планы, может кто-то предложит что-то интересное?\n\n'
        '3 - Не вижу смысла все планировать заранее, приеду и разбирусь на месте, по обстоятельствам)\n'
        ,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True,  input_field_placeholder="Как организовываем мир вокруг себя?"
        ),
    )
    return JUDGER_PERCEIVER


async def judger_perceiver(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about judger_perceiver response and ends the conversation."""
    global J_P
    global MBTI
    user = update.message.from_user
    if update.message.text in '1':
        J_P = 'J'
    else:
        J_P = 'P'
    print(J_P) 
    logger.info("judger_perceiver of %s: %s", user.first_name, J_P)
    MBTI = E_I + S_N + T_F + J_P
    logger.info("Overall result of %s: %s", user.first_name, MBTI)
    
    await update.message.reply_text(
        'Поздравляю с успешным прохождением теста!\n'
        'Да, безусловно, этот тест был очень упрощенным)\n'
        'Также Вы могли быть не в настроении отвечать на такие вопросы сегодня)\n'
        f'Но веcьма вероятно, что Ваш тип личности - {MBTI} - и это прекрасно! \n\n'
        'Кстати, если вдруг у Вас есть какие-либо вопросы или, не дай бог, тревоги - Вы всегда их можешь обсудить с проверенным психологом.\n'
        'Вот ссылка -  https://t.me/svetlana_vishnyakova_psy'
    )
    await update.message.reply_text(
        'Я уверен, что Вы на правильном пути, раз хотите узнать себя еще лучше.\n'
        'Попробуйте найти больше информации в интернете о методике MBTI, а может и каких-либо других)\n'
        'Успехов Вам в познании себя! Уверен, у Вас все получиться!',
    )
    user_response = update.message.text
    print(user_response)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Успехов Вам в познании себя! Уверен, у Вас все получиться!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).build()

    # Add conversation handler with the states EXTRAVERT_INTROVERT, SENSORY_INTUITIVE, THINKER_FEELER and JUDGER_PERCEIVER
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EXTRAVERT_INTROVERT: [MessageHandler(filters.Regex("^(1|2|3|4)$"), extravert_introvert)],
            SENSORY_INTUITIVE: [MessageHandler(filters.Regex("^(1|2|3|4)$"), sensory_intuitive)],
            THINKER_FEELER: [MessageHandler(filters.Regex("^(1|2|3|4)$"), thinker_feeler)],
            JUDGER_PERCEIVER: [MessageHandler(filters.Regex("^(1|2|3|4)$"), judger_perceiver)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    new_cat_handler = CommandHandler('one_more_cat', new_cat)
    application.add_handler(new_cat_handler)
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()