from os import path
from typing import Dict
from pyrogram import Client
from pyrogram.types import Message, Voice
from typing import Callable, Coroutine, Dict, List, Tuple, Union
from callsmusic import callsmusic, queues
from helpers.admins import get_administrators
from os import path
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
from pyrogram import filters, emoji
from pyrogram.types import InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors.exceptions.flood_420 import FloodWait
import traceback
import os
import sys
from callsmusic.callsmusic import client as USER
from pyrogram.errors import UserAlreadyParticipant
import converter
from downloaders import youtube
import config

from config import BOT_USER
from config import MUSIC_USER
from config import MUSIC_NAME
from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from cache.admins import admins as a
import os
import aiohttp
import aiofiles
import ffmpeg
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from config import que
from Python_ARQ import ARQ
from pyrogram.errors import UserNotParticipant
import json
import wget
chat_id = None

def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer('• عذرا ليس لديك صلاحية التحكم لهذا الامر ! .', show_alert=True)
            return
    return decorator                                                                       
                                          
                                          
                                          
                                          
def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(
    filters.command("الاغاني")
    & filters.group
    & ~ filters.edited
)
async def playlist(client, message):
    global que
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("• **لاتوجد اغاني في القائمه** !")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style='md')
    msg = "• **المجموعه** : `{}`".format(message.chat.title)
    msg += "\n- يتم تشغيل : " + now_playing
    msg += "\n- بواسطة : " + by
    temp.pop(0)
    if temp:
        msg += '\n\n'
        msg += "• **قائمة الانتضار** : "
        for song in temp:
            name = song[0]
            usr = song[1].mention(style='md')
            msg += f'\n- {name}'
            msg += f"\n- بواسطة : {usr}\n"
    await message.reply_text(msg)       
    
# ============================= Settings =========================================

def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
    #if chat.id in active_chats:
        stats = '• **المجموعه** : `{}`'.format(chat.title)
        if len(que) > 0:
            stats += '\n\n'
            stats += '- مستوى الصوت : {}%\n'.format(vol)
            stats += '- عدد الاغاني المنتضره : `{}`\n'.format(len(que))
            stats += '- يتم تشغيل : **{}**\n'.format(queue[0][0])
            stats += '- بواسطة : {}'.format(queue[0][1].mention)
    else:
        stats = None
    return stats

def r_ply(type_):
    if type_ == 'play':
        ico = '▶'
    else:
        ico = '⏸'
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('⏹', 'leave'),
                InlineKeyboardButton('⏸', 'puse'),
                InlineKeyboardButton('▶️', 'resume'),
                InlineKeyboardButton('⏭', 'skip')
                
            ],
            [
                InlineKeyboardButton('• قائمة الاغاني •', 'playlist'),
                
            ],
            [       
                InlineKeyboardButton("• اغلاق •",'cls')
            ]        
        ]
    )
    return mar

@Client.on_message(
    filters.command("الاغنيه")
    & filters.group
    & ~ filters.edited
)
async def ee(client, message):
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        await message.reply(stats)              
    else:
        await message.reply("• **لاتوجد اغاني مشغله هنا** !")

@Client.on_message(
    filters.command("التحكم")
    & filters.group
    & ~ filters.edited
)
@authorized_users_only
async def settings(client, message):
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply('pause'))
            
        else:
            await message.reply(stats, reply_markup=r_ply('play'))
    else:
        await message.reply("• **لاتوجد اغاني مشغله هنا** !")

@Client.on_callback_query(filters.regex(pattern=r'^(playlist)$'))
@Client.on_callback_query(filters.regex(pattern=r'^(playlist)$'))
async def p_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat
    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'playlist':           
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('Player is idle')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "• **المجموعه** : `{}`".format(cb.message.chat.title)
        msg += "\n- يتم تشغيل : "+ now_playing
        msg += "\n- بواسطة : "+by
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg += '• **قائمة الانتضار** : '
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n- {name}'
                 msg += f'\n- بواسطة : {usr}\n'
        await cb.message.edit(msg)      

