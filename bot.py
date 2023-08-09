import discord
from discord.ext import commands
from googletrans import Translator
import os
import random 
import requests
import youtube_dl

intents = discord.Intents.default()
intents.message_content = True
sonuc = ["yazi", "tura"] 
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık')


#BOTUN TANITIMI
@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba {bot.user}! Ben botum.')


#HE KOMUDU
@bot.command()
async def heh(ctx, count_heh = 5):
    await ctx.send("he" * count_heh)


#GELEN KULLANICIYA DMDEN HOŞGELDİN MESAJI
@bot.event
async def on_member_join(member):
    await member.send(f"{discord.Member} sunucuya hoş geldin!")


#MESAJIN KİM TARAFINDAN SİLİNDİĞİ VE NE ZAMAN SİLİNDİĞİNİ LOGLAYAN KOMUT
@bot.event
async def on_message_delete(message):
    print(f'{message.author} : {message.content} : {message.created_at}')


#ÇEVİRİ KOMUTU
@bot.command()
async def cevir(ctx, text):
    translator = Translator()
    ceviri = translator.translate(text)
    await ctx.send(ceviri.text)


#KİCK KOMUTU
@bot.command()
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send("Kullanıcı Sunucudan Atıldı.")

#BAN KOMUTU
@bot.command()
async def ban(ctx, member: discord.Member):
    await member.ban()
    await ctx.send("Kullanıcı Sunucudan Yasaklandı.")


# UNBAN KOMUDU
@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} yasağı kaldırıldı.')
            return

# SUSTURMA KOMUDU
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not muted_role:
        muted_role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False)

    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f'{member.mention} susturuldu. Sebep: {reason}')

# SUSTURMA KALDIRMA KOMUDU
@bot.command()
async def unmute(ctx, member: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
    if muted_role in member.roles:
        await member.remove_roles(muted_role)
        await ctx.send(f'{member.mention} susturulması kaldırıldı.')
    else:
        await ctx.send(f'{member.mention} zaten susturulmamış.')

#CAPS LOCK UYARI KOMUTU
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    total_characters = len(message.content)
    uppercase_characters = sum(1 for char in message.content if char.isupper())
    uppercase_ratio = uppercase_characters / total_characters

    uppercase_threshold = 0.6 
    if uppercase_ratio > uppercase_threshold:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, lütfen büyük harfle yazmayın.")

    await bot.process_commands(message)

#ZAR ATMA KOMUTU
@bot.command()
async def zarat(ctx):
    await ctx.send(str(random.randint(1, 6)))

#YAZI TURA KOMUTU
@bot.command()
async def yazitura(ctx):
    await ctx.send(random.choice(sonuc))

#TEMİZLEME KOMUTU
@bot.command()
async def sil(ctx, amount: int):
    print(f"!sil komutu çağırıldı. Silinecek mesaj sayısı: {amount}")

    if 1 <= amount <= 100:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} mesaj silindi.", delete_after=5)
    else:
        await ctx.send("Geçerli bir mesaj sayısı belirtmelisiniz. (1 ile 100 arasında)")

#HAVA DURUMU KOMUTU 
@bot.command()
async def hava(ctx, *, city: str):
    try:
        API_KEY = "77ad1b337a14b14bd9bf1ffaa259d157"  

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == "404":
            await ctx.send("Bu şehir bulunamadı.")
        else:
            city_name = data["name"]
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            message = f"Hava Durumu: {weather_desc}\nSıcaklık: {temp}°C\nNem: {humidity}%"
            await ctx.send(f"{city_name} için hava durumu:\n{message}")

    except Exception as e:
        print(e)
        await ctx.send("Hava durumu bilgisini alırken bir hata oluştu.")


#TAŞ KAĞIT MAKAS KOMUTU
@bot.command()
async def taş_kağıt_makas(ctx, choice: str):
    choices = ['taş', 'kağıt', 'makas']
    bot_choice = random.choice(choices)

    choice = choice.lower()

    if choice not in choices:
        await ctx.send("Lütfen geçerli bir seçenek girin: taş, kağıt veya makas.")
    else:
        await ctx.send(f"Benim seçimim: {bot_choice}")

        if choice == bot_choice:
            await ctx.send("Berabere!")
        elif (
            (choice == 'taş' and bot_choice == 'makas') or
            (choice == 'kağıt' and bot_choice == 'taş') or
            (choice == 'makas' and bot_choice == 'kağıt')
        ):
            await ctx.send("Tebrikler, kazandınız!")
        else:
            await ctx.send("Üzgünüm, kaybettiniz!")        

