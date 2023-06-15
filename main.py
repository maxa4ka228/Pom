from env import TOKEN  # Импортирую токен, чтобы его никто не украл)
from aiogram import Bot, Dispatcher, executor, types  # Ссылка на бота в телеграмме -> https://t.me/Pon228723_bot
from aiogram.dispatcher.filters import Text  # Ссылка на бота в ввиде QR-кода -> http://qrcoder.ru/code/?https%3A%2F%2Ft.me%2FPon228723_bot&4&0
import time  # Импортирую время для того, чтобы пользователь мог прочитать, что написал бот комфортно
from aiogram.dispatcher import FSMContext #Для перехода между async def
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands="help", state="*")# Команда помощи
async def _(message: types.Message):
    await message.answer("Для начала программы напиши /start👈😛")


@dp.message_handler(commands=["start", "back"], state="*")# Начало програмы
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Питание", "Проверить себя на наличие лишнего веса"]
    keyboard.add(*buttons)
    await message.answer(
        "Привет!\nЯ бот, который может по твоим характеристикам подобрать для тебя рацион питания и дать советы, также протестировать насколько идеальная твоя фигура😎"
        "\nДля начала надо выбрать что вы хотите изучить",
        reply_markup=keyboard)
    await state.set_state("wait_answers")


@dp.message_handler(Text(equals="Проверить себя на наличие лишнего веса"), state="wait_answers")# Программа для проверки лишнего веса
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Мужчина", "Женщина"]
    keyboard.add(*buttons)
    await message.answer("Для начала теста надо выбрать ваш пол👇", reply_markup=keyboard)
    await state.set_state("wait_gender")


@dp.message_handler(Text(equals="Мужчина"), state="wait_gender")# Если мужчина, задаём вопрос о росте
async def _(message: types.Message, state: FSMContext):
    await state.update_data(gender="M")
    await message.answer("Напишите ваш рост(в сантиметрах)👇")
    await state.set_state("wait_height")


@dp.message_handler(Text(equals="Женщина"), state="*")# Если женщина, задаём вопрос о росте
async def _(message: types.Message, state: FSMContext):
    await state.update_data(gender="W")
    await message.answer("Напишите ваш рост(в сантиметрах)👇")
    await state.set_state("wait_height")


@dp.message_handler(state="wait_height")# Получаем рост и задаём вопрос о весе
async def _(message: types.Message, state: FSMContext):
    height = int(message.text) / 100
    await state.update_data({"height": height})
    await message.answer("Напишите ваш вес(в кг)👇")
    await state.set_state("wait_weight")


@dp.message_handler(state="wait_weight")# Получаем вес пользователя
async def _(message: types.Message, state: FSMContext):
    weight = int(message.text)
    await state.update_data({"weight": weight})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Проверить')
    await message.answer("Нажмите на кнопку 'Проверить'👇", reply_markup=keyboard)
    await state.set_state("wait_imt_button")


@dp.message_handler(Text(equals="Проверить"), state="wait_imt_button")# Процесс нахождения ИМТ и вывод
async def _(message: types.Message, state: FSMContext):
    data = await state.get_data()
    weight = data['weight']
    height = data['height']

    answer = weight / (height * height)# Формула выведения ИМТ

    await message.answer(f"Ваш Индекс Массы Тела (ИМТ) равен👉{answer:.1f}")

    if answer <= 16:
        await message.answer("У вас дефицит массы тела (истощение), в честь этого вы получаете курицу, только не кушайте её всю сразу😯")
        time.sleep(0.5)
        await message.answer("https://recfood.ru/wp-content/uploads/2019/04/ku11-scaled-e1580476964188.jpg")
    elif 16 < answer <= 18.5:
        await message.answer("У вас недостаточная масса тела (дефицит), в честь этого вы получаете рыбу, вам нужно кушать больше😮")
        time.sleep(0.5)
        await message.answer("https://goodsovet.ru/wp-content/uploads/2022/10/kak-prigotovit-forel-scaled-e1665825123950.jpg")
    elif 18.5 < answer <= 24.9:
        await message.answer("Норма, у вас идеальная фигура, в честь этого вы получаете кубок за идеальную фигуру! Продолжайте в том же духе!😉")
        time.sleep(0.5)
        await message.answer("https://www.eltis.org/sites/default/files/news/shutterstock_238134754.jpg")
    elif 25 < answer <= 29.9:
        await message.answer("У вас нормальная фигура, в честь этого вы получаете медальку. Продолжайте в том же духе!😉")
        time.sleep(0.5)
        await message.answer("https://cdn4.iconfinder.com/data/icons/modern-education-1/128/24-1024.png")
    elif 30 <= answer <= 34.9:
        await message.answer("У вас ожирение 1 степени, поэтому вы получаете тарелку фруктов, нужно садиться на диету😕")
        time.sleep(0.5)
        await message.answer("https://klike.net/uploads/posts/2022-09/1662369606_j-23.jpg")
    elif 35 <= answer <= 39.9:
        await message.answer("У вас ожирение 2 степени, поэтому вы получаете салат, надо садиться на диету😩")
        time.sleep(0.5)
        await message.answer("https://salatikdoma.ru/wp-content/uploads/2017/05/%D1%81%D0%B0%D0%BB%D0%B0%D1%82-%D0%B8%D0%B7-%D1%81%D0%B0%D0%BB%D0%B0%D1%82%D0%B0.jpg")
    elif answer >= 40:
        await message.answer("У вас ожирение 3 степени, поэтому вы получаете полезный пучок салата, срочно садитесь на диету😱")
        time.sleep(0.5)
        await message.answer("https://здоровое-питание.рф/upload/iblock/d25/3nd9fpw2uc28nbdzno7nev3493j7ftp7/salat-s-tuntsom-2.jpg")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее"), state="wait_imt_button")# Если пользователь хочет узнать больше
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Вот ссылка для подробного изучения👇https://ria.ru/20220514/ves-1788536975.html")# Выводим ссылку


    @dp.message_handler(Text(equals="Начало"), state="wait_imt_button")# Если пользователь хочет в начало программы
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")




