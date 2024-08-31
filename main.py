import asyncio
import discord
from discord.ext import commands
import youtube_dl

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)

bot.bot_data = {'queue': [], 'loop_queue': False}

FFMPEG_OPTIONS = {
  'before_options':
  '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn'
}

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
  'format': 'bestaudio/best',
  'restrictfilenames': True,
  'noplaylist': True,
  'extractor_retries': 'auto',
  'nocheckcertificate': True,
  'ignoreerrors': False,
  'logtostderr': False,
  'quiet': True,
  'no_warnings': True,
  'default_search': 'auto',
  'source_address':
  '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes 
}

ffmpeg_options = {'options': '-vn'}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def get_voice_client(guild):
  if not guild:
    return None
  voice_client = guild.voice_client
  if not voice_client:
    return None
  return voice_client


@bot.command(name='join')
async def join(ctx):
  if not ctx.author.voice:
    await ctx.send("You are not connected to a voice channel.")
    return
  voice_channel = ctx.author.voice.channel
  await voice_channel.connect()


@bot.command(name='leave')
async def leave(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  await voice_client.disconnect()
  await ctx.send("Left the voice channel.")


@bot.command(name='play')
async def play(ctx, queue_index=None):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  if 'queue' not in bot.bot_data or not bot.bot_data['queue']:
    await ctx.send("The queue is empty.")
    return
  async with ctx.typing():
    if queue_index is None:
      current_queue_index = bot.bot_data.get('current_queue_index', 0)
    else:
      try:
        current_queue_index = int(queue_index) - 1
      except ValueError:
        await ctx.send("Invalid queue index.")
        return
    if current_queue_index >= len(bot.bot_data['queue']):
      await ctx.send("Invalid queue index.")
      return
    queue_item = bot.bot_data['queue'][current_queue_index]
    user_id, info = queue_item
    source = discord.PCMVolumeTransformer(
      discord.FFmpegPCMAudio(info['url'], **ffmpeg_options))
    voice_client.play(source)
    bot.bot_data['current_queue_index'] = current_queue_index + 1
  await ctx.send(f"Now playing: {info['title']} (requested by <@{user_id}>)")


@bot.command(name='pause')
async def pause(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  if voice_client.is_playing():
    voice_client.pause()
    await ctx.send("Paused.")
  else:
    await ctx.send("Not playing anything.")


@bot.command(name='resume')
async def resume(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  if voice_client.is_paused():
    voice_client.resume()
    await ctx.send("Resumed.")
  else:
    await ctx.send("Not paused.")


@bot.command(name='stop')
async def stop(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  voice_client.stop()
  await ctx.send("Stopped.")


@bot.command(name='queue')
async def queue(ctx, url):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  async with ctx.typing():
    try:
      info = await asyncio.to_thread(ytdl.extract_info, url, download=False)
      source = discord.PCMVolumeTransformer(
        discord.FFmpegPCMAudio(info['url'], **ffmpeg_options))
    except youtube_dl.DownloadError:
      await ctx.send("Failed to download the song.")
      return
    if 'queue' not in bot.bot_data:
      bot.bot_data['queue'] = []
    bot.bot_data['queue'].append((ctx.author.id, info))
  await ctx.send(f"Queued: {info['title']}")


#loop


@bot.command(name='loop')
async def loop(ctx):
  bot.bot_data['loop_queue'] = not bot.bot_data['loop_queue']
  await ctx.send(
    f"Queue looping {'enabled' if bot.bot_data['loop_queue'] else 'disabled'}."
  )


#next
@bot.command(name='next')
async def next(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  if 'queue' not in bot.bot_data or not bot.bot_data['queue']:
    await ctx.send("The queue is empty.")
    return
  if bot.bot_data.get('current_queue_index', 0) >= len(bot.bot_data['queue']):
    await ctx.send("End of queue.")
    return
  bot.bot_data['current_queue_index'] += 1
  if bot.bot_data['loop_queue'] and bot.bot_data['current_queue_index'] == len(
      bot.bot_data['queue']):
    bot.bot_data['current_queue_index'] = 0
  voice_client.stop()
  await play(ctx, str(bot.bot_data['current_queue_index']))


#previous
@bot.command(name='previous')
async def previous(ctx):
  voice_client = get_voice_client(ctx.guild)
  if not voice_client:
    await ctx.send("Not connected to a voice channel.")
    return
  if 'queue' not in bot.bot_data or not bot.bot_data['queue']:
    await ctx.send("The queue is empty.")
    return
  async with ctx.typing():
    current_queue_index = bot.bot_data.get('current_queue_index', 0)
    if current_queue_index <= 1:
      await ctx.send("No previous song.")
      return
    queue_item = bot.bot_data['queue'][current_queue_index - 2]
    user_id, info = queue_item
    source = discord.PCMVolumeTransformer(
      discord.FFmpegPCMAudio(info['url'], **ffmpeg_options))
    voice_client.stop()
    voice_client.play(source)
    bot.bot_data['current_queue_index'] = current_queue_index - 1
  await ctx.send(f"Now playing: {info['title']} (requested by <@{user_id}>)")


#commands
@bot.command(name='commands', help='List all available commands')
async def list_commands(ctx):
  commands_list = []
  for command in bot.commands:
    commands_list.append(command.name)
  await ctx.send(
    f"Here is a list of all the available commands:\n```{', '.join(commands_list)}```"
  )


if __name__ == "__main__":
  bot.run(
    "")
