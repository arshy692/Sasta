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

import os
from pyrogram import *
from pyrogram.types import *
from STORM.helper.basic import edit_or_reply, get_text, get_user
from config import SUDO_USERS

OWNER = os.environ.get("OWNER", None)
BIO = os.environ.get("BIO", "404 : Bio Lost")

@Client.on_message(
    filters.command(["clone"], ".") & (filters.me | filters.user(SUDO_USERS))
)
async def clone(client: Client, message: Message):
    if not message.reply_to_message:
        return await hellbot.delete(
            message, "Reply to a user's message to clone their profile."
        )

    replied_user = message.reply_to_message.from_user
    if replied_user.is_self:
        return await hellbot.delete(message, "I can't clone myself!")

    hell = await hellbot.edit(message, "Cloning ...")

    try:
        meh = await client.resolve_peer(client.me.id)
        fullUser = await client.invoke(GetFullUser(id=meh))
        about = fullUser.full_user.about or ""
    except:
        about = ""

    first_name = client.me.first_name
    last_name = client.me.last_name or ""

    await db.set_env("CLONE_FIRST_NAME", first_name)
    await db.set_env("CLONE_LAST_NAME", last_name)
    await db.set_env("CLONE_ABOUT", about)

    try:
        targetUser = await client.resolve_peer(replied_user.id)
        repliedFullUser = await client.invoke(GetFullUser(id=targetUser))
        await client.update_profile(
            first_name=replied_user.first_name,
            last_name=replied_user.last_name or "",
            about=repliedFullUser.full_user.about or "",
        )
    except:
        await client.update_profile(
            first_name=replied_user.first_name,
            last_name=replied_user.last_name or "",
        )

    try:
        profile_pic = await client.download_media(replied_user.photo.big_file_id)
        await client.set_profile_photo(photo=profile_pic)
        os.remove(profile_pic)
    except:
        pass

    await hell.edit("**😁 𝖧𝖾𝗅𝗅𝗈 𝗆𝗒 𝖿𝗋𝗂𝖾𝗇𝖽!**")
    await hellbot.check_and_log(
        "clone",
        f"**Cloned {replied_user.mention}** ({replied_user.id}) \n\n**By:** {first_name}",
    )


@on_message("revert", allow_stan=True)
async def revert(client: Client, message: Message):
    first_name = await db.get_env("CLONE_FIRST_NAME")
    last_name = await db.get_env("CLONE_LAST_NAME")
    about = await db.get_env("CLONE_ABOUT")

    if not first_name:
        return await hellbot.delete(message, "I'm not cloned yet.")

    hell = await hellbot.edit(message, "Reverting ...")

    await client.update_profile(first_name, last_name, about)

    async for photos in client.get_chat_photos("me", 1):
        await client.delete_profile_photos(photos.file_id)

    await db.rm_env("CLONE_FIRST_NAME")
    await db.rm_env("CLONE_LAST_NAME")
    await db.rm_env("CLONE_ABOUT")

    await hell.edit("**Reverted back!**")
    await hellbot.check_and_log(
        "revert",
        f"**Reverted to my original profile.** \n\n**By:** {first_name}",
