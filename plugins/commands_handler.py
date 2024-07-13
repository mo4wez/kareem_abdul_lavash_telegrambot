import asyncio
import jdatetime
import datetime
import pyromod
from pyrogram import Client, filters
from peewee import fn
from models.database import Inventory, BagUsage, OldInventory
from constants.bot_messages import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    USE_BAG_MESSAGE,
    REOPRT_MESSAGE,
    TOTAL_REPORT_MESSAGE,
    BAG_TYPE_MAPPING,
    SELECTED_USAGE_TYPE_MESSAGE,
    ENTER_NAME_MESSAGE,
    ENTER_PHONE_MESSAGE,
    NOT_ENOUGH_INVENTORY_MESSAGE,
    NOT_INVENTORY_AVAILABLE_MESSAGE,
    RECORD_SAVED_MESSAGE,
    INVALID_AMOUNT_MESSAGE,
    USAGE_LIST_FOR_MESSAGE,
    USAGE_LIST_TEXT,
    USAGE_LIST_EMPTY_MESSAGE,
    SELECT_USAGE_LIST_TEXT,
    ADDED_INVENTORY_TEXT,
    ADD_TO_INVENTORY_ERROR_TEXT,
    ENTER_RECEIVED_AMOUNT_TEXT,
)
from constants.bot_keyboards import USE_BAG_KEYBOARD, USAGE_LIST_KEYBOARD


def get_current_datetime():
    # Convert jdatetime to standard datetime
    j_now = jdatetime.datetime.now()
    return datetime.datetime(j_now.year, j_now.month, j_now.day, j_now.hour, j_now.minute, j_now.second)

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(WELCOME_MESSAGE)

@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply(HELP_MESSAGE)

@Client.on_message(filters.command("add_received"))
async def add_received(client, message):
    chat_id = message.chat.id
    try:
        await message.reply(ENTER_RECEIVED_AMOUNT_TEXT)
        count_msg = await client.listen(chat_id)
        count = int(count_msg.text)  # Convert the message text to an integer
        Inventory.create(bags_received=count, bags_remaining=count, date_received=get_current_datetime())
        await message.reply(ADDED_INVENTORY_TEXT.format(count))
    except (IndexError, ValueError):
        await message.reply(ADD_TO_INVENTORY_ERROR_TEXT)

@Client.on_message(filters.command("use_bag"))
async def use_bag(client, message):
    await message.reply(text=USE_BAG_MESSAGE, reply_markup=USE_BAG_KEYBOARD)


@Client.on_message(filters.command("list_bag_users"))
async def list_bag_users(client, message):
    await message.reply(text=SELECT_USAGE_LIST_TEXT, reply_markup=USAGE_LIST_KEYBOARD)


@Client.on_callback_query()
async def handle_usage_type(client, callback_query):
    if callback_query.data.startswith("list_"):
        usage_type = callback_query.data.split("_")[1]

        type_persian = BAG_TYPE_MAPPING[usage_type]

        usages = BagUsage.select().where(BagUsage.type == usage_type)
        if usages:
            response = USAGE_LIST_FOR_MESSAGE.format(type_persian)
            for usage in usages:
                response += USAGE_LIST_TEXT.format(usage.name or 'N/A', usage.amount, usage.date, usage.phone or 'N/A')
        else:
            response = USAGE_LIST_EMPTY_MESSAGE.format(type_persian)

        await callback_query.message.reply(response)
    elif callback_query.data in ['bake', 'shopkeeper', 'needy', 'sold']:
        s_usage_type = callback_query.data
        for usage_type, persian_name in BAG_TYPE_MAPPING.items():
            if usage_type == s_usage_type:
                s_persian_name = persian_name
                await callback_query.message.reply(SELECTED_USAGE_TYPE_MESSAGE.format(persian_name))
                response = await client.listen(callback_query.message.chat.id)

        try:
            amount = int(response.text)
            await callback_query.message.reply(ENTER_NAME_MESSAGE)
            name_response = await client.listen(callback_query.message.chat.id)
            name = name_response.text if name_response.text.strip() else None

            await callback_query.message.reply(ENTER_PHONE_MESSAGE)
            phone_response = await client.listen(callback_query.message.chat.id)
            phone = phone_response.text if phone_response.text.strip() else None

            inventory = Inventory.select().where(Inventory.bags_remaining > 0).order_by(Inventory.date_received).get()
            if inventory.bags_remaining < amount:
                await callback_query.message.reply(NOT_ENOUGH_INVENTORY_MESSAGE.format(inventory.bags_remaining))
                return
            
            BagUsage.create(inventory=inventory, type=s_usage_type, amount=amount, name=name, phone=phone, date=get_current_datetime())
            inventory.bags_remaining -= amount
            inventory.save()

            await callback_query.message.reply(RECORD_SAVED_MESSAGE.format(amount, s_persian_name))
        except ValueError:
            await callback_query.message.reply(INVALID_AMOUNT_MESSAGE)
        except Inventory.DoesNotExist:
            await callback_query.message.reply(NOT_INVENTORY_AVAILABLE_MESSAGE)

@Client.on_message(filters.command("report"))
async def report(client, message):
    total_received = Inventory.select(fn.SUM(Inventory.bags_received)).scalar() or 0
    total_remaining = Inventory.select(fn.SUM(Inventory.bags_remaining)).scalar() or 0
    total_used = total_received - total_remaining

    total_old_rem = OldInventory.select(fn.SUM(OldInventory.bags_remaining)).scalar() or 0

    report_text = REOPRT_MESSAGE.format(
        total_received,
        total_used,
        total_remaining,
        total_old_rem,
    )

    for bag_type, persian_name in BAG_TYPE_MAPPING.items():
        used = BagUsage.select(fn.SUM(BagUsage.amount)).where(BagUsage.type == bag_type).scalar() or 0
        report_text += TOTAL_REPORT_MESSAGE.format(persian_name, used) + '\n'

    await message.reply(report_text)

@Client.on_message(filters.command("move_old_bags"))
async def move_old_bags(client, message):
    chat_id = message.chat.id

    old_bags = Inventory.select().where(Inventory.bags_remaining > 0)

    if old_bags:
        try:
            await message.reply("لطفاً تعداد کیسه هایی که می خواهید به موجودی قدیمی منتقل کنید را وارد کنید:")
            count_msg = await client.listen(chat_id)
            count = int(count_msg.text)  # Convert the message text to an integer

            total_bags_remaining = sum(bag.bags_remaining for bag in old_bags)
            if count > total_bags_remaining:
                await message.reply(f'تعداد کیسه های موجود برای انتقال کافی نیست. حداکثر تعداد کیسه های قابل انتقال: {total_bags_remaining}')
                return

            bags_to_move = count
            for old_bag in old_bags:
                if bags_to_move <= 0:
                    break
                if old_bag.bags_remaining <= bags_to_move:
                    bags_to_move -= old_bag.bags_remaining
                    OldInventory.create(
                        bags_remaining=old_bag.bags_remaining,
                        date_received=old_bag.date_received
                    )
                    old_bag.delete_instance()
                else:
                    OldInventory.create(
                        bags_remaining=bags_to_move,
                        date_received=old_bag.date_received
                    )
                    old_bag.bags_remaining -= bags_to_move
                    old_bag.save()
                    bags_to_move = 0

            await message.reply('آرد های قدیمی از کیسه های جدید جدا شدند')
        except (IndexError, ValueError):
            await message.reply("لطفاً یک عدد معتبر وارد کنید.")
    else:
        await message.reply('کیسه ای برای انتقال در انبار موجود نیست.')
