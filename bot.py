from telethon import events, TelegramClient, Button
import logging
from telethon.tl.functions.users import GetFullUserRequest as us
import os


logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)

bot = TelegramClient(
        "Whisper",
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e"
        ).start(
                bot_token=TOKEN
                )
db = {}

@bot.on(events.NewMessage(pattern="^[!?/]whisperstart$"))
async def stsrt(event):
    await event.reply(
            "**🌐 I'ᴍ ᴛʜᴇ Wʜɪsᴘᴇʀ Bᴏᴛ. 💬 Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ᴛᴏ sᴇɴᴅ sᴇᴄʀᴇᴛ ᴡʜɪsᴘᴇʀs ɪɴ ɢʀᴏᴜᴘs.🔮 I ᴡᴏʀᴋ ɪɴ ᴛʜᴇ Iɴʟɪɴᴇ ᴍᴏᴅᴇ ᴛʜᴀᴛ ᴍᴇᴀɴs ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ᴇᴠᴇɴ ɪғ I'ᴍ ɴᴏᴛ ɪɴ ᴛʜᴇ ɢʀᴏᴜᴘ.💌 Iᴛ ɪs ᴠᴇʀʏ ᴇᴀsʏ ᴛᴏ ᴜsᴇ ᴍᴇ, sɪᴍᴘʟʏ ғᴏʀᴡᴀʀᴅ ᴀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴀ ᴜsᴇʀ ᴛᴏ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ ᴀɴᴅ I'ʟʟ ᴅᴏ ᴛʜᴇ ʀᴇsᴛ ғᴏʀ ʏᴏᴜ.**",
            buttons=[
                [Button.switch_inline("Go Inline", query="")]
                ]
            )


@bot.on(events.InlineQuery())
async def die(event):
    if len(event.text) != 0:
        return
    me = (await bot.get_me()).username
    
@bot.on(events.InlineQuery(pattern="wspr"))
async def inline(event):
    me = (await bot.get_me()).username
    try:
        inp = event.text.split(None, 1)[1]
        user, msg = inp.split("|")
    except IndexError:
        await event.answer(
                [], 
                switch_pm=f"@{me} [UserID]|[Message]",
                switch_pm_param="start"
                )
    except ValueError:
        await event.answer(
                [],
                switch_pm=f"Give a message too!",
                switch_pm_param="start"
                )
    try:
        ui = await bot(us(user))
    except BaseException:
        await event.answer(
                [],
                switch_pm="Invalid User ID/Username",
                switch_pm_param="start"
                )
        return
    db.update({"user_id": ui.user.id, "msg": msg, "self": event.sender.id})
    text = f"""
A Whisper Has Been Sent
To [{ui.user.first_name}](tg://user?id={ui.user.id})!
Click The Below Button To See The Message!\n
**Note:** __Only {ui.user.first_name} can open this!__
    """
    dn = event.builder.article(
            title="Its a secret message!",
            description="It's a secret message!",
            text=text,
            buttons=[
                [Button.inline(" Show Message! ", data="wspr")]
                ]
            )
    await event.answer(
            [dn],
            switch_pm="It's a secret message!",
            switch_pm_param="start"
            )


@bot.on(events.CallbackQuery(data="wspr"))
async def ws(event):
    user = int(db["user_id"])
    lol = [int(db["self"])]
    lol.append(user)
    if event.sender.id not in lol:
        await event.answer("🔐 This message is not for you!", alert=True)
        return
    msg = db["msg"]
    if msg == []:
        await event.anwswer(
                "Oops!\nIt's looks like message got deleted from my server!", alert=True)
        return
    await event.answer(msg, alert=True)

print("Succesfully Started Bot!")
bot.run_until_disconnected()
