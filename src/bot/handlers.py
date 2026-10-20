import logging
import sys
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from services.downloader import SoundcloudDownloader
from core.config import TELEGRAM_BOT_TOKEN
from mutagen.id3 import ID3, TIT2, TPE1
from telegram import InputFile

logging.disable(logging.CRITICAL)
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')


class SoundcloudBot:
    def __init__(self):
        self.downloader = SoundcloudDownloader()
        self.temp_files = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Hi!\nSend me a Soundcloud link and I'll download the audio for you."
        )

    async def handle_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "editing_metadata" in context.user_data:
            await self.handle_metadata(update, context)
            return

        url = update.message.text

        if "soundcloud.com" not in url:
            await update.message.reply_text("Please send a valid Soundcloud link.")
            return

        downloading_msg = await update.message.reply_text("Downloading (this may take a moment)...")

        try:
            mp3_path, title, thumbnail = self.downloader.download(url)

            message_id = update.message.message_id
            self.temp_files[message_id] = {"path": mp3_path, "thumbnail": thumbnail}

            with open(mp3_path, "rb") as audio_file:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🖼️", url=thumbnail), InlineKeyboardButton("Change Metadata", callback_data=f"meta_{message_id}")]
                ])
                await update.message.reply_audio(
                    audio=audio_file,
                    title=title,
                    filename=f"{title}.mp3",
                    reply_markup=keyboard,
                )

            await downloading_msg.delete()

        except Exception:
            await update.message.reply_text("Error downloading")

    async def metadata_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        if query.data.startswith("meta_"):
            message_id = int(query.data.split("_")[1])
            if message_id in self.temp_files:
                context.user_data["editing_metadata"] = message_id
                context.user_data["original_message_id"] = query.message.message_id
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
                except:
                    pass
                text_msg = await query.message.reply_text("Send new metadata in format: title|artist")
                context.user_data["text_message_id"] = text_msg.message_id

    async def handle_metadata(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        metadata_text = update.message.text
        parts = metadata_text.split("|")

        if len(parts) < 2:
            await update.message.reply_text("Invalid format. Use: title|artist")
            del context.user_data["editing_metadata"]
            return

        message_id = context.user_data["editing_metadata"]
        temp_data = self.temp_files.get(message_id)
        mp3_path = temp_data["path"] if temp_data else None
        thumbnail = temp_data["thumbnail"] if temp_data else ""

        if not mp3_path:
            await update.message.reply_text("File not found. Download again.")
            del context.user_data["editing_metadata"]
            if "original_message_id" in context.user_data:
                del context.user_data["original_message_id"]
            return

        try:
            audio = ID3(mp3_path)
            audio.delete()

            if parts[0]:
                audio.add(TIT2(encoding=3, text=parts[0]))
            if parts[1]:
                audio.add(TPE1(encoding=3, text=parts[1]))

            audio.save()

            await update.message.delete()

            if "text_message_id" in context.user_data:
                try:
                    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data["text_message_id"])
                except:
                    pass

            with open(mp3_path, "rb") as audio_file:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🖼️", url=thumbnail)]
                ])
                await update.message.reply_audio(
                    audio=audio_file,
                    title=parts[0] if parts[0] else "Updated",
                    filename=f"{parts[0] if parts[0] else 'track'}.mp3",
                    reply_markup=keyboard,
                )

            self.downloader.cleanup(mp3_path)
            del self.temp_files[message_id]
            del context.user_data["editing_metadata"]
            if "original_message_id" in context.user_data:
                del context.user_data["original_message_id"]
            if "text_message_id" in context.user_data:
                del context.user_data["text_message_id"]

        except Exception:
            await update.message.reply_text("Error updating metadata")
            del context.user_data["editing_metadata"]
            if "original_message_id" in context.user_data:
                del context.user_data["original_message_id"]

    def run(self):
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_link))
        app.add_handler(CallbackQueryHandler(self.metadata_button))

        app.run_polling()
