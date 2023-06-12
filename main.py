from env import TOKEN  # Импортирую токен, чтобы его никто не украл)
from aiogram import Bot, Dispatcher, executor, types  # Ссылка на бота в телеграмме -> https://t.me/Pon228723_bot
from aiogram.dispatcher.filters import Text  # Ссылка на бота http://qrcoder.ru/code/?https%3A%2F%2Ft.me%2FPon228723_bot&4&0
import time  # Импортирую время для того, чтобы человек подумал, что робот долго думает и пользователь мог прочитать, что написал бот комфортно
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="help", state="*")
async def _(message: types.Message):
    await message.answer("Для начала программы напиши /start👈😛")


@dp.message_handler(commands=["start", "back"], state="*")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Питание", "Проверить себя на наличие лишнего жира"]
    keyboard.add(*buttons)
    await message.answer(
        "Привет!\nЯ бот, который может по твоим характеристикам подобрать для тебя еду и советы, также протестировать насколько идеальная твоя фигура😎\nДля начала надо выбрать что вы хотите изучить",
        reply_markup=keyboard)
    await state.set_state("wait_answers")


@dp.message_handler(Text(equals="Проверить себя на наличие лишнего жира"), state="wait_answers")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Мужчина", "Женщина"]
    keyboard.add(*buttons)
    await message.answer("Для начала теста надо выбрать ваш пол👇", reply_markup=keyboard)
    await state.set_state("wait_gender")


@dp.message_handler(Text(equals="Мужчина"), state="wait_gender")
async def _(message: types.Message, state: FSMContext):
    await state.update_data(gender="M")
    await message.answer("Напишите ваш рост(в сантиметрах)👇")
    await state.set_state("wait_height")


@dp.message_handler(Text(equals="Женщина"), state="*")
async def _(message: types.Message, state: FSMContext):
    await state.update_data(gender="W")
    await message.answer("Напишите ваш рост(в метрах)👇")
    await state.set_state("wait_height")


@dp.message_handler(state="wait_height")
async def _(message: types.Message, state: FSMContext):
    height = int(message.text) / 100
    await state.update_data({"height": height})
    await message.answer("Напишите ваш вес(в кг)👇")
    await state.set_state("wait_weight")


@dp.message_handler(state="wait_weight")
async def _(message: types.Message, state: FSMContext):
    weight = int(message.text)
    await state.update_data({"weight": weight})
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Проверить')
    await message.answer("Нажмите на кнопку 'Проверить'👇", reply_markup=keyboard)
    await state.set_state("wait_imt_button")


@dp.message_handler(Text(equals="Проверить"), state="wait_imt_button")
async def _(message: types.Message, state: FSMContext):
    data = await state.get_data()
    weight = data['weight']
    height = data['height']

    answer = weight / (height * height)

    await message.answer(f"Ваш Индекс Массы Тела (ИМТ) равен👉{answer:.1f}")

    if answer <= 16:
        await message.answer("У вас дефицит массы тела (истощение), попробуйте побольше есть😁")
    elif answer < 16 and answer <= 18.5:
        await message.answer("У вас недостаточная масса тела (дефицит)😮")
    elif answer > 18.5 and answer <= 24.9:
        await message.answer("Норма, у вас идеальная фигура. Продолжайте в том же духе!😉")
    elif answer >= 30 and answer <= 34.9:
        await message.answer("У вас ожирение 1 степени, нужно садиться на диету😕")
    elif answer <= 35 and answer <= 39.9:
        await message.answer("У вас ожирение 2 степени, надо садиться на диету😩")
    elif answer >= 40:
        await message.answer("У вас ожирение 3 степени, срочно сидитесь на диету😱")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="wait_imt_button")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Вот ссылка для подробного изучения👇https://ria.ru/20220514/ves-1788536975.html")

    @dp.message_handler(Text(equals="Назад"), state="wait_imt_button")
    async def _(message: types.Message):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")




@dp.message_handler(Text(equals="Питание"), state="wait_answers")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Мужчины", "Женщины"]
    keyboard.add(*buttons)
    await message.answer("Для начала создания питания надо выбрать ваш пол", reply_markup=keyboard)
    await state.set_state("wait_gender_food")



@dp.message_handler(Text(equals="Мужчины"), state="wait_gender_food")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["7-12", "11-14", "14-17", "18–29", "30–44", "45–64", "65–74", "75+"]
    keyboard.add(*buttons)
    await message.answer("Выберите ваш возраст", reply_markup=keyboard)
    await state.set_state("food_age")

