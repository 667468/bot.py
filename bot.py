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
	pass_context=True)
async def bbot(ctx):
 await bot.say("Ben Fatih Ünsever tarafından yazılmış bir Discord uygulaması botuyum!")

# Güncel döviz kurunu ve bitcoin fiyatını gösterir.
@bot.command(name='doviz',
	description="Güncel döviz kurunu ve bitcoin fiyatını gösterir.",
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
 value_son_guncelleme = response.json()['usd']['date']
 await bot.say("Güncel 1 ABD Doları " + "alış fiyatı: " + str(value_usd_alis) + " TRY")
 await bot.say("Güncel 1 Euro " + "alış fiyatı: " + str(value_eur_alis) + " TRY")
 await bot.say("Güncel 1 İngiliz Sterlini " + "alış fiyatı: " + str(value_gbp_alis) + " TRY")
 await bot.say("Güncel 1 Kanada Doları " + "alış fiyatı: " + str(value_cad_alis) + " TRY")
 await bot.say("Güncel 1 İsviçre Frangı " + "alış fiyatı: " + str(value_chf_alis) + " TRY")
 await bot.say("Güncel 1 Kuveyt Dinarı " + "alış fiyatı: " + str(value_kwd_alis) + " TRY")
 await bot.say("Güncel 1 S. Arabistan Riyali " + "alış fiyatı: " + str(value_sar_alis) + " TRY")
 # Bitcoin fiyatı (TRY cinsinden)
 bitcoinurl = "https://api.coindesk.com/v1/bpi/currentprice/TRY.json"
 response = requests.get(bitcoinurl)
 bitcoin_value = response.json()['bpi']['TRY']['rate']
 await bot.say("Güncel 1 Bitcoin " + "alış fiyatı: " + bitcoin_value + " TRY")
 await bot.say("Son güncelleme: " + value_son_guncelleme)

# İstanbul şehri için güncel havadurumu bilgisini gösterir.
@bot.command(name='havadurumu',
	description="İstanbul şehri için güncel havadurumu bilgisini gösterir.",
	pass_context=True)
async def havadurumu(ctx):
 # TODO: Havadurumu bilgilerini Türkçe'ye ayarla! API İngilizce
 havadurumuurl = "https://www.metaweather.com/api/location/2344116/"
 response = requests.get(havadurumuurl)
 value_havadurumu = response.json()['consolidated_weather'][0]['weather_state_name']
 value_ortsicaklik_havadurumu = response.json()['consolidated_weather'][0]['the_temp']
 value_minsicaklik_havadurumu = response.json()['consolidated_weather'][0]['min_temp']
 value_maxsicaklik_havadurumu = response.json()['consolidated_weather'][0]['max_temp']
 value_ruzgarhizi_havadurumu = response.json()['consolidated_weather'][0]['wind_speed']
 value_ruzgaryonu_havadurumu = response.json()['consolidated_weather'][0]['wind_direction_compass']
 value_nem_havadurumu = response.json()['consolidated_weather'][0]['humidity']
 value_dogus_havadurumu = response.json()['sun_rise']
 value_batis_havadurumu = response.json()['sun_set']
 value_tarih_havadurumu = response.json()['consolidated_weather'][0]['applicable_date']
 await bot.say("Hava durumu: " + value_havadurumu)
 await bot.say("Gün içerisinde Ort. Sıcaklık: " + str(value_ortsicaklik_havadurumu) + " °C")
 await bot.say("Gün içerisinde Min. Sıcaklık: " + str(value_minsicaklik_havadurumu) + " °C")
 await bot.say("Gün içerisinde Max. Sıcaklık: " + str(value_maxsicaklik_havadurumu) + " °C")
 await bot.say("Rüzgar hızı: " + str(value_ruzgarhizi_havadurumu) + " " + value_ruzgaryonu_havadurumu)
 await bot.say("Nem Miktarı: %" + str(value_nem_havadurumu))
 await bot.say("Güneş Doğuşu: " + str(value_dogus_havadurumu))
 await bot.say("Güneş Batışı : " + str(value_batis_havadurumu))
 await bot.say("Hava durumu tarihi: " + value_tarih_havadurumu)

# Yeniden eskiye yazdığınız sayı kadar mesaj siler.(Minimum 2 mesaj siler)
@bot.command(name='clean',
	description="Bu komut riskli olduğundan sadece sahibi tarafından kullanılabilir. Kullanıldığında; yeniden eskiye yazdığınız sayı kadar mesaj siler.(Minimum 2 mesaj siler)",
	pass_context=True)
async def clean(ctx, number):
 # TODO: Sadece grup admini tarafından kullanılacak bir komut haline getir!
 msg = []
 number = int(number)
 async for x in bot.logs_from(ctx.message.channel, limit=number):
    msg.append(x)
 await bot.delete_messages(msg)

bot.run(token)
