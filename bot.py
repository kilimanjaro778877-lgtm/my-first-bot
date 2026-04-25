import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

ANTHROPIC_KEY = "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"
TELEGRAM_TOKEN = "8608801274:AAFLogFmpuqif3BR5SggtkgevjYYABmjJIM"

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
histories = {}

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if user_id not in histories:
        histories[user_id] = []

    histories[user_id].append({"role": "user", "content": text})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system="Ти корисний асистент.",
        messages=histories[user_id]
    )

    reply = response.content[0].text
    histories[user_id].append({"role": "assistant", "content": reply})

    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()