@dp.message_handler(Text(equals="Питание"), state="wait_answers")# Если пользователь выбрал 'Питание'
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Мужчины", "Женщины"]
    keyboard.add(*buttons)
    await message.answer("Для начала создания питания надо выбрать ваш пол", reply_markup=keyboard)
    await state.set_state("wait_gender_food")




@dp.message_handler(Text(equals="Мужчины"), state="wait_gender_food")# Если мужчина задаём вопрос о возрасте
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["7-11", "12-14", "15-17", "18–29", "30–44", "45–64", "65–74", "75+"]
    keyboard.add(*buttons)
    await message.answer("Выберите ваш возраст", reply_markup=keyboard)
    await state.set_state("food_age")

@dp.message_handler(Text(equals="7-11"), state="food_age")# Если пользователю 7-12 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Это время развития организма, надо чательно подбирать продукты и балансировать жиры\n"
                         "Для детей такого возраста нужно потреблять примерно 2300 ккал \nНадо бязательно употреблять такую еду, как творог "
                         ", рыба, фрукты\n"
                         "На попить можно сок или воду \nВот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://sun9-14.userapi.com/impg/q60LYGKIrm4L_f1ZLTCOnt_ALruVDIuw0LL4Aw/BPtXmtmf_1k.jpg?size=604x604&quality=96&sign=51aad660d493252582c96e23bde9c0e5&c_uniq_tag=ZR_OIMTTx8ZVzKbfNwR062PhOGR7rj4fmUy-D6Lotlo&type=album")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="12-14"), state="food_age")# Если пользователю 12-14 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Для детей такого возраста нужно потреблять до 2500 ккал \nНадо обязательно есть творог"
                         "\nРацион в данном случае следует сбалансировать таким образом, чтобы в нем не было большого количества жирных продуктов. Но полностью удалять из меню жирную пищу нельзя "
                         "\nНа попить можно сок, чай, воду\nВот пример:")
    time.sleep(0.5)
    await message.answer("https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-5.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="15-17"), state="food_age")# Если пользователю 15-17 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять примерно 2500 ккал \nНадо бязательно есть творог "
        " рыбу и фрукты "
        "\nНа попить можно сок, чай, воду"
        "\nВот пример:")
    time.sleep(0.5)
    await message.answer("https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-7.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="18–29"), state="food_age")# Если пользователю 18-29 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте нужно не переедать и соблюдать пропорции, отказаться от фастфуда"
                         "\nНа попить можно кофе, сок и немного минеральной воды"
                         "\nДля людей такого возраста нужно потреблять примерно 1700 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://pp.userapi.com/c846420/v846420691/153f5e/fNBV93HABbc.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https:https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="30–44"), state="food_age")# Если пользователю 30-44 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В этом возрасте нужно есть больше белка, желательно рыбу и фрукты"
                         "\nНа попить можно кофе или свежевыжатый сок"
                         "\nДля людей такого возраста нужно потреблять примерно 1650 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://ketokotleta.ru/wp-content/uploads/8/2/a/82ab4461c13ce7a0f7038bc007ffb5cc.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="45–64"), state="food_age")# Если пользователю 45-64 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте мужчинам нужно больше белка, но и слишком много его тоже не должно быть"
                         "\nНа попить лучше всего свежевыжатый сок или чай"
                         "\nДля людей такого возраста нужно потреблять примерно 1550 - 1600 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://i.pinimg.com/originals/dd/1e/85/dd1e85fbf063787be29ff7d6a146b9b4.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="65–74"), state="food_age")# Если пользователю 65-74 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("При таком возрасте происходят сдвиги обмена веществ и изменения работы внутренних органов"
                         "\nНа попить можно заварить чая с травами либо цикория"
                         "\nДля людей такого возраста нужно потреблять примерно 1450 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://montisbar.ru/wp-content/uploads/d/8/e/d8eeb8dd4c97cfefc04c64c77b97fc55.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="75+"), state="food_age")# Если пользователю 75+ лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "При физиологическом старении у здоровых пожилых людей происходят сдвиги обмена веществ и состояния органов и систем организма"
        "\nНа попить можно заварить чая с травами либо цикория"
        "\nДля людей такого возраста нужно потреблять примерно 1350 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://privately.ru/sport-diety/uploads/posts/2020-08/enju-c-podschetom-kalopij-na-vsju-nedelju-fitnes-podruga-6.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")





