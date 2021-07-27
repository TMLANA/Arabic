from callsmusic.callsmusic import client as USER
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import config
from config import BOT_USER
from config import MUSIC_USER
from config import MUSIC_NAME
from pyrogram.errors import UserAlreadyParticipant
from helpers.decorators import errors, authorized_users_only

@Client.on_message(filters.group & filters.command(["انضمام","دخول","انضم","ادخل"]))
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "• <b>قم برفعي مشرف في هذه المجموعه اولا</b> !",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name =  "Music"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id,"• **تم انضمامي لهذه المجموعه** .")
    except UserAlreadyParticipant:
        await message.reply_text(
            "• <b>الحساب المساعد بالتاكيد في هذه المجموعه</b> .",
        )
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"• <b>لقد حدث خطا اثناء انضمام الحساب المساعد</b> !\n- يرجى التاكد ان الحساب المساعد غير محظور من المجموعه \n- او قم باضافته يدويا الى هنا : @{MUSIC_USER}",
        )
        return
    #await message.reply_text("<b>helper userbot joined your chat</b>")
    
@USER.on_message(filters.group & filters.command(["غادر"]))
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:  
        await message.reply_text(
            f"• <b>لقد حدث خطا اثناء مغادرة الحساب المساعد</b> !\n- قم بطرده يدويا من هنا لحل المشكله",
        )
        return
