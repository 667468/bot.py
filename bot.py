import telebot
import os
import random
import string
import requests

token = (os.environ['BOT_TOKEN']) # Telegram botunu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin.
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help'])
def help(message):
	info = ('/randompass - Rastgele, harf ve rakamlardan oluşan, 11 haneli şifre oluşturur.\n'
		'/flipcoin - Yazı-tura atar.\n'
		'/randomcat - Rastgele kedi fotoğrafı gönderir.\n'
		)
	bot.reply_to(message, info)

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def text(message):
	if '/start' in message.text:
		welcome = ('Hoşgeldiniz! '
			'Komutlar için "/help" yazabilirsiniz!\n'
			)
		bot.reply_to(message, welcome)
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

	if '/randomcat' in message.text:
		randomcaturl = "https://api.thecatapi.com/v1/images/search?format=json"
		response = requests.get(randomcaturl)
		value_random_cat = response.json()[0]['url']
		bot.send_photo(message.chat.id, value_random_cat)
		return

bot.polling(none_stop=True, interval=0, timeout=3)