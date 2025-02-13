import asyncio
import discord
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VoiceHandler:
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.is_playing = False
        self.current_channel = None

    async def join_channel(self, channel):
        """
        Join a voice channel
        """
        try:
        # Check if the TTS bot is in the target channel
            tts_bot_id = 513423712582762502
            if any(member.id == tts_bot_id for member in channel.members):
                logger.info(f"TTS bot is present in {channel.name}, skipping connection.")
                return
             
            if self.voice_client and self.voice_client.is_connected():
                if self.current_channel == channel:
                    return
                await self.voice_client.move_to(channel)
            else:
                self.voice_client = await channel.connect()
            self.current_channel = channel
            # Add small delay to ensure connection is fully established
            await asyncio.sleep(1)
            logger.info(f"Joined voice channel: {channel.name}")
        except Exception as e:
            logger.error(f"Error joining voice channel: {str(e)}")
            raise

    async def leave_channel(self):
        """
        Leave the current voice channel
        """
        try:
            if self.voice_client and self.voice_client.is_connected():
                await self.voice_client.disconnect()
                self.voice_client = None
                self.current_channel = None
                logger.info("Left voice channel")
        except Exception as e:
            logger.error(f"Error leaving voice channel: {str(e)}")

    async def play_audio(self, audio_file):
        """
        Play audio file in voice channel
        """
        try:
            if not self.voice_client or not self.voice_client.is_connected():
                logger.warning("No voice client available or not connected")
                return

            # Wait if already playing
            while self.is_playing:
                await asyncio.sleep(0.1)

            self.is_playing = True

            # Create FFmpeg audio source with specific options
            audio_source = discord.FFmpegPCMAudio(
                audio_file,
                options='-loglevel warning'
            )

            def after_playing(error):
                self.is_playing = False
                if error:
                    logger.error(f"Error playing audio: {str(error)}")

            # Add volume transformer to ensure adequate volume
            transformed_source = discord.PCMVolumeTransformer(audio_source, volume=1.0)
            self.voice_client.play(transformed_source, after=after_playing)

            # Wait until audio finishes playing
            while self.is_playing:
                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Error playing audio: {str(e)}")
            self.is_playing = False
            raise