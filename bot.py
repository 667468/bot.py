import discord
from discord import Game
from discord.ext import commands
import os
import requests
import asyncio
from bs4 import BeautifulSoup
import urllib.request

bot_prefix = ("!!", "??", ">>") # Bunu kendi isteğinize göre değiştirebilirsiniz. Botun komutları algılaması için, komutların başında bu üç prefixte biri olması gerekli. Örneğin; !!xyz, ??xyz, >>xyz gibi...
token = (os.environ['BOT_TOKEN']) # Discord botunuzun tokenini 'export BOT_TOKEN=XXX' şeklinde veya '(os.environ)' kısmını silip, 'BOT_TOKEN' kısmına ekleyin.
bot = commands.Bot(command_prefix=bot_prefix)

@bot.event
async def on_ready():
	print("BOT: Logged as: {}".format(bot.user.name))
	print("BOT: ID: {}".format(bot.user.id))
	print("BOT: Joined {}".format(str(len(bot.guilds))) + " guild/s!")
	activity = discord.Game(name="Komutlar için: !!help")
	await bot.change_presence(status=discord.Status.dnd, activity=activity) # 'status' komutu sayesinde botun durumu değiştiriliyor. (online,invisible,idle,dnd)

### Yardım komutu
bot.remove_command('help')
@bot.command(pass_context=True)
async def help(ctx):
	commands = [about,doviz,havadurumu]
	descriptions = ["Botun hakkında bilgi verir.", "Güncel döviz kurunu gösterir.", "Istenilen şehir için güncel havadurumu bilgisini gösterir."]
	await ctx.send(\
		"Bot komutları:\n" \
		"```'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}```".format(commands[0],descriptions[0],commands[1],descriptions[1],commands[2],descriptions[2]))

	"""
	# Muzik/Video yardım komutu
	commands = [join,leave,play,pause,resume,stop,queue]
	descriptions = ["Bulunduğunuz ses kanalına katılır.", "Bulunduğunuz ses kanalından ayrılır.", "Şarkıyı başlatır.", "Şarkıyı duraklatır.", "Şarkıyı devam ettirir.", "Şarkıyı durdurur veya bir sonraki şarkıya geçer.", "Şarkıyı sıraya alır."]
	await ctx.send(\
		"Müzik komutları:\n" \
		"```'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}\n" \
		"'{}' komutu: {}```".format(commands[0],descriptions[0],commands[1],descriptions[1],commands[2],descriptions[2],commands[3],descriptions[3],commands[4],descriptions[4],commands[5],descriptions[5],commands[6],descriptions[6]))

	await ctx.send("Örnek 'doviz' komutu kullanımı: ```{}doviz {}doviz {}doviz```".format(bot_prefix[0],bot_prefix[1],bot_prefix[2]))
	await ctx.send("Örnek 'stop' komutu kullanımı: ```{}stop {}stop {}stop```".format(bot_prefix[0],bot_prefix[1],bot_prefix[2]))
	"""

### Sunucu adminleri için yardım komutu. ('help' komutunda gözükmez!)
@bot.command(pass_context=True)
async def adminhelp(ctx):
	message_author = ctx.message.author
	commands = [kick,ban,unban,clear]
	descriptions = ["Kullanıcıyı kickler.","Kullanıcıyı banlar.","Kullanıcının banını kaldırır.","Yeniden eskiye yazdığınız sayı kadar mesaj siler. Minimum 2, maksimum 100 mesaj siler."]
	admin_kontrol = message_author.guild_permissions.administrator
	if admin_kontrol:
		await ctx.send(\
			"Bu komutları sadece sunucu adminleri kullanabilir!\n" \
			"```'{}' komutu: {}\n" \
			"'{}' komutu: {}\n" \
			"'{}' komutu: {}\n" \
			"'{}' komutu: {}```".format(commands[0],descriptions[0],commands[1],descriptions[1],commands[2],descriptions[2],commands[3],descriptions[3]))
	else:
		await ctx.send("Komut listesi için !!help komutunu kullanabilirsiniz!")

### Botun hakkında bilgi verir.
@bot.command(pass_context=True)
async def about(ctx):
	await ctx.send("Merhaba! Ben Fatih Ünsever tarafından yazılmış bir Discord uygulaması botuyum! Komutlar için {}help yazabilirsiniz!".format(bot_prefix[0]))

### Kullanıcıyı kickler.
@bot.command(pass_context=True)
async def kick(ctx, user: discord.Member, *, reason):
	message_author = ctx.message.author
	admin_kontrol = message_author.guild_permissions.administrator
	if admin_kontrol:
		await user.kick(reason=reason)
		print("'{}' isimli kullanıcı, '{}' sebebinden dolayi kicklendi!".format(user,reason))
	else:
		await ctx.send("Üzgünüm '{}', bunu yapmaya izniniz yok!".format(message_author))

