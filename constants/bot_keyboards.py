from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

USE_BAG_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("پخت", callback_data="bake")],
        [InlineKeyboardButton("مغازه داران", callback_data="shopkeeper")],
        [InlineKeyboardButton("رایگان", callback_data="needy")],
        [InlineKeyboardButton("فروش تکی", callback_data="sold")],
    ]
)

USAGE_LIST_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("لیست پخت", callback_data="list_bake")],
        [InlineKeyboardButton("لیست مغازه داران", callback_data="list_shopkeeper")],
        [InlineKeyboardButton("لیست رایگان ها", callback_data="list_needy")],
        [InlineKeyboardButton("لیست فروش تکی", callback_data="list_sold")],
    ]
)