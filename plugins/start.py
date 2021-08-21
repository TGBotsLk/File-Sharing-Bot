#(©)Codexbotz

import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, START_MSG, OWNER_ID, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON
from helper_func import subscribed, encode, decode, get_messages

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
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start,end+1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:

            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption = "" if not msg.caption else msg.caption.html, filename = msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

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
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("😊 About Me", callback_data = "about"),
                    InlineKeyboardButton("🔒 Close", callback_data = "close")
                ]
            ]
        )
        await message.reply_text(
            text = START_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
            reply_markup = reply_markup,
            disable_web_page_preview = True,
            quote = True
        )
        return

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    text = "<b>ഞങ്ങളുടെ Data Base പ്രകാരം നിങ്ങൾ ഇതുവരെ ഞങ്ങളുടെ Update Channel ലിൽ join ചെയ്തിട്ടില്ല\n\nഅതുകൊണ്ട് താഴെ കാണുന്ന (join Channel) എന്ന link ഉപയോഗിച്ചു update channel ലിൽ അംഗമാകൂ\n\nYou have not yet joined our Update Channel as per our Data Base\n\nso join the update channel using the link (join Channel) below\n\nஎங்கள் தரவுத்தளத்தின்படி நீங்கள் இன்னும் எங்கள் புதுப்பிப்பு சேனலில் சேரவில்லை, எனவே கீழேயுள்ள இணைப்பைப் பயன்படுத்தி சேனலில் சேருங்கள் (சேனலில் சேருங்கள்)\n\nನಮ್ಮ ಡೇಟಾ ಬೇಸ್ ಪ್ರಕಾರ ನೀವು ಇನ್ನೂ ನಮ್ಮ ಅಪ್ಡೇಟ್ ಚಾನೆಲ್ ಗೆ ಸೇರಿಕೊಂಡಿಲ್ಲ ಹಾಗಾಗಿ ಕೆಳಗಿನ ಲಿಂಕ್ ಬಳಸಿ (ಚಾನೆಲ್ ಸೇರಿಕೊಳ್ಳಿ) ಅಪ್ಡೇಟ್ ಚಾನೆಲ್ ಗೆ ಸೇರಿಕೊಳ್ಳಿ\n\nమా డేటా బేస్ ప్రకారం మీరు ఇంకా మా అప్‌డేట్ ఛానెల్‌లో చేరలేదు కాబట్టి దిగువ లింక్ (ఛానెల్‌లో చేరండి) ఉపయోగించి అప్‌డేట్ ఛానెల్‌లో చేరండి\n\nआप अभी तक हमारे डेटा बेस के अनुसार हमारे अपडेट चैनल में शामिल नहीं हुए हैं, इसलिए नीचे दिए गए लिंक (चैनल से जुड़ें) का उपयोग करके अपडेट चैनल से जुड़ें </b>"
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
