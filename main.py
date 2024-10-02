import os
import telebot
import random
import schedule
import time
import threading

chat_ids = set()
punctuation_marks = ['.', '?', '!', '...']
cat_emotes = ['😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']

API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)


def construct_message():

    # Body
    body = 'meow'
    body_len = random.randint(0, 3)
    body_repeated = ' '.join([body] * body_len)
    final_body = body.capitalize() + ' ' + body_repeated
    terminal_mark = random.choice(punctuation_marks)

    # Cats
    cat_n = random.randint(1, 4)
    cat = ''.join(random.choices(cat_emotes, k=cat_n))

    # Final message
    final_message = final_body.strip() + terminal_mark + ' ' + cat
    return final_message


@bot.message_handler(commands=['start', 'help'])
def greet(message):
    chat_id = message.chat.id
    chat_ids.add(chat_id)  # Store chat_id
    bot.reply_to(message, 'Meow! Meow meow meow? 😺')


@bot.message_handler(func=lambda message: True)
def chat(message):
    chat_id = message.chat.id
    chat_ids.add(chat_id)  # Store chat_id
    respopnse = construct_message()
    bot.send_message(message.chat.id, respopnse)


def notify_all():
    for chat_id in chat_ids:
        bot.send_message(chat_id, 'you havent messaged me in a while')


schedule.every(10).minutes.do(notify_all)


# Keep running the schedule in a separate thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# In another thread, the bot keeps listening to messages
threading.Thread(target=run_schedule).start()

bot.infinity_polling()
