import telebot, os, random, string, requests

token = (os.environ['BOT_TOKEN'])
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
@bot.edited_message_handler(commands=['help', 'start'])
def help(message):
	info = (\
		'/randompass - Rastgele istenilen uzunlukta şifre oluşturur.\n' \
		'/randomuser - Rastgele kullanıcı bilgileri(isim,soyisim,cinsiyet,yaş vs.) üretir.\n' \
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
		if passlen < 6:
			bot.send_message(message.chat.id, 'Güvenliğiniz için minimum 6 haneli şifre oluşturun!')
	except IndexError:
		bot.send_message(message.chat.id, 'Örnek kullanım: /randompass 9')
		return
	passgenerator = [random.choice(string.ascii_letters+string.digits) for i in range(passlen)]
	passgenerator = ("".join(passgenerator))
	bot.send_message(message.chat.id, passgenerator)

@bot.message_handler(commands=['randomuser'])
@bot.edited_message_handler(commands=['randomuser'])
def randomuser(message):
	randomuser_url = "https://uinames.com/api/?ext"
	response = requests.get(randomuser_url)
	value_randomuser_name = response.json()['name']
	value_randomuser_surname = response.json()['surname']
	value_randomuser_gender = response.json()['gender']
	if value_randomuser_gender == 'male':
		value_randomuser_gender = 'Erkek'
	else:
		value_randomuser_gender = 'Kadın'
	value_randomuser_region = response.json()['region']
	value_randomuser_age = response.json()['age']
	value_randomuser_birthday = response.json()['birthday']['dmy']
	value_randomuser_email = response.json()['email']
	generated_account = (\
		'İsim: ' + value_randomuser_name + '\n' \
		'Soyisim: ' + value_randomuser_surname + '\n' \
		'Cinsiyet: ' + value_randomuser_gender + '\n' \
		'Yaş: ' + str(value_randomuser_age) + '\n' \
		'Doğum Yeri: ' + value_randomuser_region + '\n' \
		'Doğum Tarihi: ' + str(value_randomuser_birthday) + '\n' \
		'E-mail: ' + value_randomuser_email
		)
	bot.send_message(message.chat.id, generated_account)

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