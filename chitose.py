#Esta é a ChitoseBot, escrita em Python e discord.py.
#ChitoseBot é uma Fork de outras bot minhas, TanyaBot e Paradox.
 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import requests
import time
import sys
from async_timeout import timeout
from discord import Game
import asyncio
import random
import functools
import itertools
import math
import os
import youtube_dl


#Prefixos e Token
bot = commands.Bot(command_prefix="c!")
client = discord.ext.commands.Bot(command_prefix = "c!")
TOKEN = ''



#Animaçãozinha show do Terminal
@bot.event
async def on_ready () :
    animation = " | / — \ "
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name='Otacast Brasil - The Trash Anime Cast'))
    
    for i in range(30):
        time.sleep(0.1)
        sys.stdout.write("\r" + animation[ i % len(animation)])
        sys.stdout.flush()
    print("CHITOSE - STATUS:ONLINE"),


#Respostas automáticas
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    salty=[
	       'Não tanto quanto você.',
	       'Olha quem fala.',
	       'Disse o NEET sem vida que assiste anime.',
	       'c!ban.',
	       'morre.'
	      ]
    if message.content.startswith('bot lixo'):
        await message.channel.send(random.choice(salty))
        await bot.process_commands(message)
        
        
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.content.startswith('bot bom'):
        await message.channel.send(':)')
        await bot.process_commands(message)
 
#Comandos
@bot.command(nome='info',
             aliases=['info'])
async def ajuda(ctx):
    embed = discord.Embed(
        title='CHITOSE | 0.0.2', description='LISTA DE COMANDOS', color=0xcc23b5)
    embed.add_field(name="INTERAÇÕES", value="""c!abraço [@membro] - Dá um abraço no membro mencionado.
(aliases - abraçar, hug).

c!choro - Envia um GIF de uma Animu Girl triste.
(aliases - cry, chorar).

c!tapa [@membro] - Dá um tapa no membro mencionado.
(aliases - slap, bater).

c!cafuné [@membro] - Faz um cafuné no membro mencionado.""")


    embed.add_field(name="RÁDIO", value="""c!entrar - Faz com que eu seja adicionada à Rádio/Voice chat que você está.

c!tocar [Música/Link] - Ao colocar o nome/link da música, faz com que ela seja tocada.

c!pausar - Pausa a música atual.

c!retomar - Retoma a música pausada.

c!pular - Abre uma votação de 3 pessoas para pular a música.

c!volume [0 - 100] - Muda o volume da música atual.

c!agora - Mostra a música que está sendo tocada.

c!parar - Para a música e sai do Voice Chat.""")

    embed.add_field(name='MODERAÇÃO', value="""[ESTES COMANDOS SÓ PODEM SER USADOS PELOS PROTAGONISTS]

c!aniquilar [@membro] [Razão] - Bane um membro do servidor.

c!kick [@membro] [Razão] - Expulsa um membro do servidor.

c!aviso [@membro] [Motivo] - Dá um aviso ao membro mencionado.

c!apagar [Valor] - Apaga o número específicado de mensagens.

""")
    embed.set_footer(text='(C) Otacast Brasil - The Trash Anime Cast')
    embed.set_image(url='https://dg31sz3gwrwan.cloudfront.net/fanart/259655/915275-0-q80.jpg')
    await ctx.send( embed = embed )


@bot.command(name='abraço',
                aliases=['hug', 'abraçar', 'abraco', 'abracar'])
async def abraço(ctx, member: discord.Member):
    hugs=['https://media1.tenor.com/images/49a21e182fcdfb3e96cc9d9421f8ee3f/tenor.gif?itemid=3532079',
              'https://i.kym-cdn.com/photos/images/original/000/935/627/3a5.gif',
              'https://i.gifer.com/F1s1.gif',
              'http://i.imgur.com/pME21N2.gif',
              'https://i.gifer.com/2CZ4.gif',
              'http://i.imgur.com/rlOJqHL.gif',
              'https://i.imgur.com/FCXa6Gx.gif',
              'https://media1.tenor.com/images/074d69c5afcc89f3f879ca473e003af2/tenor.gif?itemid=4898650',
              'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/e06f5232-fe1a-4cb8-badf-48ed7fd6af05/d4uw8w5-2cafa0f2-ce59-4852-b4df-d5cdfee5fa7f.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2UwNmY1MjMyLWZlMWEtNGNiOC1iYWRmLTQ4ZWQ3ZmQ2YWYwNVwvZDR1dzh3NS0yY2FmYTBmMi1jZTU5LTQ4NTItYjRkZi1kNWNkZmVlNWZhN2YuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.KCyrL3nscvl71k_0nl8iVV-IM0eH3NyIIbyIIdW3W24',
              'https://media1.tenor.com/images/969f0f462e4b7350da543f0231ba94cb/tenor.gif?itemid=14246498',
              'https://i.gifer.com/5ngg.gif',
              'https://66.media.tumblr.com/ebc214f892af851ffd7297e0e6212cdb/tumblr_o2kwkfyzT01uprh6zo1_400.gifv',
              'https://66.media.tumblr.com/dfdc4dda019b539975e22c7f819cd2d3/tumblr_inline_p7qy7cCxYD1uz9xg9_540.gif',
              'https://66.media.tumblr.com/350c512200d6cbb6506774f2cddc9641/tumblr_ooonx9vM691qzxv73o1_500.gifv',
              'https://66.media.tumblr.com/666d180e31c743ee35cb0116b05fa31e/tumblr_os8w02LP0B1wq0ygoo1_r5_500.gif',
               ]
    imageURL = (random.choice(hugs))
    embed = discord.Embed(
        title = ctx.message.author.name + " deu um abraço em " + member.name + "...Awwwww!", color=0xcc23b5)
    embed.set_image(url=imageURL)
    await ctx.send( embed = embed )
    
    
