import os
import asyncio
import time
import re
from gtts import gTTS
import tempfile
from utils.logger import setup_logger
from config import DEFAULT_TTS_LANGUAGE, SUPPORTED_LANGUAGES

logger = setup_logger(__name__)

class TTSManager:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.user_languages = {}  # Store language preferences per user
        self.last_message_time = {}  # Store last message timestamp per user
        self.USERNAME_COOLDOWN = 20  # Cooldown in seconds
        logger.info(f"Initialized TTS Manager with temp directory: {self.temp_dir}")

    def set_language(self, user_id: str, lang_code: str):
        """Set TTS language for a specific user"""
        if lang_code in SUPPORTED_LANGUAGES:
            self.user_languages[user_id] = lang_code
            logger.info(f"Language set to: {lang_code} for user: {user_id}")
        else:
            raise ValueError(f"Unsupported language: {lang_code}")

    def get_user_language(self, user_id: str) -> str:
        """Get the language setting for a specific user"""
        return self.user_languages.get(user_id, DEFAULT_TTS_LANGUAGE)

    def _clean_username(self, username: str) -> str:
        """Remove emojis and make username lowercase"""
        # Remove emojis and other special characters
        username = re.sub(r'[^\w\s-]', '', username)
        # Convert to lowercase
        username = username.lower()
        # Remove extra spaces and strip
        username = ' '.join(username.split())
        return username

    def _should_say_username(self, user_id: str) -> bool:
        """Check if we should say the username based on cooldown"""
        current_time = time.time()
        last_time = self.last_message_time.get(user_id, 0)

        # Update last message time
        self.last_message_time[user_id] = current_time

        # Check if enough time has passed
        return (current_time - last_time) >= self.USERNAME_COOLDOWN

    async def create_tts(self, text: str, user_id: str, username: str):
        """
        Create a TTS file from text and return the filepath
        """
        try:
            # Get user's preferred language
            lang = self.get_user_language(user_id)

            # Clean username and check cooldown
            clean_username = self._clean_username(username)
            should_say_username = self._should_say_username(user_id)

            # Create the full text with or without username
            full_text = f"{clean_username} said, {text}" if should_say_username else text

            # Generate temporary filename
            temp_file = os.path.join(self.temp_dir, f'speech_{hash(text)}.mp3')

            logger.info(f"Generating TTS for text: {full_text[:50]}... in language: {lang}")

            # Use run_in_executor to prevent blocking
            await asyncio.get_event_loop().run_in_executor(
                None,
                self._generate_tts,
                full_text,
                lang,
                temp_file
            )

            # Verify file was created
            if not os.path.exists(temp_file):
                raise Exception("TTS file was not created")

            logger.info(f"TTS file created successfully: {temp_file}")
            return temp_file

        except Exception as e:
            logger.error(f"Error creating TTS: {str(e)}")
            raise

    def _generate_tts(self, text: str, language: str, filepath: str):
        """
        Generate TTS file (runs in executor)
        """
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(filepath)
            logger.debug(f"TTS generation completed for file: {filepath}")
        except Exception as e:
            logger.error(f"Error in TTS generation: {str(e)}")
            raise

    def cleanup_file(self, filepath):
        """
        Remove temporary TTS file
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"Cleaned up file: {filepath}")
        except Exception as e:
            logger.error(f"Error cleaning up file {filepath}: {str(e)}")