from pyrogram import types, Client, filters
from pyrogram.types import InputMediaPhoto
import config # config.py se image lene ke liye

class HelpInline:
    # Aapke purane methods (ikb aur ikm)
    def ikb(self, text, callback_data):
        return types.InlineKeyboardButton(text=text, callback_data=callback_data)

    def ikm(self, rows):
        return types.InlineKeyboardMarkup(rows)

    def help_markup(self, _lang: dict, back: bool = False) -> types.InlineKeyboardMarkup:
        if back:
            rows = [[self.ikb(text=_lang["back"], callback_data="help back"), 
                     self.ikb(text=_lang["close"], callback_data="help close")]]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            # Aapke logic ke hisaab se buttons
            buttons = [self.ikb(text=_lang[f"help_{cb}"], callback_data=f"help {cb}") for cb in cbs]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            rows.append([self.ikb(text=_lang["close"], callback_data="help close")])
            
        return self.ikm(rows)

# --- Bot Handlers (Yahan image show hogi) ---

h_inline = HelpInline()

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    # _lang ko yahan load karein (Example ke liye empty dict)
    markup = h_inline.help_markup(_lang)
    
    # Message ki jagah Photo bhej rahe hain
    await message.reply_photo(
        photo=config.HELP_IMG, # Config se image uthayi
        caption="Yahan aapka help message aayega",
        reply_markup=markup
    )

@Client.on_callback_query(filters.regex(r"help"))
async def help_callback(client, callback_query):
    data = callback_query.data.split()
    
    if data[1] == "back":
        # Back dabane par wapis image aur main menu dikhegi
        await callback_query.edit_message_media(
            media=InputMediaPhoto(config.HELP_IMG, caption="Main Help Menu"),
            reply_markup=h_inline.help_markup(_lang, back=False)
        )
    
    elif data[1] == "close":
        await callback_query.message.delete()
    
    else:
        # Kisi category par click karne par (Admins, Play etc)
        await callback_query.edit_message_media(
            media=InputMediaPhoto(config.HELP_IMG, caption=f"Ye {data[1]} ka menu hai"),
            reply_markup=h_inline.help_markup(_lang, back=True)
                   )
