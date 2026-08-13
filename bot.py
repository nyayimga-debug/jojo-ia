"""Bot Telegram pour récupérer les IDs (utilisateur, groupes, canaux publics/privés)."""

import logging
import os

from dotenv import load_dotenv
from telegram import (
    Chat,
    KeyboardButton,
    KeyboardButtonRequestChat,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.constants import ChatType
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

CHAT_TYPE_LABELS = {
    ChatType.PRIVATE: "Chat privé",
    ChatType.GROUP: "Groupe",
    ChatType.SUPERGROUP: "Supergroupe",
    ChatType.CHANNEL: "Canal",
}

BTN_MY_ID = "🆔 My ID"
BTN_MY_CHANNEL = "📢 My Channel"
BTN_MY_GROUP = "👥 My Group"
BTN_MY_FORUM = "🧵 My Forum"

# request_id envoyé par Telegram dans le ChatShared correspondant, pour
# savoir quel bouton a déclenché le partage.
REQUEST_ID_CHANNEL = 1
REQUEST_ID_GROUP = 2
REQUEST_ID_FORUM = 3

SHARED_CHAT_LABELS = {
    REQUEST_ID_CHANNEL: "📢 Canal partagé",
    REQUEST_ID_GROUP: "👥 Groupe partagé",
    REQUEST_ID_FORUM: "🧵 Forum partagé",
}


def build_main_keyboard() -> ReplyKeyboardMarkup:
    """Clavier persistant avec les raccourcis ID / Canal / Groupe / Forum."""
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton(BTN_MY_ID)],
            [
                KeyboardButton(
                    BTN_MY_CHANNEL,
                    request_chat=KeyboardButtonRequestChat(
                        request_id=REQUEST_ID_CHANNEL,
                        chat_is_channel=True,
                        request_title=True,
                        request_username=True,
                    ),
                ),
                KeyboardButton(
                    BTN_MY_GROUP,
                    request_chat=KeyboardButtonRequestChat(
                        request_id=REQUEST_ID_GROUP,
                        chat_is_channel=False,
                        request_title=True,
                        request_username=True,
                    ),
                ),
            ],
            [
                KeyboardButton(
                    BTN_MY_FORUM,
                    request_chat=KeyboardButtonRequestChat(
                        request_id=REQUEST_ID_FORUM,
                        chat_is_channel=False,
                        chat_is_forum=True,
                        request_title=True,
                        request_username=True,
                    ),
                )
            ],
        ],
        resize_keyboard=True,
    )