@bot.command(name='chorar',
                aliases=['cry', 'choro'])
async def chorar(ctx):
    cry=['https://66.media.tumblr.com/df5dc523b88ae23b6774d0c33fc73f88/tumblr_oogt5durBc1qzxv73o1_500.gif',
          'https://66.media.tumblr.com/7a62299e92bfbe10194ecf7850e0769c/tumblr_okckzleiEg1vh9ej2o1_500.gif',
          'https://66.media.tumblr.com/747687b64eec709e6b12eb0672d49d0b/tumblr_o3fl95DhD51u8mykho1_500.gif',
          'https://66.media.tumblr.com/5d4be9e172a65bbc7e099cf6090f0e0e/tumblr_p1j4i9NJwn1qbvovho1_r1_500.gif',
          'https://66.media.tumblr.com/c75eed23b504e601313a63418122aa96/tumblr_ozba0yZfaf1tydz8to1_500.gif',
          'https://66.media.tumblr.com/5c975b28495e8524499eeb9cf9297255/tumblr_p76z0heVxD1uhe17yo1_500.gif',
          'https://66.media.tumblr.com/5e61db964f5208ceea3d306618eb4bb9/tumblr_omh4pxIVes1ufw8o4o1_540.gif',
          'https://66.media.tumblr.com/7b70108020dc7d970cc56e025a7fd250/tumblr_ohbw3wIP8r1qbvovho1_540.gif',
          'https://66.media.tumblr.com/e9fb46144efc579746e57bcaebd3350a/tumblr_olrmy4djBG1tydz8to1_500.gif',
          'https://www.tumblr.com/search/anime+cry+gif',
          'https://66.media.tumblr.com/c9f735e9b8090beeb25eb8e1f4f1975c/tumblr_p0qnn9WbYu1tydz8to1_500.gif',
          'https://66.media.tumblr.com/c9f735e9b8090beeb25eb8e1f4f1975c/tumblr_p0qnn9WbYu1tydz8to1_500.gif',
          'https://66.media.tumblr.com/25a401be43e92aa5b1fb0c620da7386d/tumblr_ozoo8jkdNc1udouqko1_500.gif',
          'https://66.media.tumblr.com/ab11c52cc2f4ca091454e94196cf5ff7/tumblr_outcxfZAVH1qztgoio1_500.gif',
          'https://66.media.tumblr.com/055958b63177d95012ad334092bcce70/tumblr_pgejn5KwyA1th206io1_500.gif',
]
    imageURL = (random.choice(cry))
    embed = discord.Embed(
        title = ctx.message.author.name + " está triste...")
    embed.set_image(url=imageURL)
    await ctx.send( embed = embed )


@bot.command(name='tapa',
                aliases=['slap', 'bater'])
