import pyromod.listen
import sys

from pyrogram import Client

from config import (
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    FORCE_SUB_CHANNEL,
    FORCE_SUB_GROUP,
    LOGGER,
    OWNER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Berhenti. Gabung Group https://t.me/ShicyyXCode untuk Bantuan"
            )
            sys.exit()

        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot tidak dapat Mengambil link invite dari FORCE_SUB_CHANNEL!"
                )
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} adalah admin di Channel Tersebut, Chat ID F-Subs Channel Saat Ini: {FORCE_SUB_CHANNEL}"
                )
                self.LOGGER(__name__).info(
                    "Bot Berhenti. Gabung Group https://t.me/ShicyyXCode untuk Bantuan"
                )
                sys.exit()

        if FORCE_SUB_GROUP:
            try:
                link = (await self.get_chat(FORCE_SUB_GROUP)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_GROUP)
                    link = (await self.get_chat(FORCE_SUB_GROUP)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(
                    "Bot tidak dapat Mengambil link invite dari FORCE_SUB_GROUP!"
                )
                self.LOGGER(__name__).warning(
                    f"Pastikan @{self.username} adalah admin di Group Tersebut, Chat ID F-Subs Group Saat Ini: {FORCE_SUB_GROUP}"
                )
                self.LOGGER(__name__).info(
                    "Bot Berhenti. Gabung Group https://t.me/ShicyyXCode untuk Bantuan"
                )
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Pastikan @{self.username} adalah admin di Channel DataBase anda, CHANNEL_ID Saat Ini: {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot Berhenti. Gabung Group https://t.me/ShicyyXCode untuk Bantuan"
            )
            sys.exit()

        self.set_parse_mode("html")
        self.LOGGER(__name__).info(
            f"[🔥 BERHASIL DIAKTIFKAN! 🔥]\n\nBOT Dibuat oleh @{OWNER}\nJika @{OWNER} Membutuhkan Bantuan, Silahkan Tanyakan di Grup https://t.me/ShicyyXCode"
        )

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
