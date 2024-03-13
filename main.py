import discord
from discord.ext import commands
import json
import yt_dlp
from discord import PCMVolumeTransformer, FFmpegPCMAudio
import asyncio
from pytube import Playlist


TOKEN = ''
SERVER_ID = ''
CHANNEL_ID = ''

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

with open('playlist.json', 'r') as f:
    playlists = json.load(f)

async def get_voice_client(force_reconnect=False):
    guild = bot.get_guild(int(SERVER_ID))
    if guild is None:
        print("Guild not found.")
        return None
    channel = guild.get_channel(int(CHANNEL_ID))
    if channel and isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
        if force_reconnect and guild.voice_client:
            await guild.voice_client.disconnect()
        if channel.permissions_for(guild.me).connect:
            voice_client = await channel.connect()
            await guild.me.edit(suppress=False)
            return voice_client
        else:
            print("Bot does not have permission to connect to the channel.")
            return None
    else:
        print("Channel is not a voice or stage channel, or CHANNEL_ID not provided.")
        return None

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} | discord.gg/wicks')
    voice_client = await get_voice_client()
    if voice_client:
        await play_playlist(voice_client, playlists)


async def get_playlist_urls(playlist_url):
    playlist = Playlist(playlist_url)
    urls = list(playlist.video_urls)
    return urls


def download_youtube_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": False,
        "yesplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        return audio_url


async def play_playlist(voice_client:discord.VoiceClient, playlists):
    while True:
        for reciter in playlists['reciters']:
            playlist_id = reciter['playList']
            urls = await get_playlist_urls(f'https://www.youtube.com/playlist?list={playlist_id}')
            for url in urls:
                if not voice_client or not voice_client.is_connected():
                    voice_client = await get_voice_client(force_reconnect=True)
                    if not voice_client:
                        print("Failed to reconnect.")
                        return
                try:
                    audio_url = download_youtube_audio(url)
                    ffmpeg_options = {
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn',
                    }
                    source = FFmpegPCMAudio(audio_url, **ffmpeg_options)
                    voice_client.play(PCMVolumeTransformer(source))
                    while voice_client.is_playing() or voice_client.is_paused():
                        await asyncio.sleep(1)
                except Exception as e:
                    print(f"Error playing URL {url}: {e}")
                continue

bot.run(TOKEN)
