import telebot
from telebot import types
import random
import logging  # Для отладки и трекинга
import os  # Для файла логов

# Настройка логирования: в консоль + файл user_log.txt
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('user_log.txt', encoding='utf-8'),  # Файл для админа
        logging.StreamHandler()  # Консоль для dev
    ]
)

# Твой токен от BotFather (замени на реальный)
TOKEN = export BOT_TOKEN=xxx
bot = telebot.TeleBot(TOKEN)

# Счетчик уникальных пользователей (в памяти; для лога)
unique_users = set()

# Главное меню (ReplyKeyboard)
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('🧠 Тестирование'))
    markup.add(types.KeyboardButton('💫 Аффирмации'))
    markup.add(types.KeyboardButton('🔥 Мотивация дня'))
    markup.add(types.KeyboardButton('ℹ️ Помощь'))
    return markup

# Подменю для тестирования (Inline)
def test_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('😰 Тест на стресс (10 вопросов)', callback_data='test_stress'))
    markup.add(types.InlineKeyboardButton('🧩 Тест на тип личности MBTI (8 вопросов)', callback_data='test_mbti'))
    markup.add(types.InlineKeyboardButton('❤️ Тест на EQ (10 вопросов)', callback_data='test_eq'))
    markup.add(types.InlineKeyboardButton('← Назад', callback_data='back_main'))
    return markup

# Подменю для аффирмаций (Inline)
def affirm_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('👨 Для мужчин', callback_data='affirm_men'))
    markup.add(types.InlineKeyboardButton('👩 Для женщин', callback_data='affirm_women'))
    markup.add(types.InlineKeyboardButton('← Назад', callback_data='back_main'))
    return markup

# Контент: Тесты (расширенные, без изменений)
STRESS_QUESTIONS = [
    ("Сколько раз вы переезжали за последний год?", ["0 раз (0)", "1 раз (20)", "2+ раза (50)"]),
    ("Были ли изменения в работе/учебе?", ["Нет (0)", "Да, небольшие (20)", "Да, значительные (40)"]),
    ("Смерть близкого родственника?", ["Нет (0)", "Да (63)"]),
    ("Развод или разрыв отношений?", ["Нет (0)", "Да (73)"]),
    ("Ссора с близким?", ["Нет (0)", "Да (35)"]),
    ("Изменения в здоровье семьи?", ["Нет (0)", "Да (44)"]),
    ("Собственные проблемы со здоровьем?", ["Нет (0)", "Да (53)"]),
    ("Финансовые потери?", ["Нет (0)", "Да (38)"]),
    ("Изменения в досуге?", ["Нет (0)", "Да (19)"]),
    ("Новое место жительства/работы?", ["Нет (0)", "Да (29)"])
]
STRESS_RESULTS = {
    (0, 149): "Низкий стресс ({score} баллов): Вы в гармонии! Поддерживайте баланс.",
    (150, 299): "Средний стресс ({score} баллов): Внимание! Попробуйте релаксацию.",
    (300, 999): "Высокий стресс ({score} баллов): Срочно! Обратитесь к специалисту."
}

MBTI_QUESTIONS = [
    ("Вы предпочитаете вечеринки или тихий вечер дома?", ["Вечеринки (E)", "Дома (I)"]),
    ("В компании вы заряжаетесь или устаете?", ["Заряжаюсь (E)", "Устаю (I)"]),
    ("Фокус на фактах или идеях?", ["Фактах (S)", "Идеях (N)"]),
    ("Планируете по деталям или видите картину целиком?", ["Деталям (S)", "Картине (N)"]),
    ("Решения по логике или эмоциям?", ["Логике (T)", "Эмоциям (F)"]),
    ("В споре важны аргументы или чувства?", ["Аргументы (T)", "Чувства (F)"]),
    ("Любите порядок или спонтанность?", ["Порядок (J)", "Спонтанность (P)"]),
    ("Дедлайны мотивируют или давят?", ["Мотивируют (J)", "Давят (P)"])
]
MBTI_RESULTS = {
    'INTJ': 'Архитектор: Стратег, независимый, visionary.',
    'INTP': 'Логик: Аналитик, изобретатель.',
    'ENTJ': 'Командир: Лидер, харизматичный.',
    'ENTP': 'Дебатер: Креативный, остроумный.',
    'INFJ': 'Адвокат: Идеалист, эмпатичный.',
    'INFP': 'Посредник: Творческий, ценит гармонию.',
    'ENFJ': 'Протагоніст: Харизматичный ментор.',
    'ENFP': 'Кампейнер: Энтузиаст, вдохновляющий.',
    'ISTJ': 'Логист: Надежный, организованный.',
    'ISFJ': 'Защитник: Заботливый, лояльный.',
    'ESTJ': 'Исполнитель: Эффективный менеджер.',
    'ESFJ': 'Консул: Социальный, поддерживающий.',
    'ISTP': 'Виртуоз: Практик, изобретатель.',
    'ISFP': 'Авантюрист: Художник, чувствительный.',
    'ESTP': 'Предприниматель: Дерзкий, энергичный.',
    'ESFP': 'Развлекатель: Жизнерадостный, спонтанный.'
}

