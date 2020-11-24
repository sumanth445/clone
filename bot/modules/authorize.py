from bot.helper.telegram_helper.message_utils import sendMessage
from telegram.ext import run_async
from bot import AUTHORIZED_CHATS, dispatcher
from telegram.ext import CommandHandler
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import Filters
from telegram import Update
from bot.helper.telegram_helper.bot_commands import BotCommands


@run_async
def authorize(update,context):
    reply_message = update.message.reply_to_message
    msg = ''
    with open('authorized_chats.txt', 'a') as file:
        if reply_message is None:
            # Trying to authorize a chat
            chat_id = update.effective_chat.id
            if chat_id not in AUTHORIZED_CHATS:
                file.write(f'{chat_id}\n')
                AUTHORIZED_CHATS.add(chat_id)
                msg = '⛽𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
            else:
                msg = '⛽𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
        else:
            # Trying to authorize someone in specific
            user_id = reply_message.from_user.id
            if user_id not in AUTHORIZED_CHATS:
                file.write(f'{user_id}\n')
                AUTHORIZED_CHATS.add(user_id)
                msg = '⛽𝐏𝐞𝐫𝐬𝐨𝐧 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐨𝐭'
            else:
                msg = '⛽𝐏𝐞𝐫𝐬𝐨𝐧 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐨𝐭'
        sendMessage(msg, context.bot, update)


@run_async
def unauthorize(update,context):
    reply_message = update.message.reply_to_message
    if reply_message is None:
        # Trying to unauthorize a chat
        chat_id = update.effective_chat.id
        if chat_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(chat_id)
            msg = '⛽𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐈𝐬 𝐔𝐧𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
        else:
            msg = '⛽𝐓𝐡𝐢𝐬 𝐂𝐡𝐚𝐭 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝'
    else:
        # Trying to authorize someone in specific
        user_id = reply_message.from_user.id
        if user_id in AUTHORIZED_CHATS:
            AUTHORIZED_CHATS.remove(user_id)
            msg = '⛽𝐏𝐞𝐫𝐬𝐨𝐧 𝐔𝐧𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐨𝐭!'
        else:
            msg = '⛽𝐏𝐞𝐫𝐬𝐨𝐧 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐔𝐧𝐀𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐞 𝐁𝐨𝐭!'
    with open('authorized_chats.txt', 'a') as file:
        file.truncate(0)
        for i in AUTHORIZED_CHATS:
            file.write(f'{i}\n')
    sendMessage(msg, context.bot, update)


authorize_handler = CommandHandler(command=BotCommands.AuthorizeCommand, callback=authorize,
                                   filters=CustomFilters.owner_filter & Filters.group)
unauthorize_handler = CommandHandler(command=BotCommands.UnAuthorizeCommand, callback=unauthorize,
                                     filters=CustomFilters.owner_filter & Filters.group)
dispatcher.add_handler(authorize_handler)
dispatcher.add_handler(unauthorize_handler)

