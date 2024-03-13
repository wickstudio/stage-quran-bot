# Stage Quran Bot

## Description

This Discord bot is designed to play audio ( quran ) from YouTube playlists in a voice channel. It utilizes the `discord.py` library for interaction with Discord and `yt_dlp` and `pytube` for fetching and streaming YouTube audio.

## Features

- Plays Quran from YouTube playlists in a designated voice channel.
- Automatically reconnects to voice channel if disconnected.
- Supports multiple playlists specified in a JSON file.

## Requirements

- Python 3.6 or higher
- discord.py
- yt_dlp
- pytube

## Installation

1. Clone this repository:

```
git clone https://github.com/wickstudio/stage-quran-bot.git
```

2. Install the required dependencies:

```
pip install -r requirements.txt
```

3. Create a `config.json` file in the root directory and fill in your bot token, server ID, and channel ID in the following format:

```json
{
    "TOKEN": "your_bot_token_here",
    "SERVER_ID": "your_server_id_here",
    "CHANNEL_ID": "your_channel_id_here"
}
```

4. Create a `playlist.json` file in the root directory and specify your playlists as follows:

```json
{
    "reciters": [
        {
            "name": "Reciter Name",
            "playList": "YouTube_Playlist_ID"
        }
    ]
}
```

## Usage

1. Start the bot:

```
python bot.py
```

2. Invite the bot to your Discord server using the generated OAuth link.

3. Ensure that the bot has necessary permissions to join and speak in the designated voice channel.

4. Use the defined command prefix followed by commands to interact with the bot (e.g., `!play`).

## Commands

- `!play`: Starts playing audio from the specified YouTube playlist.
- `!stop`: Stops playing audio and disconnects the bot from the voice channel.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for any suggestions or improvements.

## License

This project is licensed under the [MIT License](LICENSE).