import json
import os
import re
import telebot
from groq import Groq
from dotenv import load_dotenv

# ============================================================
# CONFIGURACIÓN
# ============================================================

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("❌ No se encontró TELEGRAM_BOT_TOKEN en el archivo .env")

if not GROQ_API_KEY:
    print("⚠️ GROQ_API_KEY no configurada. El bot funcionará con las consultas de horarios.")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# ============================================================
# INFORMACIÓN DEL COLEGIO
# ============================================================

contexto_colegio = {
    "institucion": "Unidad Educativa Eduardo Kingman",

    "horarios_atencion_padres": [

        {
            "docente": "Altamirano Retto Pedro",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 12:45 – 13:45",
            "viernes": "7:45 A 8:25, Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Arellano Urgiles Kevin",
            "lunes": "Hora de salida 13:20 – 13:45",
            "martes": "7:05 A 7:45, Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 13:20 – 13:45",
            "jueves": "11:35 A 12:10, Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Campoverde Aguilera Roger",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "9:05 A 9:45, Hora de salida 13:20 – 13:45",
            "miercoles": "9:05 A 9:45, Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 13:20 – 13:45",
            "viernes": "Hora de salida 13:20 – 13:45"
        },

        {
            "docente": "Cárdenas Estrada Leonardo Estefano",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "8:25 A 9:05, Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 13:20 – 13:45",
            "viernes": "7:45 A 8:25, Hora de salida 13:20 – 13:45"
        },

        {
            "docente": "Castro Villegas Joselyne",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "7:05 A 7:45, Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "7:05 A 7:45, Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Chávez Aguiar Luis",
            "lunes": "Hora de salida 13:20 – 13:45",
            "martes": "9:05 A 9:45, Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "9:05 A 9:45, Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 13:20 – 13:45"
        },

        {
            "docente": "Hernández Romero Wilson",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "7:05 A 7:45, Hora de salida 13:20 – 13:45",
            "viernes": "7:45 A 8:25, Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Lavayen Valero Andrea",
            "lunes": "Hora de salida 13:20 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "7:05 A 7:45, Hora de salida 13:20 – 13:45",
            "viernes": "7:05 A 7:45, Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Mero Jiménez Ronaldo",
            "lunes": "12:10 a 12:45, Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 13:20 – 13:45",
            "jueves": "9:05 - 9:45, Hora de salida 13:20 – 13:45",
            "viernes": "Hora de salida 13:20 – 13:45"
        },

        {
            "docente": "Prado Sempertegui Emily",
            "lunes": "7:05 A 7:45, Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 13:20 – 13:45",
            "jueves": "10:55-11:35",
            "viernes": "Sin registro"
        },

        {
            "docente": "Rugel Tatiana",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "7:45-8:25, Hora de salida 12:45 – 13:45",
            "viernes": "10:55-11:35, Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Salguero Leonardo",
            "lunes": "10:55-11:35, Hora de salida 13:20 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "11:35-12:10, Hora de salida 13:20 – 13:45",
            "jueves": "Hora de salida 13:20 – 13:20",
            "viernes": "Hora de salida 13:20 – 13:20"
        },

        {
            "docente": "Soto Lavayen Jaliveth Damarys",
            "lunes": "Hora de salida 13:20 – 13:45",
            "martes": "9:05-9:45, Hora de salida 13:20 – 13:45",
            "miercoles": "Hora de salida 13:20 – 13:45",
            "jueves": "Sin registro",
            "viernes": "8:25-9:05, Hora de salida 12:45 – 13:20"
        },

        {
            "docente": "Suña Josué",
            "lunes": "12:10-12:45, Hora de salida 13:20 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 13:20 – 13:45",
            "viernes": "7:05-7:45, Hora de salida 13:20 – 13:45"
        },

        {
            "docente": "Vega Vera Evelyn Carolina",
            "lunes": "7:45-8:25, Hora de salida 12:45 – 13:45",
            "martes": "Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "11:35-12:10, Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Villamar Walter",
            "lunes": "7:45-8:25, Hora de salida 12:45 – 13:45",
            "martes": "7:45-8:25, Hora de salida 12:45 – 13:45",
            "miercoles": "Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 12:45 – 13:45"
        },

        {
            "docente": "Zhigui Corvachi Julissa Alexandra",
            "lunes": "Hora de salida 12:45 – 13:45",
            "martes": "7:05-7:45, Hora de salida 12:45 – 13:45",
            "miercoles": "7:05-7:45, Hora de salida 12:45 – 13:45",
            "jueves": "Hora de salida 12:45 – 13:45",
            "viernes": "Hora de salida 12:45 – 13:45"
        }
    ]
}


# ============================================================
# FUNCIONES DE BÚSQUEDA
# ============================================================

def normalizar(texto):
    """
    Convierte el texto a minúsculas y elimina tildes.
    """
    import unicodedata

    texto = texto.lower()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto


def buscar_profesor(texto):
    """
    Busca un profesor aunque el usuario escriba
    solamente una parte del nombre.
    """

    texto_normalizado = normalizar(texto)

    mejores_resultados = []

    for profesor in contexto_colegio["horarios_atencion_padres"]:

        nombre = profesor["docente"]
        nombre_normalizado = normalizar(nombre)

        partes = nombre_normalizado.split()

        coincidencias = 0

        for parte in partes:

            if len(parte) >= 4 and parte in texto_normalizado:
                coincidencias += 1

        if coincidencias > 0:
            mejores_resultados.append(
                (coincidencias, profesor)
            )

    if not mejores_resultados:
        return None

    mejores_resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return mejores_resultados[0][1]


