import telebot
import os
import random
import string

token = (os.environ['BOT_TOKEN']) # Telegram botunu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin.
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help'])
def help(message):
	info = ('/randompass - Rastgele, rakam ve sayılardan oluşan, 11 haneli şifre oluşturur.\n'
			'/flipcoin - Yazı-tura atar.\n'
			)
	bot.send_message(message.chat.id, info)

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def text(message):
	if '/start' in message.text:
		welcome = ('Hoşgeldiniz! '
				   'Komutlar için "/help" yazabilirsiniz!\n'
				  )
		bot.send_message(message.chat.id, welcome)
		return

	if '/randompass' in message.text:
		passlen = 11 #TODO: İstenilen sayıya göre ayarla!
		passgenerator = [random.choice(string.ascii_letters+string.digits) for i in range(passlen)]
		passgenerator = ("".join(passgenerator))
		bot.send_message(message.chat.id, passgenerator)
		return

	if '/flipcoin' in message.text:
		liste = ['yazı', 'tura']
		yazitura = [random.choice(liste)]
		bot.send_message(message.chat.id, yazitura)
		return

bot.polling(none_stop=True, interval=0, timeout=3)