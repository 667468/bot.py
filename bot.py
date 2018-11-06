from discord.ext.commands import Bot
from discord import Game
import os
import requests

bot_prefix = ("!!", "??") # Bunu kendi isteğinize göre değiştirebilirsiniz. Botun komutu algılaması için, komutun başında bu iki prefixte biri olması gerekli. Örneğin; !!doviz, ??doviz gibi...
token = (os.environ['BOT_TOKEN']) # Discord botu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin.
bot = Bot(command_prefix=bot_prefix)

@bot.event
# TODO: Türkçeleştirilebilir ama böyle de güzel
async def on_ready():
 print("BOT: Logged as: {}".format(bot.user.name))
 print("BOT: ID: {}".format(bot.user.id))
 print("BOT: Joined {}".format(str(len(bot.servers))) + " server/s!")
 await bot.change_presence(game=Game(name='Komutlar için "!!help" yazabilirsiniz!'))

# TODO: Türkçe bir komut ismi bulunca, değiştir.
@bot.command(name='whoareu',
	description="Botun hakkında bilgi verir.",
	aliases=['??whoareu'],
	pass_context=True)
async def whoareu(ctx):
 await bot.say("Ben Fatih Ünsever tarafından yazılmış bir Discord uygulaması botuyum!")

# Güncel döviz kurlarını gösterir.
@bot.command(name='doviz',
	description="Güncel döviz kurunu ve bitcoin fiyatını gösterir.")
async def doviz():
 # TODO: Altın eklenebilir.
 dovizurl = "https://www.doviz.gen.tr/doviz_json.asp"
 response = requests.get(dovizurl)
 value_dolar_alis = response.json()['dolar']
 value_dolar_satis = response.json()['dolar2']
 value_dolar_kapanis = response.json()['ddolar2']
 value_euro_alis = response.json()['euro']
 value_euro_satis = response.json()['euro2']
 value_euro_kapanis = response.json()['deuro']
 value_son_guncellenme = response.json()['songuncellenme']
 await bot.say("Güncel Euro: " + "Alış kuru: " + value_euro_alis + ", " + "Satış kuru: " + value_euro_satis)
 await bot.say("Euro dün " + value_euro_kapanis + " seviyesinde kapanış yaptı." )
 await bot.say("Güncel Dolar: " + "Alış kuru: " + value_dolar_alis + ", " + "Satış kuru: " + value_dolar_satis)
 await bot.say("Dolar dün " + value_dolar_kapanis + " seviyesinde kapanış yaptı." )
 await bot.say("Son güncellenme: " + value_son_guncellenme)
 # TODO: USD değil de TRY olabilir.
 # Bitcoin fiyatı
 bitcoinurl = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
 response = requests.get(bitcoinurl)
 bitcoin_value = response.json()['bpi']['USD']['rate']
 await bot.say("Güncel Bitcoin alış fiyatı: $" + bitcoin_value)

# TODO: Haftalık ve günlük olarak havadurumu tahmini
#@bot.command(name='havadurumu',
#	description="$SEHIR şehri için güncel havadurumunu gösterir.",
#	pass_context=True)
#async def havadurumu(ctx):
# await bot.say("WIP!!")

#TODO: Sadece grup admini tarafından kullanılacak bir komut haline getir!
@bot.command(name='clean',
	description="Bu komut riskli olduğundan sadece sahibi tarafından kullanılabilir. Kullanıldığında; yeniden eskiye yazdığınız sayı kadar mesaj siler.(Minimum 2 mesaj siler)",
	#aliases=['??clean'],
	pass_context=True)
async def clean(ctx, number):
 msg = []
 number = int(number)
 async for x in bot.logs_from(ctx.message.channel, limit=number):
    msg.append(x)
 await bot.delete_messages(msg)

bot.run(token)
