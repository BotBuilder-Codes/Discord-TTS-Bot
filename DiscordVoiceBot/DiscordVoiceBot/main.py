import asyncio
import discord
from discord.ext import commands
import os
from config import *
from bot.voice_handler import VoiceHandler
from bot.tts_manager import TTSManager
from bot.command_handler import setup as setup_commands
from utils.logger import setup_logger
from webserver import keep_alive

# Set up logging
logger = setup_logger(__name__)

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)  # Disable default help command

# Initialize managers
voice_handler = None
tts_manager = None

@bot.event
async def on_ready():
    """Handle bot startup"""
    global voice_handler, tts_manager

    voice_handler = VoiceHandler(bot)
    tts_manager = TTSManager()

    # Set up commands
    await setup_commands(bot, tts_manager, voice_handler)

    logger.info(f'Bot is ready: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!commands for help"))

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    try:
        # Process commands first
        await bot.process_commands(message)

        # Ignore bot messages and commands
        if message.author == bot.user or message.content.startswith(COMMAND_PREFIX):
            logger.info(f"Ignoring bot's own message or command")
            return

        # Get the author's voice state
        author_voice = message.author.voice
        if not author_voice or not author_voice.channel:
            logger.debug(f"User {message.author.name} is not in any voice channel")
            return

        logger.info(f"Processing message from {message.author.name} in {message.channel.name}")
        logger.info(f"Message content: {message.clean_content}")

        # Join voice channel if needed
        logger.info(f"Attempting to join voice channel: {author_voice.channel.name}")
        await voice_handler.join_channel(author_voice.channel)

        # Create TTS file with user information
        logger.info("Generating TTS file...")
        tts_file = await tts_manager.create_tts(
            message.clean_content,
            str(message.author.id),
            message.author.display_name
        )
        logger.info(f"TTS file generated: {tts_file}")

        # Play the audio
        logger.info("Attempting to play audio...")
        await voice_handler.play_audio(tts_file)
        logger.info("Audio playback completed")

        # Cleanup
        logger.info("Cleaning up TTS file...")
        tts_manager.cleanup_file(tts_file)

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)

@bot.event
async def on_voice_state_update(member, before, after):
    """Handle voice state changes"""
    try:
        # Check if bot should disconnect
        if voice_handler and voice_handler.current_channel:
            # Get all members in the voice channel
            members_in_channel = voice_handler.current_channel.members

            # If bot is alone or no one is in the channel
            if len(members_in_channel) <= 1:
                await voice_handler.leave_channel()
                logger.info("Bot left voice channel - no users present")

    except Exception as e:
        logger.error(f"Error handling voice state update: {str(e)}")

def main():
    """Main entry point"""
    try:
        # Start the keep-alive webserver
        keep_alive()

        # Verify token is set
        if not DISCORD_TOKEN:
            raise ValueError("Discord token not set in environment variables")

        # Start the bot
        bot.run(DISCORD_TOKEN)

    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()