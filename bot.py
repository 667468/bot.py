import telebot
import os
import random
import string
import requests

token = (os.environ['BOT_TOKEN']) # Telegram botunu oluşturduğunuzda ki token.
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
@bot.edited_message_handler(commands=['help', 'start'])
def help(message):
	info = ('/randompass - Rastgele, harf ve rakamlardan oluşan, istenilen sayıda şifre oluşturur.\n'
		'/randomusername - Rastgele kullanıcı adı üretir.\n'
		'/randomcat - Rastgele kedi fotoğrafı gönderir.\n'
		'/randomdog - Rastgele köpek fotoğrafı gönderir.\n'
		'/flipcoin - Yazı-tura atar.'
		)
	bot.reply_to(message, info)

@bot.message_handler(commands=['randompass'])
@bot.edited_message_handler(commands=['randompass'])
def randompass(message):
	try:
		passlen = int(message.text.split(' ')[1])
		if passlen < 6:
			bot.send_message(message.chat.id, 'Güvenliğiniz için minimum 6 haneli şifre oluşturun!')
	except IndexError:
		bot.send_message(message.chat.id, 'Örnek kullanım: /randompass 9')
		return
	passgenerator = [random.choice(string.ascii_letters+string.digits) for i in range(passlen)]
	passgenerator = ("".join(passgenerator))
	bot.send_message(message.chat.id, passgenerator)

@bot.message_handler(commands=['randomusername'])
@bot.edited_message_handler(commands=['randomusername'])
def randomusername(message):
	randomusernameurl = "https://api.randomuser.me/"
	response = requests.get(randomusernameurl)
	value_random_username = response.json()['results'][0]['login']['username']
	bot.send_message(message.chat.id, value_random_username)

@bot.message_handler(commands=['randomcat'])
@bot.edited_message_handler(commands=['randomcat'])
def randomcat(message):
	randomcaturl = "https://api.thecatapi.com/v1/images/search?format=json"
	response = requests.get(randomcaturl)
	value_random_cat = response.json()[0]['url']
	bot.send_photo(message.chat.id, value_random_cat)

@bot.message_handler(commands=['randomdog'])
@bot.edited_message_handler(commands=['randomdog'])
def randomdog(message):
	randomdogurl = "https://dog.ceo/api/breeds/image/random"
	response = requests.get(randomdogurl)
	value_random_dog = response.json()['message']
	bot.send_photo(message.chat.id, value_random_dog)

@bot.message_handler(commands=['flipcoin'])
@bot.edited_message_handler(commands=['flipcoin'])
def flipcoin(message):
	liste = ['Yazı', 'Tura']
	yazitura = [random.choice(liste)]
	bot.send_message(message.chat.id, yazitura)

bot.polling(none_stop=True, interval=0, timeout=3)