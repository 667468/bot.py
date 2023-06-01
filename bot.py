import telebot, os, random, string, requests

token = (os.environ['BOT_TOKEN'])
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
@bot.edited_message_handler(commands=['help', 'start'])
def help(message):
	info = (\
		'/randompass - Rastgele istenilen uzunlukta şifre oluşturur.\n' \
		'/randomcat - Rastgele kedi fotoğrafı gönderir.\n' \
		'/randomdog - Rastgele köpek fotoğrafı gönderir.\n' \
		'/flipcoin - Yazı-tura atar.'
		)
	bot.reply_to(message, info)

@bot.message_handler(commands=['randompass'])
@bot.edited_message_handler(commands=['randompass'])
def randompass(message):
	try:
		passlen = int(message.text.split(' ')[1])
		if passlen < 12:
			bot.send_message(message.chat.id, 'Güvenliğiniz için minimum 12 karakterli şifre oluşturun!')
	except IndexError:
		bot.send_message(message.chat.id, 'Örnek kullanım: /randompass 29')
		return
	passgenerator = [random.choice(string.ascii_letters+string.digits+string.punctuation) for i in range(passlen)]
	passgenerator = ("".join(passgenerator))
	bot.send_message(message.chat.id, passgenerator)

@bot.message_handler(commands=['randomcat'])
@bot.edited_message_handler(commands=['randomcat'])
def randomcat(message):
	randomcat_url = "https://api.thecatapi.com/v1/images/search?format=json"
	response = requests.get(randomcat_url)
	value_random_cat = response.json()[0]['url']
	bot.send_photo(message.chat.id, value_random_cat)

@bot.message_handler(commands=['randomdog'])
@bot.edited_message_handler(commands=['randomdog'])
def randomdog(message):
	randomdog_url = "https://dog.ceo/api/breeds/image/random"
	response = requests.get(randomdog_url)
	value_random_dog = response.json()['message']
	bot.send_photo(message.chat.id, value_random_dog)

@bot.message_handler(commands=['flipcoin'])
@bot.edited_message_handler(commands=['flipcoin'])
def flipcoin(message):
	liste = ['Yazı', 'Tura']
	yazitura = [random.choice(liste)]
	bot.send_message(message.chat.id, yazitura)

bot.polling(none_stop=True, interval=0, timeout=3)
