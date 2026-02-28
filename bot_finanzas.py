import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Diccionario para guardar datos de cada usuario
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola! Soy tu bot de finanzas.\n"
                                    "Podés registrar tu sueldo, gastos y pedir tu saldo o resumen.\n"
                                    "Ejemplo:\n"
                                    "sueldo 50000\n"
                                    "gasto comida 200\n"
                                    "gasto transporte 50\n"
                                    "saldo\n"
                                    "resumen")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from_number = update.message.from_user.id
    text = update.message.text.lower()

    # Crear usuario si no existe
    if from_number not in user_data:
        user_data[from_number] = {
            "sueldo": 0,
            "gastos": []
        }

    user = user_data[from_number]
    lines = text.split("\n")
    responses = []

    for line in lines:
        parts = line.split()
        if not parts:
            continue

        if parts[0] == "sueldo" and len(parts) == 2:
            user["sueldo"] = float(parts[1])
            responses.append(f"Sueldo registrado: {user['sueldo']}")

        elif parts[0] == "gasto" and len(parts) == 3:
            categoria = parts[1]
            monto = float(parts[2])
            user["gastos"].append((categoria, monto))
            responses.append(f"Gasto agregado: {categoria} - {monto}")

        elif parts[0] == "saldo":
            total_gastos = sum(g[1] for g in user["gastos"])
            saldo = user["sueldo"] - total_gastos
            responses.append(f"Saldo disponible: {saldo}")

        elif parts[0] == "resumen":
            total_gastos = sum(g[1] for g in user["gastos"])
            saldo = user["sueldo"] - total_gastos
            resumen = f"Sueldo: {user['sueldo']}\nGastos:"
            for g in user["gastos"]:
                resumen += f"\n  {g[0]}: {g[1]}"
            resumen += f"\nSaldo: {saldo}"
            responses.append(resumen)

        else:
            responses.append(f"No entiendo: {line}")

    await update.message.reply_text("\n\n".join(responses))


if __name__ == "__main__":
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        print("Error: TOKEN no encontrado en variables de entorno")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot corriendo...")
    app.run_polling()