@Client.on_callback_query(filters.regex(pattern=r'^(play|pause|skip|leave|puse|resume|menu|cls)$'))
@cb_admin_check
async def m_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    the_data = cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == 'pause':
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chat_id] == 'paused'
                ):
            await cb.answer('• لايوجد اتصال لهذه الاغنيه . !', show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer('• تم ايقاف الاغنيه . !')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('play'))
                

    elif type_ == 'play':       
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chat_id] == 'playing'
            ):
                await cb.answer('• لايوجد اتصال لهذه الاغنيه . !', show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer('• تم تشغيل الاغنيه . !')
            await cb.message.edit(updated_stats(m_chat, qeue), reply_markup=r_ply('pause'))
                     

    elif type_ == 'playlist':
        queue = que.get(cb.message.chat.id)
        if not queue:   
            await cb.message.edit('• لاتوجد اغاني في القائمه . !')
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style='md')
        msg = "• **المجموعه** : `{}`".format(cb.message.chat.title)
        msg += "\n- يتم تشغيل : "+ now_playing
        msg += "\n- بواسطة : "+by
        temp.pop(0)
        if temp:
             msg += '\n\n'
             msg += '• **قائمة الانتضار** : '
             for song in temp:
                 name = song[0]
                 usr = song[1].mention(style='md')
                 msg += f'\n- {name}'
                 msg += f'\n- بواسطة : {usr}\n'
        await cb.message.edit(msg)      
                      
    elif type_ == 'resume':     
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
            ) or (
                callsmusic.pytgcalls.active_calls[chat_id] == 'playing'
            ):
                await cb.answer('• لايوجد اتصال لهذه الاغنيه او انها بالفعل مشغله . !', show_alert=True)
        else:
            callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.answer('• تم استمرار تشغيل الاغنيه .. .')     
    elif type_ == 'puse':         
        if (
            chat_id not in callsmusic.pytgcalls.active_calls
                ) or (
                    callsmusic.pytgcalls.active_calls[chat_id] == 'paused'
                ):
            await cb.answer('• لايوجد اتصال لهذه الاغنيه او انها بالفعل متوقفه . !', show_alert=True)
        else:
            callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer('• تم ايقاف الاغنيه . !')
    elif type_ == 'cls':          
        await cb.answer('• تم اغلاق لوحة التحكم . !')
        await cb.message.delete()       

    elif type_ == 'menu':  
        stats = updated_stats(cb.message.chat, qeue)  
        await cb.answer('• تم فتح لوحة التحكم . !')
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⏹', 'leave'),
                    InlineKeyboardButton('⏸', 'puse'),
                    InlineKeyboardButton('▶️', 'resume'),
                    InlineKeyboardButton('⏭', 'skip')
                
                ],
                [
                    InlineKeyboardButton('• قائمة الاغاني • ', 'playlist'),
                
                ],
                [       
                    InlineKeyboardButton("• اغلاق •",'cls')
                ]        
            ]
        )
        await cb.message.edit(stats, reply_markup=marr) 
    elif type_ == 'skip':        
        if qeue:
            skip = qeue.pop(0)
        if chat_id not in callsmusic.pytgcalls.active_calls:
            await cb.answer('• لايوجد اتصال لهذه الاغنيه . !', show_alert=True)
        else:
            callsmusic.queues.task_done(chat_id)

            if callsmusic.queues.is_empty(chat_id):
                callsmusic.pytgcalls.leave_group_call(chat_id)
                
                await cb.message.edit('• **لاتوجد اغاني في القائمه** !\n- تم اغلاق الاتصال .')
            else:
                callsmusic.pytgcalls.change_stream(
                    chat_id,
                    callsmusic.queues.get(chat_id)["file"]
                )
                await cb.answer('Skipped')
                await cb.message.edit((m_chat, qeue), reply_markup=r_ply(the_data))
                await cb.message.reply_text(f'• **تم تخطي** : ({skip[0]})\n• **تم تشغيل** : ({qeue[0][0]})')

    else:      
        if chat_id in callsmusic.pytgcalls.active_calls:
            try:
                callsmusic.queues.clear(chat_id)
            except QueueEmpty:
                pass

            callsmusic.pytgcalls.leave_group_call(chat_id)
            await cb.message.edit('Successfully Left the Chat!')
        else:
            await cb.answer('• لايوجد اتصال هنا . !', show_alert=True)

