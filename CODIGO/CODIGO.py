import os
import logging
import telebot
from rembg import remove
from TOKEN import TOKEN  

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Olá! Envie uma imagem e eu vou remover o fundo para você.')

@bot.message_handler(content_types=['photo'])
def process_image(message):
    try:
        bot.send_chat_action(message.chat.id, "upload_photo")
        file_info = bot.get_file(message.photo[-1].file_id)
        file_path = bot.download_file(file_info.file_path)
        input_path = 'input_image.png'
        with open(input_path, 'wb') as input_file:
            input_file.write(file_path)
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)
        output_path = 'output_image.png'
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        with open(output_path, 'rb') as output_file:
            bot.send_photo(message.chat.id, output_file)
        os.remove(input_path)
        os.remove(output_path)
    except Exception as e:
        logger.error(f'Erro ao processar a imagem: {e}')
        bot.reply_to(message, 'Desculpe, ocorreu um erro ao processar a imagem.')

bot.polling()
