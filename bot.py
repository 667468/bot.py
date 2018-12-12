import discord
from discord import Game
from discord.ext import commands
import os
import requests
import asyncio

bot_prefix = ("!!", "??", ">>") # Bunu kendi isteğinize göre değiştirebilirsiniz. Botun komutu algılaması için, komutun başında bu üç prefixte biri olması gerekli. Örneğin; !!doviz, ??doviz, >>doviz gibi...
token = (os.environ['BOT_TOKEN']) # Discord botu oluşturduğunuzda çıkan tokeni 'BOT_TOKEN' kısmına ekleyin. "os.environ" kısmı; bu bot Github üzerinde paylaşıldığı ve Heroku üzerinde çalıştığı için eklendi. Kendi sunucunuzda çalıştıracak veya botun tokenini direk ekleyecekseniz silebilirsiniz.
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
 print("BOT: Logged as: {}".format(bot.user.name))
 print("BOT: ID: {}".format(bot.user.id))
 print("BOT: Joined {}".format(str(len(bot.servers))) + " server/s!")
 await bot.change_presence(game=Game(name='Komutlar için "!!help" yazabilirsiniz!'))

# Kişisel yardım komutu
# TODO: Basitleştir.
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
 commands = [bbot,doviz,havadurumu]
 descriptions = ["Botun hakkında bilgi verir.", "Güncel döviz kurunu gösterir.", "İstanbul şehri için güncel havadurumu bilgisini gösterir."]
 await bot.say("'{}' komutu: {}\n" \
 	"'{}' komutu: {}\n" \
 	"'{}' komutu: {}\n" \
 	"#UYARI: Komutları kullanmadan önce başlarında '{}' '{}' '{}' bu üç prefixden biri olması gerekli! Örneğin; !!doviz, ??doviz, >>doviz gibi...".format(commands[0],descriptions[0],commands[1],descriptions[1],commands[2],descriptions[2],bot_prefix[0],bot_prefix[1],bot_prefix[2]))

@bot.command(pass_context=True)
async def adminhelp(ctx):
 commands = [kick,ban,unban,clear]
 descriptions = ["Kullanıcıyı sunucudan kickler.","Kullanıcıyı sunucudan banlar.","Kullanıcının sunucudan banını kaldırır.","Yeniden eskiye yazdığınız sayı kadar mesaj siler. Minimum 2, maksimum 100 mesaj siler."]
 if ctx.message.author.server_permissions.administrator:
  await bot.say("'{}' komutu: {}\n" \
 	"'{}' komutu: {}\n" \
 	"'{}' komutu: {}\n" \
 	"'{}' komutu: {}\n".format(commands[0],descriptions[0],commands[1],descriptions[1],commands[2],descriptions[2],commands[3],descriptions[3]))
 else:
  await bot.say("Komut listesi için !!help komutunu kullanabilirsiniz!")

@bot.command(pass_context=True)
async def bbot(ctx):
 await bot.say("Ben Fatih Ünsever tarafından yazılmış bir Discord uygulaması botuyum!")

# Kullanıcıyı sunucudan kickler.
@bot.command(pass_context=True)
async def kick(ctx, userName: discord.Member):
 if ctx.message.author.server_permissions.administrator:
  await bot.kick(userName)
  print("{} isimli kullanıcı kicklendi!".format(userName))
 else:
  await bot.say("Üzgünüm {}, bunu yapmaya izniniz yok!".format(ctx.message.author))

# Kullanıcıyı sunucudan banlar.
@bot.command(pass_context=True)
async def ban(ctx, userName: discord.Member):
 if ctx.message.author.server_permissions.administrator:
  await bot.ban(userName)
  print("{} isimli kullanıcı banlandı!".format(userName))
 else:
  await bot.say("Üzgünüm {}, bunu yapmaya izniniz yok!".format(ctx.message.author))

# Kullanıcının sunucudan banını kaldırır.
@bot.command(pass_context=True)
async def unban(ctx, userName: discord.Member):
 if ctx.message.author.server_permissions.administrator:
  await bot.unban(userName)
  print("{} isimli kullanıcı unbanlandı!".format(userName))
 else:
  await bot.say("Üzgünüm {}, bunu yapmaya izniniz yok!".format(ctx.message.author))

