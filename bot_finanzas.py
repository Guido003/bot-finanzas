import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
TOKEN = "8592148719:AAEtO8LsyYoGnQQdg67K5HZKeUeYDOfddc8"
user_data = {}  # Guardamos datos de cada usuario por chat_id

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -----------------------------
# FUNCIONES
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu bot de finanzas.\n"
        "Comandos disponibles:\n"
        "- sueldo <monto>\n"
        "- gasto <categoria> <monto>\n"
        "- saldo\n"
        "- resumen"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.lower().strip()

    if chat_id not in user_data:
        user_data[chat_id] = {"sueldo": 0, "gastos": {}}

    user = user_data[chat_id]

    try:
        if text.startswith("sueldo"):
            monto = float(text.split()[1])
            user["sueldo"] = monto
            await update.message.reply_text(f"Sueldo mensual registrado: ${monto:.2f}")

        elif text.startswith("gasto"):
            _, categoria, monto = text.split()
            monto = float(monto)
            if categoria not in user["gastos"]:
                user["gastos"][categoria] = 0
            user["gastos"][categoria] += monto
            await update.message.reply_text(f"Gasto registrado: {categoria} ${monto:.2f}")

        elif text == "saldo":
            total_gastos = sum(user["gastos"].values())
            saldo = user["sueldo"] - total_gastos
            await update.message.reply_text(f"Saldo disponible: ${saldo:.2f}")

        elif text == "resumen":
            if user["gastos"]:
                resumen = "\n".join([f"{cat}: ${monto:.2f}" for cat, monto in user["gastos"].items()])
                total_gastos = sum(user["gastos"].values())
                saldo = user["sueldo"] - total_gastos
                await update.message.reply_text(f"Resumen de gastos:\n{resumen}\nTotal gastado: ${total_gastos:.2f}\nSaldo: ${saldo:.2f}")
            else:
                await update.message.reply_text("No hay gastos registrados.")

        else:
            await update.message.reply_text(
                "Comando no reconocido.\n"
                "Usa:\n- sueldo <monto>\n- gasto <categoria> <monto>\n- saldo\n- resumen"
            )
    except Exception as e:
        await update.message.reply_text("Hubo un error al procesar tu mensaje. Verifica el formato.")

# -----------------------------
# INICIAR BOT
# -----------------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()