### Kullanıcıyı banlar.
@bot.command(pass_context=True)
##FIXME: Calisiyor ama banlanan kisi tekrar guilde katilabiliyor???
async def ban(ctx, user: discord.Member, *, reason):
	message_author = ctx.message.author
	admin_kontrol = message_author.guild_permissions.administrator
	if admin_kontrol:
		await user.ban(reason=reason)
		print("'{}' isimli kullanıcı, '{}' sebebinden dolayi banlandı!".format(user,reason))
	else:
		await ctx.send("Üzgünüm '{}', bunu yapmaya izniniz yok!".format(message_author))

### Kullanıcının banını kaldırır.
@bot.command(pass_context=True)
async def unban(ctx, user: discord.Member):
	message_author = ctx.message.author
	admin_kontrol = message_author.guild_permissions.administrator
	if admin_kontrol:
		await user.unban()
		print("'{}' isimli kullanıcı unbanlandı!".format(user))
	else:
		await ctx.send("Üzgünüm '{}', bunu yapmaya izniniz yok!".format(message_author))

### Yeniden eskiye yazdığınız sayı kadar mesaj siler. Minimum 2, maksimum 100 mesaj siler.
@bot.command(pass_context=True)
async def clear(ctx, amount=100):
	message_author = ctx.message.author
	admin_kontrol = message_author.guild_permissions.administrator
	if admin_kontrol:
		await ctx.channel.purge(limit=int(amount))
		print("{} isimli kullanıcı {} adet mesaj sildi!".format(message_author, amount))
	else:
		await ctx.send("Üzgünüm {}, bunu yapmaya izniniz yok!".format(message_author))

### Güncel döviz kurunu gösterir.
@bot.command(pass_context=True)
async def doviz(ctx):
	dovizurl = "https://api.canlidoviz.com/web/items"
	response = requests.get(dovizurl)
	usd_name = response.json()[0]['name']
	usd_alis = response.json()[0]['buyPrice']
	usd_satis = response.json()[0]['sellPrice']
	eur_name = response.json()[1]['name']
	eur_alis = response.json()[1]['buyPrice']
	eur_satis = response.json()[1]['sellPrice']
	gbp_name = response.json()[2]['name']
	gbp_alis = response.json()[2]['buyPrice']
	gbp_satis = response.json()[2]['sellPrice']
	chf_name = response.json()[3]['name']
	chf_alis = response.json()[3]['buyPrice']
	chf_satis = response.json()[3]['sellPrice']
	cad_name = response.json()[4]['name']
	cad_alis = response.json()[4]['buyPrice']
	cad_satis = response.json()[4]['sellPrice']
	await ctx.send(\
 		"1 {} ".format(usd_name) + "alış fiyatı: {:.2f} ".format(usd_alis) + "TRY " + "satış fiyatı: {:.2f}".format(usd_satis) + " TRY\n" \
 		"1 {} ".format(eur_name) + "alış fiyatı: {:.2f} ".format(eur_alis) + "TRY " + "satış fiyatı: {:.2f}".format(eur_satis) + " TRY\n" \
		"1 {} ".format(gbp_name) + "alış fiyatı: {:.2f} ".format(gbp_alis) + "TRY " + "satış fiyatı: {:.2f}".format(gbp_satis) + " TRY\n" \
 		"1 {} ".format(chf_name) + "alış fiyatı: {:.2f} ".format(chf_alis) + "TRY " + "satış fiyatı: {:.2f}".format(chf_satis) + " TRY\n" \
 		"1 {} ".format(cad_name) + "alış fiyatı: {:.2f} ".format(cad_alis) + "TRY " + "satış fiyatı: {:.2f}".format(cad_satis) + " TRY\n")

### Istenilen şehir için güncel havadurumu bilgisini gösterir.
@bot.command(pass_context=True)
async def havadurumu(ctx, city):
	havadurumu_url = urllib.request.urlopen("https://www.mgm.gov.tr/FTPDATA/bolgesel/" + city + "/sonSOA.xml")
	#await ctx.send("{}, lütfen komutu girdikten sonra şehiri yazınız. Örnek: ```{}havadurumu Izmir```".format(message_author,bot_prefix[0]))
	xml = BeautifulSoup(havadurumu_url, 'xml')
	for i in xml.findAll('SOA', limit=1):
		havadurumu = i.find('GenelDurum').text
		havadurumu_tarih = i.find('Tarih').text
		sicaklik = i.find('Mak').text
		sicaklik_degisimi = i.find('HavaSicakligi').text
		ruzgar_durumu = i.find('RuzgarDurum').text
	await ctx.send(\
		"Sıcaklık: " + sicaklik + " °C" + "\n" \
		"Hava durumu: " + havadurumu + "\n" \
		"Sıcaklık değişimi: " + sicaklik_degisimi + "\n" \
		"Rüzgar durumu: " + ruzgar_durumu + "\n" \
		"Son güncelleme: " + havadurumu_tarih)

bot.run(token)
