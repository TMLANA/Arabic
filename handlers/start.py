from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_USER
from config import MUSIC_USER
from config import MUSIC_NAME

@Client.on_message(filters.command("start") & filters.private & ~filters.channel)
async def start(_, message: Message):
    await message.reply_text(
        text=f"• **اهلا بك عزيزي** : {message.from_user.mention}!**\n- في بوت تشغيل الاغاني في المكالمات الجماعيه\n- قم برفعي  مشرف في مجموعتك مع الحساب المساعد : [{MUSIC_NAME}](https://t.me/{MUSIC_USER})\n\n• **ارسل** : `/الاوامر` **لتعلم كيفية الاستعمال** .",
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton("•  اضفني في مجموعتك •", url=f"https://t.me/{MUSIC_USER}?startgroup=true")
            ]]
        ),
        disable_web_page_preview=True
    )
        
@Client.on_message(filters.command("تفعيل") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        text=f"• **تم تفعيل البوت بنجاح** .\n• **الحساب المساعد** : [{MUSIC_NAME}](https://t.me/{MUSIC_USER})",
        reply_markup=InlineKeyboardMarkup(
            [[
            InlineKeyboardButton(text="• قناة البوت •", url="https://t.me/vvvvisn")
            ]]
        ),
        disable_web_page_preview=True
    )


@Client.on_message(filters.command(["الاوامر", "help"]) & ~filters.channel)
async def cmdlist(_, message: Message):
    await message.reply_text(
        text=f"• **قائمة اوامر بوت الاغاني** : \n\n- /تشغيل + اسم الاغنيه\n- /صوت + اسم الاغنيه\n- /فيديو + اسم الاغنيه\n- /الاغاني : لعرض قائمة الاغاني\n- /الاغنيه : لعرض الاغنيه المبثوثه\n\n- /التحكم : للتحكم بقائمة الاغاني\n- /ايقاف : لأيقاف الاغنيه مؤقتا\n- /استمرار : لأكمال تشغيل الاغاني\n- /انهاء : لأيقاف جميع الاغاني\n- /غادر : لمغادرة البوت المساعد\n- /انضم : لانضمام البوت المساعد\n- /تحديث : لتحديث قائمة المشرفين\n\n• **الحساب المساعد** : [{MUSIC_NAME}](https://t.me/{MUSIC_USER})",
        reply_markup=InlineKeyboardMarkup(
              [[
              InlineKeyboardButton(text="• قناة البوت •", url="https://t.me/vvvvisn")
              ]]
          )
      )
