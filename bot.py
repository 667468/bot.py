import telebot

token = (os.environ['BOT_TOKEN']) # Discord botu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin.
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help'])
def help(message):
	bot.reply_to(message, 'WIP!')

@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def text(message):
	if '/start' in message.text:
		bot.reply_to(message, 'Hoşgeldiniz! "/help"')
		return
	bot.reply_to(message, 'Komutlar için "/help" yazabilirsiniz!')

bot.polling()
