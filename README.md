# Discord Music Bot
at Technical Festival Contest, SVNIT'2023

## Overview

This Discord music bot allows users to stream audio from YouTube into voice channels on a Discord server. Built with Python and utilizing `youtube_dl` for audio extraction and `discord.py` for bot interactions, this bot supports a range of commands for managing playback and queues.

## Features

- Join and Leave Voice Channels: Commands to connect the bot to and disconnect it from voice channels.
- Play, Pause, Resume, and Stop Music: Control playback of audio tracks.
- Queue Management: Add songs to a queue and manage the playback sequence.
- Loop Queue: Toggle looping of the entire queue.
- Next and Previous Tracks: Skip to the next or previous track in the queue.
- Command Listing: Retrieve a list of all available commands.

## Technologies

- Python: Programming language used for development.
- discord.py: Library for interacting with the Discord API.
- youtube_dl: Tool for extracting audio from YouTube.
- FFmpeg: Framework for handling multimedia data.
- Replit: Platform for deploying and running the bot.

## Setup

1. Clone the Repository:

   ```bash
   git clone https://github.com/Dharmil2684/Discord-Music-Bot
   cd Discord-Music-Bot

2. Install Dependencies:

 Make sure you have Python 3.8+ installed, then install the required packages:

   ```bash
   pip install -r requirements.txt
   ```
   
3. Configure the Bot:

 Replace the placeholder token in the `bot.run()` line with your Discord bot token:

   ```python
   bot.run("YOUR_DISCORD_BOT_TOKEN")
   ```

4. Run the Bot:

 Start the bot using:

   ```bash
   python bot.py
   ```

## Error Handling

If you encounter the error "Unable to extract uploader ID" during runtime, refer to this [Stack Overflow solution](https://stackoverflow.com/questions/75495800/error-unable-to-extract-uploader-id-youtube-discord-py) for troubleshooting and resolution.

## Commands

- `!join`: Connect the bot to your voice channel.
- `!leave`: Disconnect the bot from the voice channel.
- `!play <url>`: Add a song to the queue and play it.
- `!pause`: Pause the current track.
- `!resume`: Resume playback of a paused track.
- `!stop`: Stop playback and clear the queue.
- `!queue <url>`: Add a song to the queue.
- `!loop`: Toggle looping of the queue.
- `!next`: Play the next song in the queue.
- `!previous`: Play the previous song in the queue.
- `!commands`: List all available commands.

## Contact

For any questions or issues, please reach out to
[dharmilhalpatics12@gmai.com] .
