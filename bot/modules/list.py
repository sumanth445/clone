from telegram.ext import CommandHandler, run_async
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot import LOGGER, dispatcher
from bot.helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands

@run_async
def list_drive(update,context):
    try:
        search = update.message.text.split(' ',maxsplit=1)[1]
        LOGGER.info(f"𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠: {search}")
        reply = sendMessage('🔍𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠... 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭!', context.bot, update)
        gdrive = GoogleDriveHelper(None)
        msg, button = gdrive.drive_list(search)

        if button:
            editMessage(msg, reply, button)
        else:
            editMessage('🔍𝐍𝐨 𝐑𝐞𝐬𝐮𝐥𝐭𝐬 𝐅𝐨𝐮𝐧𝐝❌', reply, button)

    except IndexError:
        sendMessage('𝐒𝐞𝐧𝐝 𝐚 𝐒𝐞𝐚𝐫𝐜𝐡🔍 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐀𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐁𝐨𝐭 𝐂𝐨𝐦𝐦𝐚𝐧𝐝', context.bot, update)


list_handler = CommandHandler(BotCommands.ListCommand, list_drive,filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(list_handler)