@dp.message_handler(Text(equals="Женщины"), state="wait_gender_food")# Если женщина, задаём вопрос о возрасте
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["7-11", "12-14", "15-17", "18–29", "30–44", "45–64", "65–74", "75+"]
    keyboard.add(*buttons)
    await message.answer("Выберите ваш возраст", reply_markup=keyboard)
    await state.set_state("food_age_w")

@dp.message_handler(Text(equals="7-11"), state="food_age_w")# Если пользователю 7-11 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять примерно 2300 ккал \nНадо бязательно употреблять такую еду, как творог "
        ", рыба, фрукты , так как организм растущий надо есть больше"
        "\nНа попить можно сок или воду"
        "\nВот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://sun9-14.userapi.com/impg/q60LYGKIrm4L_f1ZLTCOnt_ALruVDIuw0LL4Aw/BPtXmtmf_1k.jpg?size=604x604&quality=96&sign=51aad660d493252582c96e23bde9c0e5&c_uniq_tag=ZR_OIMTTx8ZVzKbfNwR062PhOGR7rj4fmUy-D6Lotlo&type=album")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="12-14"), state="food_age_w")# Если пользователю 12-14 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять до 2500 ккал \nНадо бязательно есть творог "
        " рыбу и фрукты \nРацион в данном случае следует сбалансировать таким образом, чтобы в нем не было большого количества жирных продуктов. Но полностью удалять из меню жирную пищу нельзя"
        "\nНа попить можно сок, чай, воду"
        " \nВот пример:")
    time.sleep(0.5)
    await message.answer("https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-5.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="15-17"), state="food_age_w")# Если пользователю 15-17 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять примерно 2500 ккал \nНадо обязательно есть творог "
        " рыбу и фрукты \nНа попить можно сок, чай, воду"
        "\n Вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-7.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="18–29"), state="food_age_w")# Если пользователю 18-29 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте нужно не переедать и соблюдать пропорции"
                         "\nНа попить можно кофе, сок и немного минеральной воды"
                         "\nДля людей такого возраста нужно потреблять примерно 1400 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://arena-swim.ru/wp-content/uploads/f/6/e/f6e072957ec737199fa9e992da36fae0.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="30–44"), state="food_age_w")# Если пользователю 30-44 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Нужно не переедать, есть фрукты и обязательно рыбу"
                         "\nНа попить можно кофе или свежевыжатый сок"
                         "\nДля людей такого возраста нужно потреблять примерно 1300 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://bye-bye-calories.ru/wp-content/uploads/e/2/8/e280417fb9c974ce5aaccb77cce9a827.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="45–64"), state="food_age_w")# Если пользователю 45-64 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для поддержания красоты и молодости в женском огранизме, требуется есть больше рыбы или рыбьего жира"
        "\nНа попить лучше всего свежевыжатый сок или чай"
        "\nДля людей такого возраста нужно потреблять примерно 1200 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://sun6-23.userapi.com/impg/RxYcwHINTeMGaDl3Vd7pIyfQPT46b30Vzw0OJg/muzGEUkKuog.jpg?size=1080x1080&quality=95&sign=c214f09c821e64ce4fbe1ef6048ab828&c_uniq_tag=mmfTmJHJJHkug5sLtk6TpgWzxxcidJZqNiGfJegAEZk&type=album")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="65–74"), state="food_age_w")# Если пользователю 65-74 лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "При таком возрасте происходят сдвиги обменя веществ и изменения работы внутренних органов"
        "\nНа попить можно заварить чая с травами либо цикория"
        "\nДля людей такого возраста нужно потреблять примерно 1100 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://pp.userapi.com/c830400/v830400783/12286f/fAQLK4oqH80.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")

@dp.message_handler(Text(equals="75+"), state="food_age_w")# Если пользователю 75+ лет
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "При физиологическом старении у здоровых пожилых людей происходят сдвиги обмена веществ и состояния органов и систем организма"
        "\nНа попить можно заварить чая с травами либо цикория"
        "\nДля людей такого возраста нужно потреблять примерно 1000 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://aikidzin.ru/wp-content/uploads/f/8/6/f86c5f1734bb96e9afce532375bba012.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Начало"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Начало"), state="options_w")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться в начало, напиши👉/back")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