EQ_QUESTIONS = [
    ("Вы легко распознаете эмоции других по лицу?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("В конфликте вы учитываете чувства оппонента?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Вы контролируете свои эмоции в стрессе?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Мотивируете ли себя на сложные задачи?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Понимаете ли причины своих эмоций?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Эмпатия: Чувствуете ли чужую боль?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Адаптируетесь ли к изменениям эмоционально?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("В отношениях вы открыты о чувствах?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Решите ли эмоциональные проблемы логично?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"]),
    ("Используете ли юмор для разрядки?", ["Всегда (4)", "Часто (3)", "Иногда (2)", "Редко (1)", "Никогда (0)"])
]
EQ_RESULTS = {
    (0, 14): "Низкий EQ ({score} баллов): Развивайте эмпатию через книги/курсы.",
    (15, 29): "Средний EQ ({score} баллов): Хорошо, но тренируйте контроль эмоций.",
    (30, 40): "Высокий EQ ({score} баллов): Отлично! Вы мастер отношений."
}

# Аффирмации (обновленные, без изменений)
AFFIRM_MEN = [
    "Я просыпаюсь с энергией и силой. Смотря в зеркало, я вижу лидера, готового покорять день. Я силен, уверен и достоин успеха!",
    "Утро — мой шанс начать заново. Перед зеркалом я повторяю: 'Я контролирую свою жизнь, мои действия ведут к процветанию'.",
    "Я — воин, встающий на рассвете. В зеркале отражается моя решимость: 'Препятствия — это ступеньки к вершине'.",
    "С первым лучом солнца я заявляю: 'Я достоин любви и уважения. Мои цели ясны, и я иду к ним с уверенностью'.",
    "Перед зеркалом я улыбаюсь себе: 'Сегодня я создам чудеса. Моя энергия притягивает возможности и успех'.",
    "Я просыпаюсь благодарным. В зеркале: 'Мое тело здорово, разум острый, дух непобедим'.",
    "Утро — время аффирмаций: 'Я лидер, моя воля формирует реальность. Я выбираю силу и рост'.",
    "Смотря в глаза себе, я говорю: 'Прошлое учит, настоящее — мое. Я строю будущее мечты'.",
    "Я — магнит успеха. Перед зеркалом: 'Каждый день я становлюсь богаче в опыте, финансах и отношениях'.",
    "Проснувшись, я декларирую: 'Я спокоен, фокусирован и готов к победам. Мир — мой союзник'."
]

AFFIRM_WOMEN = [
    "Я просыпаюсь в гармонии с собой. Перед зеркалом: 'Я красива, сильна и полна грации. День расцветает для меня'.",
    "Утро — ритуал любви к себе. В зеркале: 'Моя интуиция ведет, сердце открыто. Я достойна всего лучшего'.",
    "С первым светом я шепчу: 'Я — богиня, создающая свою реальность. Уверенность и радость — мои спутницы'.",
    "Перед зеркалом я утверждаю: 'Мое тело — храм, разум — мудрость, душа — свет. Я сияю изнутри'.",
    "Проснувшись, я улыбаюсь: 'Сегодня я выбираю любовь, творчество и рост. Мир отражает мою красоту'.",
    "Я — воплощение силы в мягкости. В зеркале: 'Мои мечты сбываются легко, с радостью и грацией'.",
    "Утро начинается с аффирмации: 'Я ценю себя, люблю без условий. Мои отношения гармоничны и глубокие'.",
    "Смотря на себя, я говорю: 'Энергия течет свободно. Я здорова, счастлива и успешна'.",
    "Я просыпаюсь вдохновленной: 'Моя уникальность — дар. Я делюсь ею с миром, получая в ответ изобилие'.",
    "Перед зеркалом: 'Я спокойна, центрирована и готова к чудесам. День — моя палитра для счастья'."
]