#ŞAKA KOMUTU
sakalar = [
    "Neden aslanlar aslan kralı izlemek istemez? Çünkü hakimiyetinde benzin bitti.",
    "Adamın biri güneşte yanmış, ayda donmuş, düşün sen kimsin?",
    "Yılanlardan korkma, yılmayanlardan kork.",
    "Ben hikaye anlatmam, hikaye yazarım.",
    "Adamın biri bir gün oksijenle dalga geçmiş. Nefessiz kalmış.",
    "Geçen gün taksi çevirdim ama hala dönüyor.",
    "Dünya dönüyor, insanlar dönüyor, ben dönüyorum, döner döner, dönüp dururum.",
    "En hızlı sayı hangisidir? 10, çünkü '10' diye okuyabiliyorsunuz.",
    "Beni ayakta uyutuyorsun, oturarak uyutamaz mısın?",
    "Kahve yapıyorum, filtre tutmayan kahvehaneye uğra mı gelirsin?",
]

@bot.command()
async def saka(ctx):
    joke = random.choice(sakalar)
    await ctx.send(joke)

#YARDIM KOMUTU
@bot.command()
async def yardim(ctx):
    embed = discord.Embed(title="Desty Bot Yardım Paneli", description="Bot yardım paneli", color=discord.Color.blue())
    embed.add_field(name="!hello", value="bot kendini tanıtır.", inline=False)
    embed.add_field(name="!heh <sayı>", value="bot verilen değer kadar he yazar.", inline=False)
    embed.add_field(name="!cevir <metin>", value="bot kendisine verilen metni çevirir.", inline=False)
    embed.add_field(name="!kick @", value="bot etiketlenen kullanıcıyı sunucudan atar.", inline=False)
    embed.add_field(name="!ban @", value="bot etiketlenen kullanıcıyı sunucudan yasaklar.", inline=False)
    embed.add_field(name="!zarat", value="bot zar atar.", inline=False)
    embed.add_field(name="!yazitura", value="bot yazı tura yapar.", inline=False)
    embed.add_field(name="!sil <sayı>", value="bot verilen değer kadar kanaldaki mesajları siler.", inline=False)
    embed.add_field(name="!hava <sehir>", value="bot istenilen şehirdeki hava durumunu yazar.", inline=False)
    embed.add_field(name="!taş_kağıt_makas <seçenek>", value="bot taş kağıt makas oynar.", inline=False)
    embed.add_field(name="!unban @", value="bot etiketlenen kişinin yasağını kaldırır.", inline=False)
    embed.add_field(name="!mute @", value="bot etiketlenen kişiyi susturur.", inline=False)
    embed.add_field(name="!unmute @", value="bot etiketlenen kişinin susturmasını kaldırır.", inline=False)
    embed.add_field(name="!saka", value="bot rastgele şaka yapar.", inline=False)

    embed.set_footer(text="Yardıma mı ihtiyacın var ? <destybabakral> kullanıcısına ulaşabilirsin.")
    await ctx.send(embed=embed)

#MÜZİK KOMUTU
@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send("Bir ses kanalına katılmanız gerekiyor.")
        return
    await channel.connect()

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Bot zaten bir ses kanalında değil.")

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send("Bir ses kanalına katılmanız gerekiyor.")
        return

    vc = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']

    vc.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('Oynatma bitti', e))
    await ctx.send(f'Şimdi çalıyor: {url}')

@bot.command()
async def pause(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Müzik duraklatıldı.")
        else:
            await ctx.send("Müzik zaten duraklatıldı.")
    else:
        await ctx.send("Müzik çalmıyor.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Müzik devam ettiriliyor.")
        else:
            await ctx.send("Müzik zaten devam ediyor.")
    else:
        await ctx.send("Müzik çalmıyor.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("Müzik durduruldu.")
    else:
        await ctx.send("Müzik çalmıyor.")

@bot.command()
async def meme_at(ctx):
    liste = os.listdir("memes")
    rastgele_meme = random.choice(liste)
    tam_uzanti = "memes/" + rastgele_meme
    f = open(tam_uzanti, "rb")
    meme = discord.File(f)
    await ctx.send(file=meme)        


bot.run("MTEzMTI2Mzk1OTcxMDgzODg5NQ.GIugTM.nwFrGvsVV5pxi7rKlMenXHc_FBFakmJvtgO4JI")