@Client.on_message(command("تشغيل") & other_filters)
async def play(_, message: Message):
    global que
    lel = await message.reply("• **جار التحميل** .. .")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name =  "الحساب المساعد"
    usar = user
    wew = usar.id
    try:
        #chatdetails = await USER.get_chat(chid)
        lmoa = await _.get_chat_member(chid,wew)
    except:
           for administrator in administrators:
                      if administrator == message.from_user.id:  
                          try:
                              invitelink = await _.export_chat_invite_link(chid)
                          except:
                              await lel.edit(
                                  "• <b>قم برفعي مشرف في هذه المجموعه اولا</b> !",
                              )
                              return

                          try:
                              await USER.join_chat(invitelink)
                              await USER.send_message(message.chat.id,"• **لقد قمت بالانضمام لهذه المجموعه لتشغيل الاغاني** .")
                              await lel.edit(
                                  "• <b>تم دخول الحساب المساعد بنجاح</b> .",
                              )

                          except UserAlreadyParticipant:
                              pass
                          except Exception as e:
                              #print(e)
                              await lel.edit(
                                  f"• <b>لقد حدث خطا اثناء انضمام الحساب المساعد</b> !\n- يرجى التاكد ان الحساب المساعد غير محظور من المجموعه \n- او قم باضافته يدويا الى هنا : @{MUSIC_USER}",
                              )
                              pass
    try:
        chatdetails = await USER.get_chat(chid)
        #lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"• <b>عذرا يجب عليك اضافة</b> : @{MUSIC_USER} <b>ورفعه مشرف مع صلاحية ادارة المحادثات الصوتيه</b> !"
        )
        return     
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name
    await lel.edit("• **جار البحث عن الاغنيه** . ..")
    sender_id = message.from_user.id
    user_id = message.from_user.id
    sender_name = message.from_user.first_name
    user_name = message.from_user.first_name
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    await lel.edit("• **جار تحميل النتائج** .. .")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        await lel.edit("• **لم يتم العثور على نتائج للبحث قم باعادة المحاوله وتهجئة النص بشكل صحيح** !")
        print(str(e))
        return

    keyboard = InlineKeyboardMarkup(
            [   
                [
                               
                    InlineKeyboardButton('• قائمة الاغاني •', callback_data='playlist'),
                    InlineKeyboardButton('• التحكم •', callback_data='menu')
                
                ],                     
                [
                    InlineKeyboardButton('• اغلاق •', callback_data='cls')
                
                ]                             
            ]
        )
    requested_by = message.from_user.first_name
    await generate_cover(requested_by, title, views, duration, thumbnail)  
    file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        qeue = que.get(message.chat.id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await message.reply_text(
        text=f"• **تم اضافة الاغنيه في الدور** #{position} .",
        reply_markup=keyboard
    )
        return await lel.delete()
    else:
        chat_id = message.chat.id
        que[chat_id] = []
        qeue = que.get(message.chat.id)
        s_name = title            
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]      
        qeue.append(appendable)
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
    await message.reply_text(
        text=f"• **تم تشغيل الاغنيه بنجاح** \n- بواسطة : {message.from_user.mention()}",
        reply_markup=keyboard,
        disable_web_page_preview=True
    ),
    )
        return await lel.delete()

# Have u read all. If read RESPECT :-)