async def tapa(ctx, member: discord.Member):
    slaps=['https://i.imgur.com/Agwwaj6.gif',
            'https://4.bp.blogspot.com/-YqcMy_yMzdc/XAmdzO7cp5I/AAAAAAABY_0/vjPC2rNMBnYjLyRklhQRgVoR7DtOdjslACKgBGAs/s1600/Omake%2BGif%2BAnime%2B-%2BSeishun%2BButa%2BYarou%2Bwa%2BBunny%2BGirl%2BSenpai%2Bno%2BYume%2Bwo%2BMinai%2B-%2BEpisode%2B10%2B-%2BMai-Nodoka%2BSlaps%2BSakuta.gif',
            'https://66.media.tumblr.com/7f4117e92bed5b2cde593581fe2efcc7/tumblr_ojw26msKoB1vl7ueco3_500.gifv',
            'http://electrohaxz.tk/media/img/anime-images/Nekos/gif/slap/slap_005.gif',
            'https://thumbs.gfycat.com/RigidDismalChevrotain-size_restricted.gif',
            'https://i.kym-cdn.com/photos/images/original/001/264/655/379.gif',
            'https://66.media.tumblr.com/00af342d3838fed0f978b62ff496dfea/tumblr_phizajqDcb1wj1nn0o1_400.gifv',
            'http://electrohaxz.tk/media/img/anime-images/Nekos/gif/slap/slap_006.gif',
            'https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7143c853-3069-4165-8f0e-ec5f99d6e696/dc2j3vi-687c6b82-a84a-4d19-954c-4b4d7c8ab7c7.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzcxNDNjODUzLTMwNjktNDE2NS04ZjBlLWVjNWY5OWQ2ZTY5NlwvZGMyajN2aS02ODdjNmI4Mi1hODRhLTRkMTktOTU0Yy00YjRkN2M4YWI3YzcuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.1B-cXWgfTlpjPFp69UJtyFX7gNxZ-rfBpukevuN3tBQ',
            'http://pa1.narvii.com/5738/dfaf6db236cc6980eb01049ca882ca6b83278486_00.gif',
               ]
    
    falas = ['Hoho! Mas que tapão!',
             'Ouch, vai ficar roxo.',
             'FALCON PUNCHHHHHHH!',
             'Vai ficar vermelho pra caralho!',
             'Você deve ter sido bem idiota.']
        
    imageURL = (random.choice(slaps))
    embed = discord.Embed(
        title = ctx.message.author.name + " deu um tapão em " + member.name + ". " + random.choice(falas), color=0xcc23b5)
    embed.set_image(url=imageURL)
    await ctx.send( embed = embed )
    
@bot.command()
async def avatar(ctx, user: discord.Member):
    imageURL = user.avatar_url
    embed = discord.Embed(color=0xcc23b5)
    embed.set_image(url=imageURL)
    await ctx.send ( embed = embed )
    
@bot.command(name='cafuné',
                aliases=['tap', 'pat', 'carinho', 'cafune'])
async def cafuné(ctx, member: discord.Member):
    pats=['https://media1.tenor.com/images/9d2fb0f144356e03488961407dc69e7d/tenor.gif?itemid=12189180',
          'https://tenor.com/view/anime-tap-shy-blush-re-zero-gif-14319667',
          'https://66.media.tumblr.com/629d0a7a18ce9fd198e99946db4aeffe/tumblr_o42a09vkfQ1ultad9o1_500.gif',
          'https://66.media.tumblr.com/cadf248febe96afdd6869b7a95600abb/tumblr_onjo4cGrZE1vhnny1o1_500.gif',
          'https://66.media.tumblr.com/f97f755456ea4cf141b7c4bc261c88d9/tumblr_npb8yu2BZ41u03wruo1_500.gif',
          'https://66.media.tumblr.com/6289c42ea805f475698f02207da0a377/tumblr_p14hcsxPsb1tm1dgio1_400.gifv',
          'https://66.media.tumblr.com/bde29ae19fa160f0fc7bc8f0dcf5308b/tumblr_n7t4ioLycK1rbnx7io1_500.gif',
          'https://i.imgur.com/TTGJqQR.gif',
          'https://gifimage.net/wp-content/uploads/2017/09/anime-head-pat-gif-9.gif',
          'https://uploads.disquscdn.com/images/3eba80d8b7b79eb74aef0f4410935fbde2b3f02865c026d7ccda052745ccc30d.gif',
          'https://66.media.tumblr.com/674a6801821c90f9f6a398df2184f395/tumblr_oun7zbWzBO1tgebsfo1_400.gifv',
          'https://thumbs.gfycat.com/RawAshamedGermanshorthairedpointer-small.gif',
          'https://data.whicdn.com/images/290352054/original.gif',
          'https://media1.tenor.com/images/0429a52f8e19caf3ca73884a7933baf7/tenor.gif?itemid=14095758',
          'https://memestatic.fjcdn.com/gifs/Headpat+reaction+something+simple+and+cute+i+guess_6d8a65_6488624.gif',
          'https://66.media.tumblr.com/47c21c4b871b53bfd36d86a2ddcef615/tumblr_p9b11ijLuy1th206io1_500.gifv',
          'https://em.wattpad.com/a281ce41599e18b73151a27cce16962f4d8f82a4/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f4c344b75637732677341424b55673d3d2d3438353939323930362e313466313433336162656334306138633331393432353033303734332e676966?s=fit&w=720&h=720',
          'https://media.tenor.com/images/a671268253717ff877474fd019ef73e9/tenor.gif',
          'https://giphy.com/gifs/black-season-ye7OTQgwmVuVy',
          ]
    imageURL = (random.choice(pats))
    embed = discord.Embed(
        title = ctx.message.author.name + " fez carinho em " + member.name + ". Pafu pafu.", color=0xcc23b5)
    embed.set_image(url=imageURL)
    
    await ctx.send( embed = embed )

#Rodar COGS
for cog in os.listdir(".//cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} não pode ser carregado:")
            raise e

#Rodar o Bot            
bot.run(TOKEN)