# Yeniden eskiye yazdığınız sayı kadar mesaj siler. Minimum 2, maksimum 100 mesaj siler.
@bot.command(pass_context=True)
async def clear(ctx, amount=100):
 if ctx.message.author.server_permissions.administrator:
  channel = ctx.message.channel
  messages= []
  async for message in bot.logs_from(channel, limit=int(amount)):
        messages.append(message)
  await bot.delete_messages(messages)
  print("{} isimli kullanıcı {} adet mesaj sildi!".format(ctx.message.author, amount))
 else:
  await bot.say("Üzgünüm {}, bunu yapmaya izniniz yok!".format(ctx.message.author))

# Güncel döviz kurunu gösterir.
@bot.command(pass_context=True)
async def doviz(ctx):
 dovizurl = "http://www.floatrates.com/daily/try.json"
 response = requests.get(dovizurl)
 usd_alis = response.json()['usd']['inverseRate']
 eur_alis = response.json()['eur']['inverseRate']
 gbp_alis = response.json()['gbp']['inverseRate']
 cad_alis = response.json()['cad']['inverseRate']
 chf_alis = response.json()['chf']['inverseRate']
 kwd_alis = response.json()['kwd']['inverseRate']
 sar_alis = response.json()['sar']['inverseRate']
 son_guncelleme = response.json()['usd']['date']
 await bot.say("Güncel 1 ABD Doları " + "alış fiyatı: {}".format(float("%.2f" % usd_alis)) + " TRY\n" \
 	"Güncel 1 Euro " + "alış fiyatı: {}".format(float("%.2f" % eur_alis)) + " TRY\n" \
 	"Güncel 1 İngiliz Sterlini " + "alış fiyatı: {}".format(float("%.2f" % gbp_alis)) + " TRY\n" \
 	"Güncel 1 Kanada Doları " + "alış fiyatı: {}".format(float("%.2f" % cad_alis)) + " TRY\n" \
 	"Güncel 1 İsviçre Frangı " + "alış fiyatı: {}".format(float("%.2f" % chf_alis)) + " TRY\n" \
 	"Güncel 1 Kuveyt Dinarı " + "alış fiyatı: {}".format(float("%.2f" % kwd_alis)) + " TRY\n" \
 	"Güncel 1 S. Arabistan Riyali " + "alış fiyatı: {}".format(float("%.2f" % sar_alis)) + " TRY\n" \
 	"Döviz son güncelleme: " + son_guncelleme)

# İstanbul şehri için güncel havadurumu bilgisini gösterir.
@bot.command(pass_context=True)
async def havadurumu(ctx):
 # TODO: Havadurumu bilgilerini Türkçe'ye ayarla! API İngilizce
 havadurumuurl = "https://www.metaweather.com/api/location/2344116/"
 response = requests.get(havadurumuurl)
 havadurumu = response.json()['consolidated_weather'][0]['weather_state_name']
 ortsicaklik_havadurumu = response.json()['consolidated_weather'][0]['the_temp']
 minsicaklik_havadurumu = response.json()['consolidated_weather'][0]['min_temp']
 maxsicaklik_havadurumu = response.json()['consolidated_weather'][0]['max_temp']
 ruzgarhizi_havadurumu = response.json()['consolidated_weather'][0]['wind_speed']
 ruzgaryonu_havadurumu = response.json()['consolidated_weather'][0]['wind_direction_compass']
 nem_havadurumu = response.json()['consolidated_weather'][0]['humidity']
 dogus_havadurumu = response.json()['sun_rise']
 batis_havadurumu = response.json()['sun_set']
 tarih_havadurumu = response.json()['consolidated_weather'][0]['applicable_date']
 await bot.say("Hava durumu: " + havadurumu + "\n" \
 	"Gün içerisinde Ort. sıcaklık: {}".format(int(ortsicaklik_havadurumu)) + " °C\n" \
 	"Gün içerisinde Min. sıcaklık: {}".format(int(minsicaklik_havadurumu)) + " °C\n" \
 	"Gün içerisinde Max. sıcaklık: {}".format(int(maxsicaklik_havadurumu)) + " °C\n" \
 	"Rüzgar hızı: {}".format(int(ruzgarhizi_havadurumu)) + " " + ruzgaryonu_havadurumu + "\n" \
 	"Nem miktarı: %{}".format(int(nem_havadurumu)) + "\n" \
 	"Güneş'in doğuşu: " + dogus_havadurumu + "\n" \
 	"Güneş'in batışı : " + batis_havadurumu + "\n" \
 	"Hava durumu son güncelleme: " + tarih_havadurumu)

bot.run(token)
