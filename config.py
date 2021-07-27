from os import getenv
from dotenv import load_dotenv
load_dotenv()
que = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_USER = getenv("BOT_USER", "Dev_Prox")
MUSIC_USER = getenv("MUSIC_USER", "Dev_Prox")
MUSIC_NAME = getenv("MUSIC_NAME", "Music Bot")
admins = {}
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "10"))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "218385683").split()))