# Мотивация (без изменений)
DAILY_MOTIV = [
    "Сегодня — день, когда ты меняешь мир!", "Каждый шаг приближает к мечте.", "Твоя сила в настойчивости.",
    "Верь в себя — и горы сдвинутся.", "Маленькие победы ведут к большим.", "Ты уникален — сияй ярче!",
    "Прошлое ушло, будущее в твоих руках.", "Смейся, люби, живи на полную.", "Ты способен на большее, чем думаешь.",
    "День полон чудес — открой их.", "Твои мечты реальны — действуй!", "Сила в простоте: дыши и иди вперед.",
    "Ты — твоя лучшая версия сегодня.", "Преврати 'не могу' в 'я попробую'.", "Успех — это ты в действии.",
    "Радуйся мелочам — они создают счастье.", "Твоя энергия притягивает успех.", "Остановись, вдохни, засияй.",
    "Ты — магнит для хорошего.", "Завтра начинается сегодня."
]

GREAT_QUOTES = [
    "Верь в себя — и весь мир поверит. (Эйнштейн)", "То, что не убивает, делает сильнее. (Ницше)",
    "Успех — это движение от неудачи к неудаче без потери энтузиазма. (Черчилль)",
    "Единственный способ сделать великую работу — любить то, что ты делаешь. (Джобс)",
    "Жизнь — это то, что происходит с тобой, пока ты планируешь будущее. (Леннон)",
    "Будь собой; все остальные роли уже заняты. (Уайльд)", "Двадцать лет спустя вы будете больше разочарованы теми вещами, которые вы не делали. (Твен)",
    "Счастье не в том, чтобы делать всегда, что хочешь, а в том, чтобы всегда хотеть того, что делаешь. (Л. Толстой)",
    "Мысли формируют человека. (Будда)", "Самый большой риск — не рисковать вовсе. (Гейтс)",
    "Учись на ошибках вчерашнего дня, живи сегодняшним днем, надеяться на лучшее завтра. (Дизраэли)",
    "Ты никогда не слишком стар, чтобы поставить новую цель или мечтать новый сон. (Дисней)"
]

# Состояния пользователей
user_states = {}

def log_user_action(user, action):
    """Логируем действие пользователя"""
    username = user.username or "NoUsername"
    user_id = user.id
    unique_users.add(user_id)
    logging.info(f"USER ACTION: {username} (ID: {user_id}) - {action}")
    # Логируем общее количество уникальных
    logging.info(f"TOTAL UNIQUE USERS: {len(unique_users)}")

