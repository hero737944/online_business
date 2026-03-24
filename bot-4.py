import telebot
import httpx
import threading
from io import BytesIO
from gtts import gTTS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN = "8666749953:AAF1YjpAj6T1B4-akk4nE7zGC7UorS3OAiU"
CHANNEL_LINK = "https://t.me/+b1ueWALIzyczMTk0"

bot = telebot.TeleBot(BOT_TOKEN)

# User state tracking
user_states = {}
WAITING_PROMPT = "waiting_prompt"
WAITING_IMAGE  = "waiting_image"
WAITING_TTS    = "waiting_tts"

# ─── NSFW FILTER ──────────────────────────────────────────────────────────────
NSFW_KEYWORDS = [
    "nude","naked","nsfw","porn","sex","explicit","hentai",
    "adult","xxx","erotic","boob","breast","vagina","penis",
    "18+","sexy naked","undressed","topless"
]

def is_nsfw(text):
    return any(kw in text.lower() for kw in NSFW_KEYWORDS)

# ─── KEYBOARDS ────────────────────────────────────────────────────────────────
def join_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔥 Join My Channel", url=CHANNEL_LINK))
    kb.add(InlineKeyboardButton("✅ I Joined!", callback_data="check_join"))
    return kb

def main_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎨 Click to Make It", callback_data="make_image"))
    kb.add(InlineKeyboardButton("🔍 AI Check", callback_data="ai_check"))
    kb.add(InlineKeyboardButton("🔊 Text to Voice", callback_data="text_to_voice"))
    kb.row(
        InlineKeyboardButton("ℹ️ About", callback_data="about"),
        InlineKeyboardButton("🆘 Help", callback_data="help")
    )
    return kb

def back_kb():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu"))
    return kb

# ─── /start ───────────────────────────────────────────────────────────────────
@bot.message_handler(commands=["start"])
def start(message):
    name = message.from_user.first_name
    user_states.pop(message.chat.id, None)
    bot.send_message(
        message.chat.id,
        f"👾 *Welcome to Denji World!*\n\n"
        f"Hey {name}\\! 🔥\n\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"🤖 *All Bots Are Free To Use\\!*\n"
        f"━━━━━━━━━━━━━━━━━\n\n"
        f"✨ *What can I do?*\n"
        f"🎨 Generate amazing AI images from text\n"
        f"🔍 Detect if a photo is AI\\-generated\n"
        f"🛡️ 100% Safe & Family Friendly\n"
        f"⚡ Fast & Always Online\n\n"
        f"👇 *First, join our channel to unlock all features\\!*",
        parse_mode="MarkdownV2",
        reply_markup=join_kb()
    )

# ─── CALLBACKS ────────────────────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    msg_id  = call.message.message_id
    name    = call.from_user.first_name

    if call.data == "check_join":
        user_states.pop(chat_id, None)
        bot.edit_message_text(
            f"🎉 *Welcome aboard, {name}!*\n\n"
            f"👾 *Denji World is now unlocked!*\n\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Choose what you want to do 👇\n"
            f"━━━━━━━━━━━━━━━━━",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=main_kb()
        )

    elif call.data == "back_menu":
        user_states.pop(chat_id, None)
        bot.edit_message_text(
            "👾 *Denji World — Main Menu*\n\nChoose karo kya karna hai 👇",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=main_kb()
        )

    elif call.data == "make_image":
        user_states[chat_id] = WAITING_PROMPT
        bot.edit_message_text(
            "🎨 *Image Generator*\n\n"
            "✍️ Apna idea type karo!\n\n"
            "_Example: a dragon in a cyberpunk city at night_\n\n"
            "🛡️ Note: 18+ / NSFW content blocked hai.",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_kb()
        )

    elif call.data == "ai_check":
        user_states[chat_id] = WAITING_IMAGE
        bot.edit_message_text(
            "🔍 *AI Image Detector*\n\n"
            "📸 Koi bhi photo bhejo!\n"
            "Main bataunga *kitna % AI-generated* hai!\n\n"
            "_Real photos vs AI images detect karta hun_ 🤖",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_kb()
        )

    elif call.data == "text_to_voice":
        user_states[chat_id] = WAITING_TTS
        bot.edit_message_text(
            "🔊 *Text to Voice*\n\n"
            "✍️ Jo text aap voice me convert karna chahte ho, woh bhejo.\n\n"
            "_Example: Hello, welcome to my Telegram bot!_",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_kb()
        )

    elif call.data == "about":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="back_menu"))
        kb.add(InlineKeyboardButton("🔥 Join Channel", url=CHANNEL_LINK))
        bot.edit_message_text(
            "👾 *About Denji World*\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🤖 *Version:* 1.0\n"
            "⚡ *Status:* Online 24/7\n"
            "🆓 *Price:* 100% Free\n"
            "🛡️ *Safe:* NSFW Blocked\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "✨ Built with ❤️ for Denji World\n"
            "📢 Join our community for updates!",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=kb
        )

    elif call.data == "help":
        bot.edit_message_text(
            "🆘 *Help & Commands*\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🎨 *Click to Make It*\n"
            "  → Text likho, AI image banega\n\n"
            "🔍 *AI Check*\n"
            "  → Photo bhejo, AI % batayega\n\n"
            "🔊 *Text to Voice*\n"
            "  → Text bhejo, voice note milega\n\n"
            "🛡️ *18+ Content*\n"
            "  → Automatically blocked\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "💬 Problems? Channel pe message karo!",
            chat_id, msg_id,
            parse_mode="Markdown",
            reply_markup=back_kb()
        )

    bot.answer_callback_query(call.id)

