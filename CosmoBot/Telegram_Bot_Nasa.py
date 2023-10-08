import telebot
from telebot import types
import openai
from datetime import datetime
import requests

bot = telebot.TeleBot('Your_Telegram_API')

NASA_API_ENDPOINT = "https://api.nasa.gov/planetary/apod"
NASA_API_KEY = "Your_Nasa_API"

bot.remove_webhook()

chatStr = ''

def ChatModel(prompt):
    global chatStr 
    openai.api_key ='Your_Openai_API'
    chatStr += f"Death:{prompt}\nJravis: "
    
    response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=chatStr,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
    chatStr += f"{response.choices[0].text}"
    return response.choices[0].text
    
def ChatModel(prompt):
    global chatStr 
    openai.api_key = 'Your_Openai_API'
    chatStr += f"Death:{prompt}\nJravis: "
    
    response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=chatStr,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
    
    chatStr += f"{response.choices[0].text}"
    
    response_text = f"{response.choices[0].text}\n\n#SpaceApps #spaceappskz"
    return response_text


CURRENT_STATE = {}  # To keep track of the user's current interaction


def get_apod(date=None):
    """Fetch the Astronomy Picture of the Day."""
    params = {"api_key": NASA_API_KEY}
    if date:
        params["date"] = date

    response = requests.get(NASA_API_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    item1 = types.KeyboardButton("Astronomy Photo of the Day")
    item2 = types.KeyboardButton("Ask about NASA, Astronomy, Astrophysics")
    item3 = types.KeyboardButton("Volunteering program")
    markup.add(item1, item2,item3)

    bot.send_message(message.chat.id, 'Hello, My name Is CosmoBot. What would you like to know?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Astronomy Photo of the Day")
def photo_of_the_day(message):
    CURRENT_STATE[message.chat.id] = "AWAITING_DATE"
    bot.reply_to(message, "Please provide a date (YYYY-MM-DD) or type 'today' for the current date's photo.")


@bot.message_handler(func=lambda message: message.text == "Ask about NASA, Astronomy, Astrophysics")
def ask_nasa(message):
    CURRENT_STATE[message.chat.id] = "NASA_QUESTION"
    bot.reply_to(message, "What information do you need?")
  
  

@bot.message_handler(func=lambda message: message.text == "Volunteering program")
def ask_nasa(message):
    CURRENT_STATE[message.chat.id] = "NASA_QUESTION"
    bot.reply_to(message, "Which volunteering program do you want to choose?")
    markup1 = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    item1 = types.KeyboardButton("Software engineering")
    item2 = types.KeyboardButton("Scientistic")
    item3 = types.KeyboardButton("For everyone")
    
    markup1.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Choose a program:", reply_markup=markup1)

@bot.message_handler(func=lambda message: message.text in ["Software engineering", "Scientistic", "For everyone", "Advantage of volunteering"])
def handle_volunteering_options(message):
    if message.text == "Software engineering":
        response = ("Software engineering is like an open source project where "
                    "you can add your recommendations and solutions for code.")
    elif message.text == "Scientistic":
        response = ("Scientistic means you can use data from us and NASA for "
                    "your projects.")
    elif message.text == "For everyone":
        response = ("For everyone includes educational programs, videos, content, "
                    "and storytelling.")

    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: CURRENT_STATE.get(message.chat.id) == "AWAITING_DATE")
def handle_date(message):
    date_str = message.text
    if date_str == "today":
        date_str = None
    apod_data = get_apod(date_str)
    if apod_data:
        bot.send_message(message.chat.id, f"Title: {apod_data['title']}\n\n{apod_data['explanation']}")
        bot.send_photo(message.chat.id, apod_data['url']) 
        del CURRENT_STATE[message.chat.id] 
    else:
        bot.reply_to(message, "Sorry, couldn't fetch the Astronomy Picture of the Day. Please try again later.")


@bot.message_handler(func=lambda message: CURRENT_STATE.get(message.chat.id) == "NASA_QUESTION")
def handle_nasa_question(message):
    try:
        reply = ChatModel(message.text)
        bot.reply_to(message, reply)
        del CURRENT_STATE[message.chat.id]
    except Exception as e:
        bot.reply_to(message, str(e))


def chat(message):
    print(message.text)
    try:
        reply = ChatModel(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        print(e)
        bot.reply_to(message, str(e))


print('Bot started')    
bot.polling()