@dp.message_handler(Text(equals="7-12"), state="food_age")
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
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="11-14"), state="food_age")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Для детей такого возраста нужно потреблять до 2500 ккал \nНадо обязательно есть творог"
                         "\nРацион в данном случае следует сбалансировать таким образом, чтобы в нем не было большого количества жирных продуктов. Но полностью удалять из меню жирную пищу нельзя "
                         "\nНа попить можно сок, чай, воду\nВот пример:")
    time.sleep(0.5)
    await message.answer("https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-7.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="14-17"), state="food_age")
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
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="18–29"), state="food_age")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте нужно не переедать и соблюдать пропорции, отказаться от фастфуда"
                         "\nНа попить можно кофе, сок и немного минеральной воды"
                         "\nДля людей такого возраста нужно потреблять примерно 1700 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://pp.userapi.com/c846420/v846420691/153f5e/fNBV93HABbc.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https:https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="30–44"), state="food_age")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В этом возрасте нужно есть больше белка, желательно рыбу и фрукты"
                         "\nНа попить можно кофе или свежевыжатый сок"
                         "\nДля людей такого возраста нужно потреблять примерно 1650 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://ketokotleta.ru/wp-content/uploads/8/2/a/82ab4461c13ce7a0f7038bc007ffb5cc.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="45–64"), state="food_age")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте мужчинам нужно больше белка, но и слишком много его тоже не должно быть"
                         "\nНа попить лучше всего свежевыжатый сок или чай"
                         "\nДля людей такого возраста нужно потреблять примерно 1550 - 1600 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://i.pinimg.com/originals/dd/1e/85/dd1e85fbf063787be29ff7d6a146b9b4.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="65–74"), state="food_age")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("При таком возрасте происходят сдвиги обмена веществ и изменения работы внутренних органов"
                         "\nНа попить можно заварить чая с травами либо цикория"
                         "\nДля людей такого возраста нужно потреблять примерно 1450 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://montisbar.ru/wp-content/uploads/d/8/e/d8eeb8dd4c97cfefc04c64c77b97fc55.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="75+"), state="food_age")
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
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")





@dp.message_handler(Text(equals="Женщины"), state="wait_gender_food")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["7-12", "11-14", "14-17", "18–29", "30–44", "45–64", "65–74", "75+"]
    keyboard.add(*buttons)
    await message.answer("Выберите ваш возраст", reply_markup=keyboard)
    await state.set_state("food_age_w")

@dp.message_handler(Text(equals="7-12"), state="food_age_w")
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
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)
    await state.set_state("options_w")
    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="11-14"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять до 2500 ккал \nНадо бязательно есть творог "
        " рыбу и фрукты \nРацион в данном случае следует сбалансировать таким образом, чтобы в нем не было большого количества жирных продуктов. Но полностью удалять из меню жирную пищу нельзя"
        "\nНа попить можно сок, чай, воду"
        " \nВот пример:")
    time.sleep(0.5)
    await message.answer("https://quickdiets.ru/wp-content/uploads/2021/08/menyu-na-2500-kaloriy-v-den-7.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="14-17"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "Для детей такого возраста нужно потреблять примерно 2500 ккал \nНадо обязательно есть творог "
        " рыбу и фрукты \nНа попить можно сок, чай, воду"
        "\n Вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://elenaportnova.ru/wp-content/uploads/8/6/8/868e9885622c88d5418a6b18659cfe6a.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="18–30"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("В таком возрасте нужно не переедать и соблюдать пропорции"
                         "\nНа попить можно кофе, сок и немного минеральной воды"
                         "\nДля людей такого возраста нужно потреблять примерно 1400 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://arena-swim.ru/wp-content/uploads/f/6/e/f6e072957ec737199fa9e992da36fae0.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="31–45"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer("Нужно не переедать, есть фрукты и обязательно рыбу"
                         "\nНа попить можно кофе или свежевыжатый сок"
                         "\nДля людей такого возраста нужно потреблять примерно 1300 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer(
        "https://bye-bye-calories.ru/wp-content/uploads/e/2/8/e280417fb9c974ce5aaccb77cce9a827.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="45–65"), state="food_age_w")
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
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="65–75"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "При таком возрасте происходят сдвиги обменя веществ и изменения работы внутренних органов"
        "\nНа попить можно заварить чая с травами либо цикория"
        "\nДля людей такого возраста нужно потреблять примерно 1100 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://pp.userapi.com/c830400/v830400783/12286f/fAQLK4oqH80.jpg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")

@dp.message_handler(Text(equals="76+"), state="food_age_w")
async def _(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        "При физиологическом старении у здоровых пожилых людей происходят сдвиги обмена веществ и состояния органов и систем организма"
        "\nНа попить можно заварить чая с травами либо цикория"
        "\nДля людей такого возраста нужно потреблять примерно 1000 ккал, вот пример:")
    time.sleep(0.5)
    await message.answer("https://aikidzin.ru/wp-content/uploads/f/8/6/f86c5f1734bb96e9afce532375bba012.jpeg")
    time.sleep(2)
    buttons = ["Узнать поподробнее", "Назад"]
    keyboard.add(*buttons)
    await message.answer("Остались вопросы?😅", reply_markup=keyboard)

    @dp.message_handler(Text(equals="Узнать поподробнее😲"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer(
            "Вот ссылка на подробное питание для всех возрастов с подробными грамовками👇https://menunedeli.ru/2012/01/menyu-dlya-raznyx-vozrastov-na-den/")

    @dp.message_handler(Text(equals="Назад"), state="options_w")
    async def _(message: types.Message, state: FSMContext):
        time.sleep(0.5)
        await message.answer("Для того, чтобы вернуться назад, напиши👉/back")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
