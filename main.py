import os
import uuid
import pytz
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    JobQueue,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from detect import classify_leaf

# Logging
logging.basicConfig(level=logging.INFO)

# Timezone dengan pytz
tz = pytz.timezone("Asia/Jakarta")
scheduler = AsyncIOScheduler(timezone=tz)
job_queue = JobQueue()

# Token bot
TOKEN = "8425533727:AAGkuc9DVChTNG_5GuRinQ4dqJndjXc-FgM"

# Handler gambar
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    filename = f"images/{uuid.uuid4()}.jpg"
    os.makedirs("images", exist_ok=True)
    await file.download_to_drive(filename)

    await update.message.reply_text("🔍 Menganalisis gambar...")

    label, detected_path = classify_leaf(filename)

    if label == "cacar":
        diagnosis = (
            "🌿 Hasil: Daun Cengkeh Terindikasi *Cacar*.\n"
            "💡 Saran: Pangkas daun yang terinfeksi, semprotkan fungisida berbahan aktif tembaga setiap 7–14 hari."
        )
    elif label == "sehat":
        diagnosis = (
            "✅ Hasil: Daun Cengkeh *Sehat*.\n"
            "💡 Saran: Lanjutkan pemantauan secara berkala."
        )
    else:
        diagnosis = (
            "❌ Tidak dapat mendeteksi objek secara jelas. Coba kirim gambar yang lebih jelas."
        )

    await update.message.reply_text(diagnosis)

# kirim gambar bounding box + teks diagnosis
    with open(detected_path, "rb") as img:
        await update.message.reply_photo(photo=img, caption=diagnosis)

# Main program
if __name__ == "__main__":
    # Buat Application dengan job_queue custom SEBELUM build()
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .job_queue(job_queue)  # Ini wajib DITAMBAHKAN sebelum .build()
        .build()
    )

    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Bot is running...")
    app.run_polling()