# ─── MESSAGE HANDLER ──────────────────────────────────────────────────────────
@bot.message_handler(func=lambda m: True, content_types=["text", "photo", "document"])
def handle_messages(message):
    chat_id = message.chat.id
    state   = user_states.get(chat_id)

    # Image generation
    if state == WAITING_PROMPT and message.content_type == "text":
        prompt = message.text.strip()
        user_states.pop(chat_id, None)

        if is_nsfw(prompt):
            bot.send_message(
                chat_id,
                "🚫 *18+ / NSFW content allowed nahi hai!*\n\nPlease ek safe prompt try karo. 😊",
                parse_mode="Markdown",
                reply_markup=main_kb()
            )
            return

        msg = bot.send_message(chat_id, "⚡ *Generating your image...*\n🔄 AI kaam kar rahi hai...", parse_mode="Markdown")

        def gen():
            try:
                safe_prompt = prompt.replace(" ", "%20")
                url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true&enhance=true"
                with httpx.Client(timeout=60) as client:
                    r = client.get(url)
                bot.delete_message(chat_id, msg.message_id)
                bot.send_photo(
                    chat_id,
                    r.content,
                    caption=f"✅ *Image Ready!*\n\n📝 *Prompt:* `{prompt}`\n\n👾 _Powered by Denji World AI_ 🔥",
                    parse_mode="Markdown",
                    reply_markup=main_kb()
                )
            except Exception as e:
                bot.edit_message_text("❌ *Image generate nahi ho payi.*\n\nDobara try karo!", chat_id, msg.message_id, parse_mode="Markdown", reply_markup=main_kb())

        threading.Thread(target=gen).start()

    # AI image check
    elif state == WAITING_IMAGE and message.content_type in ["photo", "document"]:
        user_states.pop(chat_id, None)
        msg = bot.send_message(chat_id, "🔍 *Analyzing image...*\n🧠 AI patterns check ho rahe hain...", parse_mode="Markdown")

        def check():
            try:
                if message.content_type == "photo":
                    file_info = bot.get_file(message.photo[-1].file_id)
                else:
                    file_info = bot.get_file(message.document.file_id)

                downloaded = bot.download_file(file_info.file_path)

                with httpx.Client(timeout=30) as client:
                    r = client.post(
                        "https://api.sightengine.com/1.0/check.json",
                        data={"models": "ai-generated", "api_user": "1444910059", "api_secret": "DGmPDpHa4GarxbFGkJVKJCaFYRAtHjk6"},
                        files={"media": ("image.jpg", downloaded, "image/jpeg")}
                    )
                    result = r.json()

                if "ai_generated" in result:
                    ai_pct = round(result["ai_generated"].get("ai_generated", 0) * 100, 1)
                    hu_pct = round(100 - ai_pct, 1)

                    if ai_pct >= 75:   verdict, emoji = "🤖 *Almost Certainly AI Generated!*", "🔴"
                    elif ai_pct >= 50: verdict, emoji = "⚠️ *Likely AI Generated*", "🟡"
                    elif ai_pct >= 25: verdict, emoji = "🤔 *Possibly AI Generated*", "🟠"
                    else:              verdict, emoji = "✅ *Likely a Real Photo!*", "🟢"

                    bar = "█" * int(ai_pct/10) + "░" * (10 - int(ai_pct/10))
                    text = (
                        f"🔍 *AI Detection Result*\n\n{verdict}\n\n"
                        f"━━━━━━━━━━━━━━━━━\n"
                        f"{emoji} AI Generated: *{ai_pct}%*\n"
                        f"👤 Human Made:  *{hu_pct}%*\n\n"
                        f"📊 `[{bar}]`\n"
                        f"━━━━━━━━━━━━━━━━━\n\n"
                        f"👾 _Powered by Denji World AI_"
                    )
                else:
                    text = "❌ *Detection failed.* Clearer image bhejo ya dobara try karo."

                bot.delete_message(chat_id, msg.message_id)
                bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=main_kb())

            except Exception as e:
                bot.edit_message_text("❌ *Analysis fail ho gayi!*\n\nDobara try karo.", chat_id, msg.message_id, parse_mode="Markdown", reply_markup=main_kb())

        threading.Thread(target=check).start()

    # Text to voice
    elif state == WAITING_TTS and message.content_type == "text":
        text_to_convert = message.text.strip()
        user_states.pop(chat_id, None)

        if not text_to_convert:
            bot.send_message(
                chat_id,
                "⚠️ *Text empty hai.*\n\nPlease kuch text bhejo.",
                parse_mode="Markdown",
                reply_markup=main_kb()
            )
            return

        msg = bot.send_message(chat_id, "🔊 *Converting text to voice...*", parse_mode="Markdown")

        def make_voice():
            try:
                tts = gTTS(text=text_to_convert, lang="en")
                audio_file = BytesIO()
                tts.write_to_fp(audio_file)
                audio_file.seek(0)
                audio_file.name = "voice.mp3"

                bot.delete_message(chat_id, msg.message_id)
                bot.send_audio(
                    chat_id,
                    audio=audio_file,
                    caption="✅ *Voice Ready!*",
                    parse_mode="Markdown",
                    reply_markup=main_kb()
                )
            except Exception:
                bot.edit_message_text(
                    "❌ *Voice generate nahi ho payi.*\n\nDobara try karo!",
                    chat_id,
                    msg.message_id,
                    parse_mode="Markdown",
                    reply_markup=main_kb()
                )

        threading.Thread(target=make_voice).start()

    else:
        bot.send_message(
            chat_id,
            "👾 *Denji World*\n\n/start likho ya niche buttons use karo!",
            parse_mode="Markdown",
            reply_markup=main_kb()
        )

# ─── RUN ──────────────────────────────────────────────────────────────────────
print("👾 Denji World Bot is running...")
bot.infinity_polling()
