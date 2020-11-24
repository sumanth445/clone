from telegram.ext import CommandHandler, run_async

from bot import download_dict, dispatcher, download_dict_lock, DOWNLOAD_DIR
from bot.helper.ext_utils.fs_utils import clean_download
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import *

from time import sleep
from bot.helper.ext_utils.bot_utils import getDownloadByGid, MirrorStatus


@run_async
def cancel_mirror(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    mirror_message = None
    if len(args) > 1:
        gid = args[1]
        dl = getDownloadByGid(gid)
        if not dl:
            sendMessage(f"GID: <code>{gid}</code> not found.", context.bot, update)
            return
        with download_dict_lock:
            keys = list(download_dict.keys())
        mirror_message = dl.message
    elif update.message.reply_to_message:
        mirror_message = update.message.reply_to_message
        with download_dict_lock:
            keys = list(download_dict.keys())
            dl = download_dict[mirror_message.message_id]
    if len(args) == 1:
        if mirror_message is None or mirror_message.message_id not in keys:
            if BotCommands.MirrorCommand in mirror_message.text or \
                    BotCommands.TarMirrorCommand in mirror_message.text:
                msg = "⛽𝐌𝐢𝐫𝐫𝐨𝐫 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐇𝐚𝐯𝐞 𝐁𝐞𝐞𝐧 𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝"
                sendMessage(msg, context.bot, update)
                return
            else:
                msg = "⛽𝐏𝐥𝐞𝐚𝐬𝐞 𝐑𝐞𝐩𝐥𝐲 𝐓𝐨 𝐓𝐡𝐞 /mirror 𝐌𝐞𝐬𝐬𝐚𝐠𝐞 𝐖𝐡𝐢𝐜𝐡 𝐖𝐚𝐬 𝐔𝐬𝐞𝐝 𝐓𝐨 𝐒𝐭𝐚𝐫𝐭 𝐓𝐡𝐞 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐨𝐫 /cancel 𝐆𝐢𝐝 𝐓𝐨 𝐂𝐚𝐧𝐜𝐞𝐥 𝐈𝐭!"
                sendMessage(msg, context.bot, update)
                return
    if dl.status() == "𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 📤...":
        sendMessage("⛽𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐈𝐧 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬, 𝐃𝐨𝐧'𝐭 𝐂𝐚𝐧𝐜𝐞𝐥 𝐈𝐭.", context.bot, update)
        return
    elif dl.status() == "𝐀𝐫𝐜𝐡𝐢𝐯𝐢𝐧𝐠 🗃️🔐...":
        sendMessage("⛽𝐀𝐫𝐜𝐡𝐢𝐯𝐚𝐥 𝐎𝐟 𝐘𝐨𝐮𝐫 𝐅𝐢𝐥𝐞 𝐈𝐬 𝐈𝐧 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐏𝐫𝐨𝐠𝐫𝐞𝐬𝐬, 𝐃𝐨𝐧'𝐭 𝐂𝐚𝐧𝐜𝐞𝐥 𝐈𝐭.", context.bot, update)
        return
    else:
        dl.download().cancel_download()
    sleep(1)  # Wait a Second For Aria2 To free Resources.
    clean_download(f'{DOWNLOAD_DIR}{mirror_message.message_id}/')


@run_async
def cancel_all(update, context):
    with download_dict_lock:
        count = 0
        for dlDetails in list(download_dict.values()):
            if dlDetails.status() == MirrorStatus.STATUS_DOWNLOADING \
                    or dlDetails.status() == MirrorStatus.STATUS_WAITING:
                dlDetails.download().cancel_download()
                count += 1
    delete_all_messages()
    sendMessage(f'Cancelled {count} downloads!', context.bot, update)


cancel_mirror_handler = CommandHandler(BotCommands.CancelMirror, cancel_mirror,
                                       filters=(CustomFilters.authorized_chat | CustomFilters.authorized_user) & CustomFilters.mirror_owner_filter)
cancel_all_handler = CommandHandler(BotCommands.CancelAllCommand, cancel_all,
                                    filters=CustomFilters.owner_filter)
dispatcher.add_handler(cancel_all_handler)
dispatcher.add_handler(cancel_mirror_handler)