# ============================================================
# DETECTAR DÍA
# ============================================================

def detectar_dia(texto):

    texto = normalizar(texto)

    if "lunes" in texto:
        return "lunes"

    if "martes" in texto:
        return "martes"

    if "miercoles" in texto:
        return "miercoles"

    if "jueves" in texto:
        return "jueves"

    if "viernes" in texto:
        return "viernes"

    return None


# ============================================================
# FORMATEAR HORARIO
# ============================================================

def formato_horario(profesor):

    nombre = profesor["docente"]

    respuesta = (
        f"👨‍🏫 <b>{nombre}</b>\n"
        f"🏫 Unidad Educativa Eduardo Kingman\n\n"
        f"<b>Horario de atención a padres:</b>\n\n"
    )

    dias = {
        "lunes": "Lunes",
        "martes": "Martes",
        "miercoles": "Miércoles",
        "jueves": "Jueves",
        "viernes": "Viernes"
    }

    for clave, nombre_dia in dias.items():

        horario = profesor.get(clave, "Sin registro")

        respuesta += (
            f"📅 <b>{nombre_dia}:</b> {horario}\n"
        )

    return respuesta


# ============================================================
# RESPUESTA DIRECTA
# ============================================================

def responder_horario(texto):

    profesor = buscar_profesor(texto)

    if not profesor:
        return None

    dia = detectar_dia(texto)

    # Si preguntó por un día específico
    if dia:

        nombre_dia = {
            "lunes": "Lunes",
            "martes": "Martes",
            "miercoles": "Miércoles",
            "jueves": "Jueves",
            "viernes": "Viernes"
        }

        horario = profesor[dia]

        return (
            f"👨‍🏫 <b>{profesor['docente']}</b>\n\n"
            f"📅 <b>{nombre_dia[dia]}</b>\n"
            f"🕐 {horario}"
        )

    # Si solamente preguntó por el profesor
    return formato_horario(profesor)


# ============================================================
# IA DE GROQ
# ============================================================

instruccion_sistema = f"""
Eres 'Tecno', el asistente virtual de la
Unidad Educativa Eduardo Kingman.

Tu función es ayudar a los usuarios con información
relacionada con los horarios de atención a padres
de familia de los docentes.

REGLAS:

1. Responde siempre en español.

2. Sé educado, claro y profesional.

3. No inventes horarios.

4. Utiliza únicamente la información proporcionada.

5. Si el usuario pregunta por un profesor que no aparece
en los datos, indica que no se encontró el registro.

6. Si la pregunta no está relacionada con los horarios,
indica amablemente que tu función principal es informar
los horarios de atención a padres.

INFORMACIÓN:

{json.dumps(contexto_colegio, ensure_ascii=False)}
"""


def preguntar_groq(texto_usuario):

    try:

        respuesta = client.chat.completions.create(

            # Modelo actual
            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": instruccion_sistema
                },
                {
                    "role": "user",
                    "content": texto_usuario
                }
            ],

            temperature=0.2,

            max_tokens=500
        )

        return respuesta.choices[0].message.content

    except Exception as e:

        print("Error de Groq:", e)

        return (
            "⚠️ No pude utilizar el servicio de inteligencia "
            "artificial en este momento.\n\n"
            "Puedes preguntarme directamente por el horario "
            "de un docente."
        )


# ============================================================
# COMANDO START / HELP
# ============================================================

@bot.message_handler(commands=["start", "help"])
def enviar_bienvenida(message):

    texto = """
👋 <b>¡Hola!</b>

Soy <b>Tecno</b>, el asistente virtual de la
<b>Unidad Educativa Eduardo Kingman</b>. 🤖

Puedo ayudarte a consultar los horarios de atención
a padres de familia de los docentes.

<b>Ejemplos:</b>

📌 ¿Cuál es el horario del docente Leonardo Salguero?

📌 ¿Cuándo atiende el profesor Villamar?

📌 ¿A qué hora puedo encontrar a Kevin Arellano el martes?

📌 Horario de la profesora Rugel

📌 ¿Cuándo atiende Josué Suña el viernes?

Escribe el nombre del docente y te mostraré
su horario.
"""

    bot.reply_to(
        message,
        texto,
        parse_mode="HTML"
    )


# ============================================================
# RESPONDER MENSAJES
# ============================================================

@bot.message_handler(func=lambda message: True)
def responder_mensaje(message):

    texto_usuario = message.text.strip()

    if not texto_usuario:
        return

    try:

        # ----------------------------------------------------
        # PRIMERO: BUSCAR DIRECTAMENTE EN LOS DATOS
        # ----------------------------------------------------

        respuesta_directa = responder_horario(texto_usuario)

        if respuesta_directa:

            bot.reply_to(
                message,
                respuesta_directa,
                parse_mode="HTML"
            )

            return

        # ----------------------------------------------------
        # SEGUNDO: SI NO ENCUENTRA PROFESOR, USA GROQ
        # ----------------------------------------------------

        respuesta_ia = preguntar_groq(texto_usuario)

        bot.reply_to(
            message,
            respuesta_ia,
            parse_mode="HTML"
        )

    except Exception as e:

        print("Error general:", e)

        bot.reply_to(
            message,
            "⚠️ Ocurrió un error procesando tu mensaje."
        )


# ============================================================
# INICIAR BOT
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("🤖 TECNO - BOT DE TELEGRAM")
    print("🏫 Unidad Educativa Eduardo Kingman")
    print("✅ Bot iniciado correctamente")
    print("=" * 50)

    bot.infinity_polling()