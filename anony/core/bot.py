# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import pyrogram
from pyrogram.enums import ParseMode, ChatMemberStatus
from anony import config, logger

class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="anony",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )
        # Link preview settings (Agar Pyrogram v2+ hai toh support karega)
        try:
            self.link_preview_options = pyrogram.types.LinkPreviewOptions(is_disabled=True)
        except AttributeError:
            self.link_preview_options = None
            
        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID
        self.bl_users = pyrogram.filters.user()
        self.sudoers = pyrogram.filters.user(self.owner)

    async def boot(self):
        """
        Starts the bot and performs initial setup.
        """
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(self.logger, "Bot Started")
            get = await self.get_chat_member(self.logger, self.id)
        except Exception as ex:
            raise SystemExit(f"Bot has failed to access the log group: {self.logger}\nReason: {ex}")

        if get.status != ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Please promote the bot as an admin in logger group.")
        
        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        """
        Asynchronously stops the bot.
        """
        await super().stop()
        logger.info("Bot stopped.")
