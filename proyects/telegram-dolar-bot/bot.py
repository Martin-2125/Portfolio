import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Importamos la función del dólar
from dolar_api import get_dolar_api

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("No encontré el TOKEN en .env. Revisá que esté bien escrito.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '¡Hola! Soy tu bot del dólar blue.\n'
        'Usá /dolar para ver precios actuales.\n'
    )

async def dolar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    datos = get_dolar_api()
    if datos:
        texto = (
            f"📊 Dólar hoy ({datos['fecha']}):\n"
            f"• Oficial Venta: ${datos['oficial_venta']}\n"
            f"• Blue Venta: ${datos['blue_venta']}\n"
            f"• Blue Compra: ${datos['blue_compra']}\n\n"
        )
        await update.message.reply_text(texto)
    else:
        await update.message.reply_text("No pude agarrar los precios.")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dolar", dolar))

    print("Bot prendido y escuchando... dale que va.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()