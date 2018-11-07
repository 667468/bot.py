from discord.ext.commands import Bot
from discord import Game
import os
import requests

bot_prefix = ("!!", "??") # Bunu kendi isteğinize göre değiştirebilirsiniz. Botun komutu algılaması için, komutun başında bu iki prefixte biri olması gerekli. Örneğin; !!doviz, ??doviz gibi...
token = (os.environ['BOT_TOKEN']) # Discord botu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin.
bot = Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
 print("BOT: Logged as: {}".format(bot.user.name))
 print("BOT: ID: {}".format(bot.user.id))
 print("BOT: Joined {}".format(str(len(bot.servers))) + " server/s!")
 await bot.change_presence(game=Game(name='Komutlar için "!!help" yazabilirsiniz!'))

@bot.command(name='bbot',
	description="Botun hakkında bilgi verir.",
	aliases=['??bbot'],
	pass_context=True)
async def bbot(ctx):
 await bot.say("Ben Fatih Ünsever tarafından yazılmış bir Discord uygulaması botuyum!")

# Güncel döviz kurlarını gösterir.
@bot.command(name='doviz',
	description="Güncel döviz kurunu ve bitcoin fiyatını gösterir.",
	aliases=['??doviz'],
	pass_context=True)
async def doviz(ctx):
 dovizurl = "http://www.floatrates.com/daily/try.json"
 response = requests.get(dovizurl)
 value_usd_alis = response.json()['usd']['inverseRate']
 value_eur_alis = response.json()['eur']['inverseRate']
 value_gbp_alis = response.json()['gbp']['inverseRate']
 value_cad_alis = response.json()['cad']['inverseRate']
 value_chf_alis = response.json()['chf']['inverseRate']
 value_kwd_alis = response.json()['kwd']['inverseRate']
 value_sar_alis = response.json()['sar']['inverseRate']
 value_son_guncellenme = response.json()['usd']['date']
 await bot.say("Güncel 1 ABD Doları: " + "Alış fiyatı: " + str(value_usd_alis) + " TRY")
 await bot.say("Güncel 1 Euro: " + "Alış fiyatı: " + str(value_eur_alis) + " TRY")
 await bot.say("Güncel 1 İngiliz Sterlini: " + "Alış fiyatı: " + str(value_gbp_alis) + " TRY")
 await bot.say("Güncel 1 Kanada Doları: " + "Alış fiyatı: " + str(value_cad_alis) + " TRY")
 await bot.say("Güncel 1 İşviçre Frangı: " + "Alış fiyatı: " + str(value_chf_alis) + " TRY")
 await bot.say("Güncel 1 Kuveyt Dinarı: " + "Alış fiyatı: " + str(value_kwd_alis) + " TRY")
 await bot.say("Güncel 1 S. Arabistan Riyali: " + "Alış fiyatı: " + str(value_sar_alis) + " TRY")
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
