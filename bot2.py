from telebot.types import (
    InlineKeyboardMarkup as markup, 
    InlineKeyboardButton as Button
)
import requests
import redis
from telebot import TeleBot
from kvsqlite.sync import Client

user = Client('ids.sqlite','users')
ban = Client('ban.sqlite', 'ban')
TOKEN = "7572549807:AAFCrBBoxS9Jn3DKpK-_YdLEZKyaUCqwKCQ"
id = "6264668799"
ch = [ '@B_6ODA' , '@Your_uncle_Muhammad']
bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):    
    idu = msg.from_user.id
    if ban.exists(f'user_{idu}'):
        bot.reply_to(msg, 'عذرا عزيزي انت محظور')
        return    
    notY = []
    for channel in ch:
        cin = bot.get_chat(channel)
        chat_m = bot.get_chat_member(chat_id=cin.id, user_id=idu)
        if chat_m.status not in ['creator', 'member', 'administrator']:
            notY.append(channel)    
    if notY:
        channels_list = "\n".join(notY)
        bot.reply_to(
            msg,
            f"عذرا عزيزي المستخدم، عليك الاشتراك في قنوات البوت لتتمكن من استخدامه:\n{channels_list}\n- - - - - - - - - - \nاشترك ثم ارسل /start"
        )
    else:
        if str(idu) in id:
            ad = markup()
            o1 = Button(text='الاحصائيات', callback_data='status')
            o2 = Button(text='اذاعة', callback_data='cast')
            o3 = Button(text='حظر مستخدم', callback_data='ban')
            o4 = Button(text='الغاء حظر مستخدم', callback_data='unban')
            o5 = Button(text='ارسال التخزين',callback_data='get')
            ad.add(o1, o2)
            ad.add(o3, o4)
            ad.add(o5)
            bot.reply_to(msg, 'اهلا عزيزي المتحكم  اليك ازرار التحكم', reply_markup=ad)
        moh = markup()
        don = Button(text='بدء التحميل', callback_data='started')
        link = Button('Click here', url='https://Your_uncle_Muhammad.t.me')
        moh.add(don)
        moh.add(link)
        bot.reply_to(msg, "مرحبا 👋 إضغط على زر 'بدء التحميل' \n🔗  ⋮  وأرسل الرابط", reply_markup=moh)

@bot.callback_query_handler(func=lambda call: True)
def cal(call):
    notY = []
    user_id = call.from_user.id    
    if call.data == 'started':
        if notY: 
            channels_list = "\n".join(notY)
            bot.reply_to(
                call.message,
                f"عذرا عزيزي المستخدم، عليك الاشتراك في قنوات البوت لتتمكن من استخدامه:\n{channels_list}\n- - - - - - - - - - \nاشترك ثم ارسل /start"
            )
        elif ban.exists(f'user_{user_id}'):
            bot.reply_to(call.message, 'عذرا عزيزي انت محظور')
            return
        else:
            A = bot.edit_message_text(text='🔗 | ارسل رابط الفيديو: ', chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.register_next_step_handler(A, don_video)    
    elif call.data == 'status':
        stats(call.message) 
    elif call.data == 'get':
    	get(call.message)
    elif call.data == 'cast':
        A = bot.edit_message_text(text='🔗 | ارسل ماتريد اذاعته(نص او رسالة صوتية او جميع الميديا)', chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(A, broad)
    
    elif call.data == 'ban':
        A = bot.edit_message_text(text='ارسل الايدي لـ حظره', chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(A, band)
    
    elif call.data == 'unban':
        A = bot.edit_message_text(text='ارسل ايديه لـ الغاء حظره', chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.register_next_step_handler(A, un)
        	
def don_video(message):
    try:
        us = bot.get_me().username
        m = message.text
        idd = message.from_user.id
        mc = message.chat.id
        url = f"https://www.tikwm.com/api/?url={m}"
        res = requests.get(url).json()

        if 'data' not in res or 'play' not in res['data'] or 'title' not in res['data']:
            bot.reply_to(message, "- لم أتمكن من جلب الفيديو. يرجى التحقق من الرابط.")
            return
        wait = bot.reply_to(message, "جاري التحميل ===>")
        video = res['data']['play']
        bot.delete_message(message.chat.id, wait.message_id)  
        bot.send_video(mc, video, caption=f'- @{us} .',  reply_to_message_id=message.message_id)   
        if r:
            r.set(f"history:{idd}", f"{title}")
            r.set(f"link:{idd}", f"{m}")
    except Exception as e:
        print(f"Error in t handler: {str(e)}")
        return
def band(msg):
    try:
        idM = int(msg.text)
        bann.set(f'user_{user_id}', {'id': idM})
        bot.reply_to(msg, 'تم حظره')
    except ValueError:
        bot.reply_to(msg, 'خطأ في الايدي !')
def unban(message):
    try:
        user_id = int(message.text)
        if bann.exists(f'user_{user_id}'):
            bann.delete(f'user_{user_id}')
            bot.reply_to(message, 'تم إلغاء حظر المستخدم.')
        else:
            bot.reply_to(message, 'المستخدم غير محظور.')
    except ValueError:
        bot.reply_to(message,'خطأ في الايدي')
        
def get(msg):
    with open('ids.sqlite', 'rb') as file:
        bot.send_document(msg.chat.id, file)
    with open('ban.sqlite', 'rb') as file_bannd:
        bot.send_document(msg.chat.id, file_bannd)                
def stats(message):
    kysU = user.keys()
    kysB = ban.keys()    
    users = len(kysU) if kysU is not None else 0   
    Banned = len(kysB) if kysB is not None else 0 
    iL = f"مستخدمين البوت : {users}\n"
    iL += f"المحظورين : {Banned}"    
    bot.reply_to(message, iL)
    
def broad(message):
    bot.reply_to(message, 'جارٍ الإذاعة، الرجاء الانتظار...')
    keys = user.keys()
    users = []
    total = 0
    failed = 0    
    if not keys:
        bot.reply_to(message, 'لا يوجد مستخدمين لإرسال الرسالة.')
        return    
    for i in keys:
        key = i[0]
        try: 
            users.append(user.get(key)['id'])
        except:
            continue    
    for i in users:
        try:
            bot.copy_message(chat_id=i, from_chat_id=message.chat.id, message_id=message.message_id)
            total += 1
        except:
            failed += 1
            continue    
    rate = (total / len(keys)) * 100 if len(keys) > 0 else 0    
    bot.reply_to(message, f'''==============
    - الكلي : {len(keys)}
    - نجحت لـ : {total}
    - فشلت لـ : {failed}
    - النسبة المئوية : {rate:.2f}%
==============
    - @{bot.get_me().username}''')    
    
bot.infinity_polling()