@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.from_user
        log_user_action(user, "START - Новый пользователь зашел")
        bot.send_message(message.chat.id, "Привет! Я ПсихоМотиватор — твой помощник в психологии и мотивации. Выбери раздел:\n\nБот разработан Марленом Рафисовичем.", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Error in start: {e}")

@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        user = message.from_user
        log_user_action(user, "HELP - Просмотр справки")
        bot.send_message(message.chat.id, "ℹ️ Справка:\n- 🧠 Тестирование: Пройди психологические тесты (теперь с 8-10 вопросами!).\n- 💫 Аффирмации: Получи позитивные установки.\n- 🔥 Мотивация: Цитата дня + мысли великих.\n\nРазработчик: Марлен Рафисович.\nНапиши /start для меню.", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Error in help: {e}")

@bot.message_handler(func=lambda message: message.text == '🧠 Тестирование')
def testing(message):
    try:
        user = message.from_user
        log_user_action(user, "MENU - Выбрал 'Тестирование'")
        bot.send_message(message.chat.id, "Выбери тест:", reply_markup=test_menu())
    except Exception as e:
        logging.error(f"Error in testing: {e}")

@bot.message_handler(func=lambda message: message.text == '💫 Аффирмации')
def affirmations(message):
    try:
        user = message.from_user
        log_user_action(user, "MENU - Выбрал 'Аффирмации'")
        bot.send_message(message.chat.id, "Выбери категорию:", reply_markup=affirm_menu())
    except Exception as e:
        logging.error(f"Error in affirmations: {e}")

@bot.message_handler(func=lambda message: message.text == '🔥 Мотивация дня')
def motivation(message):
    try:
        user = message.from_user
        log_user_action(user, "MENU - Выбрал 'Мотивация дня'")
        quote = random.choice(DAILY_MOTIV)
        great = random.choice(GREAT_QUOTES)
        text = f"🔥 Мотивация дня: {quote}\n\n💭 Мысль великого: {great}"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Обновить', callback_data='new_motiv'))
        markup.add(types.InlineKeyboardButton('← Назад', callback_data='back_main'))
        bot.send_message(message.chat.id, text, reply_markup=markup)
    except Exception as e:
        logging.error(f"Error in motivation: {e}")

@bot.message_handler(func=lambda message: message.text == 'ℹ️ Помощь')
def help_handler(message):
    user = message.from_user
    log_user_action(user, "MENU - Выбрал 'Помощь'")
    help_command(message)

# Callback для запуска теста (логируем)
@bot.callback_query_handler(func=lambda call: call.data.startswith('test_'))
def handle_test(call):
    try:
        user = call.from_user
        log_user_action(user, f"TEST START - {call.data}")
        user_id = call.message.chat.id
        test_type = call.data.split('_')[1]
        user_states[user_id] = {'test_type': test_type, 'answers': [], 'step': 0}
        questions = get_questions(test_type)
        if questions:
            bot.edit_message_text("Начинаем тест! Отвечай по кнопкам.", call.message.chat.id, call.message.message_id)
            send_question(call.message.chat.id, questions[0], user_id)
        else:
            bot.answer_callback_query(call.id, "Ошибка теста!")
    except Exception as e:
        logging.error(f"Error in handle_test: {e}")
        bot.answer_callback_query(call.id, "Ошибка! Попробуй заново.")

# Функция для вопросов (без изменений)
def get_questions(test_type):
    if test_type == 'stress':
        return STRESS_QUESTIONS
    elif test_type == 'mbti':
        return MBTI_QUESTIONS
    elif test_type == 'eq':
        return EQ_QUESTIONS
    return []

# Отправка вопроса (без изменений)
def send_question(chat_id, question, user_id):
    try:
        state = user_states[user_id]
        markup = types.InlineKeyboardMarkup(row_width=1)
        for opt in question[1]:
            if '(' in opt:
                label, value = opt.split(' (', 1)
                value = value.rstrip(')')
            else:
                label, value = opt, opt
            callback_data = f'ans_{value.replace(" ", "_")}'
            markup.add(types.InlineKeyboardButton(label, callback_data=callback_data))
        text = f"Вопрос {state['step'] + 1}: {question[0]}\nВыбери ответ:"
        bot.send_message(chat_id, text, reply_markup=markup)
    except Exception as e:
        logging.error(f"Error in send_question: {e}")

# Обработчик ответов (логируем завершение теста)
@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    try:
        user_id = call.message.chat.id
        if user_id not in user_states:
            bot.answer_callback_query(call.id, "Тест не активен. Начни заново.")
            return

        state = user_states[user_id]
        answer_value = call.data.split('_', 1)[1].replace('_', ' ')
        full_answer = next((opt for opt in get_questions(state['test_type'])[state['step']][1] if answer_value in opt), answer_value)
        state['answers'].append(full_answer)
        state['step'] += 1
        questions = get_questions(state['test_type'])

        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass

        if state['step'] < len(questions):
            send_question(call.message.chat.id, questions[state['step']], user_id)
        else:
            user = call.from_user
            log_user_action(user, f"TEST COMPLETE - {state['test_type']}")
            result = calculate_result(state)
            challenge = random.choice(['Прогуляйся 10 мин на свежем воздухе.', 'Запиши 3 цели на неделю.', 'Сделай 5 глубоких вдохов.', 'Прочитай книгу 10 страниц.'])
            bot.send_message(call.message.chat.id, f"✅ Результат: {result}\n\n🎯 Мотивационный челлендж: {challenge}", reply_markup=test_menu())
            del user_states[user_id]
    except Exception as e:
        logging.error(f"Error in handle_answer: {e}")
        bot.answer_callback_query(call.id, "Ошибка ответа! Продолжи тест.")

def calculate_result(state):
    test_type = state['test_type']
    answers = state['answers']
   
    if test_type == 'stress':
        score = sum(int(a.split('(')[1].rstrip(')')) for a in answers if '(' in a)
        for r, msg in STRESS_RESULTS.items():
            if r[0] <= score <= r[1]:
                return msg.format(score=score)
   
    elif test_type == 'mbti':
        ie_count = sum(1 for a in answers[:2] if 'E' in a)
        sn_count = sum(1 for a in answers[2:4] if 'N' in a)
        tf_count = sum(1 for a in answers[4:6] if 'F' in a)
        jp_count = sum(1 for a in answers[6:] if 'P' in a)
        typ = ''.join([
            'E' if ie_count >= 1 else 'I',
            'N' if sn_count >= 1 else 'S',
            'F' if tf_count >= 1 else 'T',
            'P' if jp_count >= 1 else 'J'
        ])
        return f"Твой тип: {typ} — {MBTI_RESULTS.get(typ, 'Неопределен')}"
   
    elif test_type == 'eq':
        score = sum(int(a.split('(')[1].rstrip(')')) for a in answers if '(' in a)
        for r, msg in EQ_RESULTS.items():
            if r[0] <= score <= r[1]:
                return msg.format(score=score)
   
    return "Тест завершен!"

# Аффирмации (логируем выбор)
@bot.callback_query_handler(func=lambda call: call.data == 'affirm_men')
def affirm_men(call):
    try:
        user = call.from_user
        log_user_action(user, "AFFIRM - Выбрал 'Для мужчин'")
        affirm = random.choice(AFFIRM_MEN)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('Ещё одну', callback_data='affirm_men'))
        markup.add(types.InlineKeyboardButton('← Назад', callback_data='back_affirm'))
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, f"💪 Аффирмация для мужчин:\n{affirm}\n\n🌅 Читай вслух перед зеркалом утром!", reply_markup=markup)
    except Exception as e:
        logging.error(f"Error in affirm_men: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'affirm_women')
def affirm_women(call):
    try:
        user = call.from_user
        log_user_action(user, "AFFIRM - Выбрал 'Для женщин'")
        affirm = random.choice(AFFIRM_WOMEN)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton('Ещё одну', callback_data='affirm_women'))
        markup.add(types.InlineKeyboardButton('← Назад', callback_data='back_affirm'))
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, f"🌸 Аффирмация для женщин:\n{affirm}\n\n🌅 Читай вслух перед зеркалом утром!", reply_markup=markup)
    except Exception as e:
        logging.error(f"Error in affirm_women: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'back_affirm')
def back_affirm(call):
    try:
        bot.edit_message_text("Выбери категорию:", call.message.chat.id, call.message.message_id, reply_markup=affirm_menu())
    except Exception as e:
        logging.error(f"Error in back_affirm: {e}")
        bot.send_message(call.message.chat.id, "Выбери категорию:", reply_markup=affirm_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'new_motiv')
def new_motiv(call):
    try:
        user = call.from_user
        log_user_action(user, "MOTIV - Обновил мотивацию")
        quote = random.choice(DAILY_MOTIV)
        great = random.choice(GREAT_QUOTES)
        text = f"🔥 Новая мотивация: {quote}\n\n💭 Мысль великого: {great}"
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, text)
    except Exception as e:
        logging.error(f"Error in new_motiv: {e}")

# Back to main
@bot.callback_query_handler(func=lambda call: call.data == 'back_main')
def back_main(call):
    try:
        user = call.from_user
        log_user_action(user, "NAV - Назад в главное меню")
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, "Главное меню:", reply_markup=main_menu())
    except Exception as e:
        logging.error(f"Error in back_main: {e}")
        bot.answer_callback_query(call.id, "Ошибка навигации! Напиши /start.")

# Запуск с увеличенным timeout
if __name__ == '__main__':
    print("Бот запускается...")
    logging.info("BOT STARTED - Сервер запущен")
    try:
        bot.polling(none_stop=True, interval=1, timeout=60)
    except Exception as e:
        logging.error(f"Polling error: {e}")
        print("Перезапуск polling через 5 сек...")
        import time
        time.sleep(5)
        bot.polling(none_stop=True, interval=1, timeout=60)