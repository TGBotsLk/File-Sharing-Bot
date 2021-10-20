#(©)Codexbotz

import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, START_MSG, OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON
from helper_func import subscribed, encode, decode, get_messages_one, get_messages_two, get_messages_three

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    text = message.text
    if len(text)>7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                ids = [int(argument[1])]
                channel = f"-100{int(argument[2])}"
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            if channel == "1505653053":
                messages = await get_messages_one(client, ids)
            elif channel == "1577630215":
                messages = await get_messages_two(client, ids)
            else:
                messages = await get_messages_three(client, ids)
                
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🎬 Join Our Movie Group", url="https://t.me/joinchat/Q1uroGQ645U1OTg1"),
                ]
            ]
            )

            try:
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await msg.copy(chat_id=message.from_user.id, caption = caption, parse_mode = 'html', reply_markup = reply_markup)
            except:
                pass
        return
    else:
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    text = "<b>📌මගෙන් Film ගන්න නම් ඔයා අපේ Channel එකට Join වෙලා ඉන්න ඕනි.</b>\n<b>📌You need to join in my Channel to use me.</b>\n\n<b>⏳පහල Button එක Click කරල Channel එකට Join වෙන්න.</b>\n⏳Kindly Please join Channel\n\n😇Join වුනාට පස්සෙ පහල 'තියන Try Again' උඩ Click කරන්න. ඔයාට Film එක ලැබෙයි.\nAfter Join to Channel hit on 'Try Again' Text to Get Movie \n\n<b>👍🏽 Try Again 🔗 (https://t.me/irupc_sever_bot?start=Z2V0LTM3NjE2LWlydXBjLWdldA==)</b>"
    message_text = message.text
    try:
        command, argument = message_text.split()
        text = text + f" <b>after join channel 👉👉<a href='https://t.me/{client.username}?start={argument}'>click Here</a></b>"
    except ValueError:
        pass
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url = client.invitelink)]])
    await message.reply(
        text = text,
        reply_markup = reply_markup,
        quote = True,
        disable_web_page_preview = True
    )
