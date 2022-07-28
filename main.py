import discord, imgbbpy, datetime
from discord.ext import commands

bot = commands.Bot(command_prefix='/')

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

print('start...\a')
print(nowDatetime)

@bot.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(bot.user.name) 
    print(bot.user.id) 
    await bot.change_presence(status=discord.Status.online) # 온라인    
    # await client.change_presence(status=discord.Status.offline) # 오프라인
    print('------')

@bot.event
async def on_message(message): 
    
    # 특정 채널 무시
    # if message.channel.id == 123456789 or message.channel.id == 123456789 or message.channel.id == 123456789:
    #     return

    # 특정 유저 무시
    # if message.author.id == 123456789:
    #     return

    image_types = [".png", ".jpeg", ".gif", ".jpg", ".PNG", ".BMP", ".bmp", ".RLE", ".rle", ".pdf",".PDF"]

    channeles = bot.get_channel(1002021888664539266) # 전송할 채널 ID

    author = str(message.author)
    content = str(message.content)
    userid = str(message.author.id) 
    messageid = str(message.id)
    time = str(message.created_at)
    link = str(message.jump_url)
    # channel = str(message.channel) #수정
    # channel_id = str(message.channel.id) #수정
    channel = int(message.author.id)
    channel_id= int(message.channel.id)
    row = [userid,author,content,time,messageid,link,channel]
    print(f"{time}\nID:{userid} user:{author} 내용:{content}\n")
              
    for attachment in message.attachments:

        if any(attachment.filename.lower().endswith(image) for image in image_types):
            await attachment.save(attachment.filename)

        clients = imgbbpy.SyncClient('imgbb api 토큰') # imgbb api 토큰
        image = clients.upload(file=attachment.filename)

        # print(image.url)

        embed = discord.Embed(title="Archive", color=0x62c1cc)
        # embed = discord.Embed(title="Archive", color=0x62c1cc)
        embed.add_field(name="ID", value=attachment.id, inline=False)
        embed.add_field(name="사용자 ID", value=userid, inline=False)
        embed.add_field(name="채널", value=f"<#{channel_id}>", inline=True)  
        embed.add_field(name="사용자", value=f"<@!{channel}>", inline=True)
        embed.add_field(name="파일명", value=attachment.filename, inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text=f"게시일:{time}")
        embed.set_image(url=image.url)
        await channeles.send(embed=embed) 

    embed = discord.Embed(title="Archive", color=0x62c1cc)
    embed.add_field(name="ID", value=message.id, inline=False)
    embed.add_field(name="사용자 ID", value=userid, inline=False)  
    embed.add_field(name="채널", value=f"<#{channel_id}>", inline=True)  #수정
    embed.add_field(name="사용자", value=f"<@!{channel}>", inline=True) #수정 
    embed.set_thumbnail(url=message.author.avatar_url)
    embed.add_field(name="내용", value=content, inline=False)
    embed.set_footer(text=f"게시일:{time}")
    await channeles.send(embed=embed) 

bot.run('discord api 토큰') # discord api 토큰
