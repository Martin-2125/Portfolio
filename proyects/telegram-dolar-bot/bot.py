import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dolar_api import get_dolar_api
import json
from pathlib import Path

suscritos = set()

async def alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    suscritos.add(chat_id)
    await update.message.reply_text(
        "¡Listo! Te voy a avisar cuando el blue cambie mucho. "
        "Si querés parar, mandame /desalerta."
    )

async def desalerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    suscritos.discard(chat_id)
    await update.message.reply_text("Ok, ya no te aviso más. Si cambiás de idea, /alerta.")

async def check_blue_job(context: ContextTypes.DEFAULT_TYPE):
    datos = get_dolar_api()
    if not datos:
        return  # No hay datos, salta

    blue_actual = datos['blue_venta']
    blue_anterior = load_last_price()

    if blue_anterior is not None:
        cambio_porcent = ((blue_actual - blue_anterior) / blue_anterior) * 100
        if abs(cambio_porcent) >= 5: 
            texto = (
                f"🚨 ¡ALERTA DÓLAR! 🚨\n"
                f"El blue cambió: ${blue_anterior} → ${blue_actual} "
                f"({cambio_porcent:+.1f}%)\n"
                f"Fecha: {datos['fecha']}\n"
            )
            for chat_id in suscritos:
                try:
                    await context.bot.send_message(chat_id=chat_id, text=texto)
                except Exception as e:
                    print(f"No pude mandar a {chat_id}: {e}")
                    suscritos.discard(chat_id) 
    save_last_price(blue_actual)

LAST_PRICE_FILE = Path("last_blue.json")

def load_last_price():
    if LAST_PRICE_FILE.exists():
        with open(LAST_PRICE_FILE, 'r') as f:
            return json.load(f).get('blue_venta', None)
    return None

def save_last_price(precio):
    with open(LAST_PRICE_FILE, 'w') as f:
        json.dump({'blue_venta': precio}, f)

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
    app.add_handler(CommandHandler("alerta", alerta))
    app.add_handler(CommandHandler("desalerta", desalerta))

    print("Bot prendido y escuchando... dale que va.")
    app.job_queue.run_repeating(check_blue_job, interval=1800, first=10)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()