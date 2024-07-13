WELCOME_MESSAGE = 'به ربات مدیریت خبازی کریم عبداللواش خوش آمدید برای نحوه استفاده از ربات دستور /help را بزنید.'
HELP_MESSAGE = '''
/add_received  - اضافه کردن کیسه آرد به انبار
/use_bag     - ثبت کیسه های آرد استفاده شده (پخت، مغازه دار ها؛ رایگان، فروخته شده)
/report - نمایش موجودی انبار
/list_bag_users - لیست استفاده کنندگان
'''
USE_BAG_MESSAGE = 'نوع استفاده از کیسه آرد را انتخاب کنید:'

SELECTED_USAGE_TYPE_MESSAGE = 'نوع استفاده {} انتخاب شده است. تعداد کیسه ها را وارد کنید:'
ENTER_NAME_MESSAGE = 'نام استفاده کننده را وارد کنید (می تواند خالی باشد):'
ENTER_PHONE_MESSAGE = 'تلفن استفاده کننده را وارد کنید (می تواند خالی باشد):'
NOT_ENOUGH_INVENTORY_MESSAGE = 'موجودی انبار کافی نیست، فقط {} کیسه با قی مانده.'
RECORD_SAVED_MESSAGE = 'تعداد {} کیسه برای {} ثبت شد.'
INVALID_AMOUNT_MESSAGE = 'برای تعداد کیسه باید مقدار عددی وارد کنید.'
NOT_INVENTORY_AVAILABLE_MESSAGE = 'موجودی در دسترس نیست.'

REOPRT_MESSAGE = '''
گزارش انبار:
    - کل دریافتی در این ماه: {} کیسه
    - تعداد استفاده شده: {} کیسه
    - تعداد باقی مانده: {} کیسه

موجودی کیسه های قدیمی:
    - {} کیسه
 
'''
TOTAL_REPORT_MESSAGE = '- {}: {} کیسه'

BAG_TYPE_MAPPING = {
    'bake': 'پخت',
    'shopkeeper': 'مغازه داران',
    'needy': 'رایگان',
    'sold': 'فروش تکی'
}

SELECT_USAGE_LIST_TEXT = "نوع لیست استفاده را انتخاب کنید:"
USAGE_LIST_FOR_MESSAGE = "لیست استفاده برای {}:\n"
USAGE_LIST_TEXT = "نام: {}\nتعداد: {}\nتاریخ: {}\nتلفن: {}\n\n"
USAGE_LIST_EMPTY_MESSAGE = 'لیست {} خالی است.'

ENTER_RECEIVED_AMOUNT_TEXT = 'تعداد کیسه آرد ورودی را به عدد وارد کنید:'
ADDED_INVENTORY_TEXT = '{} کیسه به انبار اضافه شد.'
ADD_TO_INVENTORY_ERROR_TEXT = 'خطایی رخ داد، مجدد تلاش کنید.'