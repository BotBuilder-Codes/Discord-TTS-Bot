import os

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')  # Must be set in environment
COMMAND_PREFIX = '!'

# TTS Configuration
DEFAULT_TTS_LANGUAGE = 'en'
DEFAULT_TTS_PROVIDER = 'google'  # Options: google, aws, azure

SUPPORTED_LANGUAGES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'en-au': 'English (Australia)',
    'en-ca': 'English (Canada)',
    'en-gb': 'English (UK)',
    'en-gh': 'English (Ghana)',
    'en-ie': 'English (Ireland)',
    'en-in': 'English (India)',
    'en-ng': 'English (Nigeria)',
    'en-nz': 'English (New Zealand)',
    'en-ph': 'English (Philippines)',
    'en-tz': 'English (Tanzania)',
    'en-uk': 'English (UK)',
    'en-us': 'English (US)',
    'en-za': 'English (South Africa)',
    'es': 'Spanish',
    'es-es': 'Spanish (Spain)',
    'es-us': 'Spanish (United States)',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'fr-ca': 'French (Canada)',
    'fr-fr': 'French (France)',
    'gu': 'Gujarati',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'jw': 'Javanese',
    'km': 'Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'la': 'Latin',
    'lv': 'Latvian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'my': 'Myanmar (Burmese)',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pt-br': 'Portuguese (Brazil)',
    'pt-pt': 'Portuguese (Portugal)',
    'ro': 'Romanian',
    'ru': 'Russian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'su': 'Sundanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh-cn': 'Chinese (Mandarin/China)',
    'zh-tw': 'Chinese (Mandarin/Taiwan)',
}

AUDIO_FOLDER = 'temp_audio'

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'DEBUG'