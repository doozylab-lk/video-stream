import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "|ᴅ͢-ᴍᴜsɪᴄ|")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "dhananjayarecord")
ALIVE_NAME = getenv("ALIVE_NAME", "|ᴅʜᴀɴᴀɴᴊᴀYᴀ͜͡ › ͢ᴍᴜsɪᴄ|")
BOT_USERNAME = getenv("BOT_USERNAME", "dhananjayaMegabot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "DhananjayaMadushanka")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "dhananjayabots")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "DhananjayaRobotsFactory")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://www.mediafire.com/view/xqfeqjhtddqs4o1/IMG_20211110_024208_697.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
IMG_1 = getenv("IMG_1", "https://www.mediafire.com/view/xqfeqjhtddqs4o1/IMG_20211110_024208_697.jpg")
IMG_2 = getenv("IMG_2", "https://www.mediafire.com/view/xqfeqjhtddqs4o1/IMG_20211110_024208_697.jpg")
IMG_3 = getenv("IMG_3", "https://www.mediafire.com/view/xqfeqjhtddqs4o1/IMG_20211110_024208_697.jpg")
