from discord.ext import commands
from utils.logger import setup_logger
import discord

logger = setup_logger(__name__)

class CommandHandler(commands.Cog):
    def __init__(self, bot, tts_manager, voice_handler):
        self.bot = bot
        self.tts_manager = tts_manager
        self.voice_handler = voice_handler

    @commands.command(name='join', help='Joins a voice channel')
    async def join(self, ctx):
        """Join the user's voice channel"""
        if not ctx.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return

        await self.voice_handler.join_channel(ctx.author.voice.channel)
        await ctx.send(f"Joined {ctx.author.voice.channel.name}")

    @commands.command(name='leave', help='Leaves the voice channel')
    async def leave(self, ctx):
        """Leave the current voice channel"""
        if self.voice_handler.voice_client:
            await self.voice_handler.leave_channel()
            await ctx.send("Left the voice channel")
        else:
            await ctx.send("I'm not in a voice channel")

    @commands.command(name='lang', help='Changes TTS language')
    async def change_language(self, ctx, lang_code=None):
        """Change TTS language for the user"""
        from config import SUPPORTED_LANGUAGES

        if not lang_code:
            # Group languages by region/type
            langs = []
            for code, name in SUPPORTED_LANGUAGES.items():
                langs.append(f"{code}: {name}")

            # Split into multiple messages if too long
            lang_chunks = [langs[i:i + 20] for i in range(0, len(langs), 20)]

            await ctx.send("Available languages:")
            for chunk in lang_chunks:
                await ctx.send("```\n" + "\n".join(chunk) + "\n```")
            return

        if lang_code not in SUPPORTED_LANGUAGES:
            await ctx.send(f"Unsupported language code. Use `!lang` to see available languages")
            return

        # Set language for this specific user
        self.tts_manager.set_language(str(ctx.author.id), lang_code)
        await ctx.send(f"Your TTS language has been set to {SUPPORTED_LANGUAGES[lang_code]}")

    @commands.command(name='commands', help='Shows all available commands')
    async def show_commands(self, ctx):
        """Show available commands"""
        commands = [
            "**!join** - Join your voice channel",
            "**!leave** - Leave the voice channel",
            "**!lang [code]** - Change your TTS language or list available languages",
            "**!commands** - Show this message"
        ]

        embed = discord.Embed(
            title="TTS Bot Commands",
            description="\n".join(commands),
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot, tts_manager, voice_handler):
    """Set up the commands cog"""
    await bot.add_cog(CommandHandler(bot, tts_manager, voice_handler))