def format_chat_info(chat: Chat) -> str:
    lines = [
        f"📌 Type : {CHAT_TYPE_LABELS.get(chat.type, chat.type)}",
        f"🆔 ID : `{chat.id}`",
    ]
    if chat.title:
        lines.append(f"📛 Titre : {chat.title}")
    if chat.username:
        lines.append(f"🔗 Username : @{chat.username} (public)")
    else:
        lines.append("🔒 Pas de username public (privé)")
    return "\n".join(lines)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = (
        f"👋 Salut {user.first_name} !\n\n"
        "Je peux te donner l'ID :\n"
        "• De ton compte utilisateur\n"
        "• De n'importe quel groupe / supergroupe\n"
        "• De n'importe quel canal, public ou privé\n\n"
        "*Comment faire :*\n"
        "1️⃣ Envoie /id ici pour connaître ton propre ID.\n"
        "2️⃣ Ajoute-moi dans un groupe ou un canal (comme membre, "
        "admin si c'est un canal) puis envoie /id là-bas, ou "
        "attends mon message automatique dès que je rejoins.\n"
        "3️⃣ Transfère-moi (forward) n'importe quel message venant "
        "d'un groupe ou d'un canal — même privé — et je t'en donne "
        "l'ID, sans avoir besoin d'y être ajouté.\n\n"
        "👇 Ou utilise directement les boutons ci-dessous."
    )
    await update.message.reply_markdown(text, reply_markup=build_main_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    parts = [format_chat_info(chat)]

    if chat.type == ChatType.PRIVATE and user:
        parts = [
            "👤 *Tes informations*",
            f"🆔 Ton ID : `{user.id}`",
            f"🔗 Username : @{user.username}" if user.username else "🔒 Pas de username",
        ]
    elif user:
        parts.append("")
        parts.append(f"🙋 ID de l'expéditeur : `{user.id}`")

    await message.reply_markdown("\n".join(parts))


async def handle_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gère les messages transférés (forward) pour extraire l'ID de la source."""
    message = update.effective_message
    origin = message.forward_origin

    if origin is None:
        return

    origin_type = origin.type

    if origin_type == "user":
        src_user = origin.sender_user
        text = (
            "👤 *Message transféré depuis un utilisateur*\n"
            f"🆔 ID : `{src_user.id}`\n"
            f"🔗 Username : @{src_user.username}"
            if src_user.username
            else f"🆔 ID : `{src_user.id}`\n🔒 Pas de username"
        )
    elif origin_type == "hidden_user":
        text = (
            "🙈 *Message transféré depuis un utilisateur*\n"
            f"Nom affiché : {origin.sender_user_name}\n"
            "🔒 L'ID n'est pas accessible (confidentialité de la source "
            "désactivée par l'utilisateur)."
        )
    elif origin_type == "chat":
        src_chat = origin.sender_chat
        text = "💬 *Message transféré depuis un groupe*\n" + format_chat_info(src_chat)
    elif origin_type == "channel":
        src_chat = origin.chat
        text = "📢 *Message transféré depuis un canal*\n" + format_chat_info(src_chat)
    else:
        text = "❓ Origine du message inconnue."

    await message.reply_markdown(text)


async def my_id_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Réagit au bouton « My ID » du clavier persistant."""
    await id_command(update, context)


async def handle_chat_shared(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reçoit le chat choisi via les boutons « My Channel/Group/Forum »."""
    shared = update.effective_message.chat_shared
    if shared is None:
        return

    label = SHARED_CHAT_LABELS.get(shared.request_id, "💬 Chat partagé")
    lines = [f"{label}", f"🆔 ID : `{shared.chat_id}`"]
    if shared.title:
        lines.append(f"📛 Titre : {shared.title}")
    if shared.username:
        lines.append(f"🔗 Username : @{shared.username}")

    await update.effective_message.reply_markdown(
        "\n".join(lines), reply_markup=build_main_keyboard()
    )


async def on_bot_added_to_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Annonce automatiquement l'ID quand le bot est ajouté à un groupe/canal."""
    result = update.my_chat_member
    if result is None:
        return

    old_status = result.old_chat_member.status
    new_status = result.new_chat_member.status

    joined_statuses = {"member", "administrator"}
    left_statuses = {"left", "kicked"}

    if old_status in left_statuses and new_status in joined_statuses:
        chat = result.chat
        text = "✅ *Je viens d'être ajouté ici !*\n\n" + format_chat_info(chat)
        try:
            await context.bot.send_message(
                chat_id=chat.id, text=text, parse_mode="Markdown"
            )
        except Exception:
            logger.info(
                "Impossible d'envoyer un message dans %s (%s) — "
                "je n'ai probablement pas le droit d'écrire.",
                chat.id,
                chat.title,
            )


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit(
            "Erreur : la variable d'environnement TELEGRAM_BOT_TOKEN est manquante. "
            "Copie .env.example vers .env et renseigne ton token BotFather."
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(MessageHandler(filters.Text([BTN_MY_ID]), my_id_button))
    application.add_handler(
        MessageHandler(filters.StatusUpdate.CHAT_SHARED, handle_chat_shared)
    )
    application.add_handler(MessageHandler(filters.FORWARDED, handle_forward))
    application.add_handler(
        ChatMemberHandler(on_bot_added_to_chat, ChatMemberHandler.MY_CHAT_MEMBER)
    )

    logger.info("Bot démarré, en attente de messages...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
