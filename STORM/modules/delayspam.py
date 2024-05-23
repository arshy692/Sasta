#MIT License

#Copyright (c) 2024 ᴋᴜɴᴀʟ [AFK]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import asyncio
from pyrogram.types import Message
from pyrogram import filters, Client
from config import SUDO_USERS

@Client.on_message(
    filters.command(["delayspam"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def delay_spam(client: Client, message: Message):
    command_parts = message.text.split(maxsplit=2)
    
    if len(command_parts) < 3:
        await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ꜰᴏʀᴍᴀᴛ. ᴜꜱᴇ: .ᴅᴇʟᴀʏꜱᴘᴀᴍ <ᴅᴇʟᴀʏ_ꜱᴇᴄᴏɴᴅꜱ> <ᴛᴇxᴛ>")
        return
    
    try:
        delay_seconds = float(command_parts[1])
        spam_text = command_parts[2]
    except ValueError:
        await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ ꜰᴏʀᴍᴀᴛ. ᴜꜱᴇ: .ᴅᴇʟᴀʏꜱᴘᴀᴍ <ᴅᴇʟᴀʏ_ꜱᴇᴄᴏɴᴅꜱ> <ᴛᴇxᴛ>")
        return

    quantity = 5000
    if len(command_parts) > 3:
        try:
            quantity = int(command_parts[3])
        except ValueError:
            await message.reply_text("ɪɴᴠᴀʟɪᴅ Qᴜᴀɴᴛɪᴛʏ. ɪᴛ ᴍᴜꜱᴛ ʙᴇ ᴀ ᴠᴀʟɪᴅ ɪɴᴛᴇɢᴇʀ.")
            return

    for _ in range(quantity):
        if message.reply_to_message:
            id = message.reply_to_message.message_id
            await message.reply_text(spam_text, reply_to_message_id=id)
        else:
            cid = message.chat.id
            await client.send_message(cid, spam_text)
        
        await asyncio.sleep(delay_seconds)
