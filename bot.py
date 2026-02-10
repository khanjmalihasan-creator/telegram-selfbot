#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# سلف بات کامل - نسخه Railway

import os
import sys
import time
import random
import asyncio
from datetime import datetime
import pytz
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import InputPhotoEmpty
import logging

# ========== تنظیمات شما ==========
API_ID = 31266351  # همین رو بذار
API_HASH = '0c86dc56c8937015b96c0f306e91fa05'  # همین رو بذار
PHONE_NUMBER = '+989396612827'  # شماره خودت
# =================================

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# کلاس سلف بات
class PersianSelfBot:
    def __init__(self):
        self.client = None
        self.enemy_mode = False
        self.enemy_id = None
        self.enemy_name = None
        self.session_name = "persian_selfbot"
        
        # لیست فحش‌های رکیک
        self.bad_words = [
            "کص ننت", "کیرم دهنت", "جنده", "کونی", "لاشی",
            "کص کش", "حروم زاده", "گاییدمت", "ننه جنده",
            "کص خل", "خارکصه", "تخم سگ", "بی ناموس",
            "مادر قهوه", "پدر سگ", "خواهر جنده"
        ]
        
    async def start(self):
        """شروع سلف بات"""
        print("=" * 60)
        print("🔥 سلف بات فارسی در حال راه‌اندازی...")
        print(f"📱 شماره: {PHONE_NUMBER}")
        print("=" * 60)
        
        try:
            # ایجاد کلاینت تلگرام
            self.client = TelegramClient(
                self.session_name,
                API_ID,
                API_HASH,
                device_model="iPhone 14 Pro",
                system_version="iOS 16.0",
                app_version="Telegram iOS 9.0",
                lang_code="fa"
            )
            
            # اتصال به تلگرام
            print("📡 در حال اتصال به تلگرام...")
            await self.client.start(phone=PHONE_NUMBER)
            
            # نمایش اطلاعات اکانت
            me = await self.client.get_me()
            print(f"✅ متصل شدیم به: {me.first_name} (@{me.username})")
            print(f"🆔 ID: {me.id}")
            
            # شروع وظایف
            asyncio.create_task(self.update_profile_time())
            asyncio.create_task(self.keep_alive())
            
            # تنظیم هندلرها
            await self.setup_handlers()
            
            # نمایش پیام شروع
            await self.show_welcome()
            
            # اجرای دائمی
            print("\n🎯 سلف بات فعال شد و منتظر پیام‌هاست...")
            await self.client.run_until_disconnected()
            
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی: {e}")
            print("لطفاً دوباره تلاش کنید...")
            time.sleep(5)
            await self.start()
    
    async def update_profile_time(self):
        """آپدیت زمان ایران روی پروفایل"""
        print("🕒 شروع آپدیت زمان پروفایل...")
        
        while True:
            try:
                # زمان ایران
                iran_tz = pytz.timezone('Asia/Tehran')
                now = datetime.now(iran_tz)
                
                # فرمت‌های مختلف زمان
                time_formats = [
                    f"⏰ {now.strftime('%H:%M')} تهران",
                    f"🕒 {now.strftime('%H:%M')} | ایران",
                    f"📅 {now.strftime('%Y/%m/%d')} {now.strftime('%H:%M')}",
                    f"✨ {now.strftime('%H:%M')} TEH",
                    f"⭐ {now.strftime('%H:%M')} IR"
                ]
                
                # انتخاب رندوم یک فرمت
                new_name = random.choice(time_formats)
                
                # آپدیت اسم پروفایل
                await self.client(UpdateProfileRequest(
                    first_name=new_name,
                    about="🔺به دلیل مشغله کاری و قطعی مکرر اینترنت ممکنه کمی با تاخیر جواب بگیرید"
                ))
                
                print(f"✅ پروفایل آپدیت شد: {new_name}")
                
            except Exception as e:
                print(f"⚠️ خطا در آپدیت پروفایل: {e}")
            
            # هر 4-6 دقیقه آپدیت کن
            await asyncio.sleep(random.randint(240, 360))
    
    async def keep_alive(self):
        """زنده نگه داشتن بات"""
        print("🔋 شروع keep-alive...")
        while True:
            try:
                # یک کار ساده انجام بده تا ثابت کنی زنده‌ای
                await asyncio.sleep(300)
                print("🟢 بات هنوز فعال است...")
            except:
                pass
    
    async def setup_handlers(self):
        """تنظیم هندلرهای رویداد"""
        
        # هندلر پیام‌های خصوصی
        @self.client.on(events.NewMessage(incoming=True))
        async def message_handler(event):
            # لاگ پیام
            sender = await event.get_sender()
            print(f"📨 پیام از {sender.first_name}: {event.text[:30]}...")
            
            # اگر پیام از خودم بود کاری نکن
            if sender.id == (await self.client.get_me()).id:
                return
            
            # دستور تنظیم دشمن
            if event.text == 'تنظیم دشمن' and event.is_reply:
                await self.set_enemy(event)
                return
            
            # دستور خاموش دشمن
            if event.text == 'خاموش دشمن':
                await self.disable_enemy(event)
                return
            
            # دستور وضعیت
            if event.text == 'وضعیت':
                await self.show_status(event)
                return
            
            # دستور راهنما
            if event.text == 'راهنما':
                await self.show_help(event)
                return
            
            # اگر حالت دشمن فعال است
            if self.enemy_mode and self.enemy_id and sender.id == self.enemy_id:
                await self.reply_to_enemy(event)
                return
            
            # پاسخ خودکار به پیام خصوصی
            if event.is_private:
                await self.auto_reply(event)
    
    async def set_enemy(self, event):
        """تنظیم کاربر به عنوان دشمن"""
        try:
            reply_msg = await event.get_reply_message()
            target_user = await reply_msg.get_sender()
            
            self.enemy_id = target_user.id
            self.enemy_name = target_user.first_name or target_user.username or "کاربر"
            self.enemy_mode = True
            
            response = f"""
✅ **دشمن تنظیم شد!**

👤 **نام:** {self.enemy_name}
🆔 **ID:** {self.enemy_id}
🔥 **حالت:** فعال

از این پس به همه پیام‌های این کاربر پاسخ می‌دهم!
            """
            
            await event.reply(response)
            print(f"🎯 دشمن تنظیم شد: {self.enemy_name}")
            
        except Exception as e:
            print(f"⚠️ خطا در تنظیم دشمن: {e}")
            await event.reply("⚠️ خطا در تنظیم دشمن")
    
    async def disable_enemy(self, event):
        """غیرفعال کردن حالت دشمن"""
        self.enemy_mode = False
        self.enemy_id = None
        self.enemy_name = None
        
        await event.reply("✅ حالت دشمن غیرفعال شد")
        print("🟢 حالت دشمن غیرفعال شد")
    
    async def reply_to_enemy(self, event):
        """پاسخ به دشمن"""
        try:
            # انتخاب رندوم یک فحش
            bad_word = random.choice(self.bad_words)
            
            # اموجی‌های مختلف
            emojis = ["🔥", "💢", "⚡", "👊", "🤬", "😡", "💀"]
            emoji = random.choice(emojis)
            
            # ارسال پاسخ
            await event.reply(f"{emoji} **{bad_word}** {emoji}")
            
            print(f"🔥 پاسخ به دشمن: {bad_word}")
            
        except Exception as e:
            print(f"⚠️ خطا در پاسخ به دشمن: {e}")
    
    async def auto_reply(self, event):
        """پاسخ خودکار به پیام‌ها"""
        try:
            # تأخیر رندوم 2-8 ثانیه
            delay = random.uniform(2, 8)
            await asyncio.sleep(delay)
            
            # ارسال پاسخ
            await event.reply("🔺به دلیل مشغله کاری و قطعی مکرر اینترنت ممکنه کمی با تاخیر جواب بگیرید")
            
            print(f"🤖 پاسخ خودکار ارسال شد")
            
        except Exception as e:
            print(f"⚠️ خطا در پاسخ خودکار: {e}")
    
    async def show_status(self, event):
        """نمایش وضعیت بات"""
        try:
            status_text = f"""
📊 **وضعیت سلف بات:**

🕒 **تایم ایران:** فعال
📞 **پاسخ خودکار:** فعال
🔥 **حالت دشمن:** {'✅ فعال' if self.enemy_mode else '⭕ غیرفعال'}
👤 **دشمن فعلی:** {self.enemy_name if self.enemy_mode else 'ندارد'}
📡 **وضعیت اتصال:** آنلاین
⏰ **زمان سرور:** {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
🌐 **هاست:** Railway (رایگان)
            """
            
            await event.reply(status_text)
            
        except Exception as e:
            print(f"⚠️ خطا در نمایش وضعیت: {e}")
    
    async def show_help(self, event):
        """نمایش راهنما"""
        help_text = """
📖 **راهنمای سلف بات:**

🎯 **دستورات:**
• `تنظیم دشمن` (با ریپلای) - تنظیم کاربر بعنوان دشمن
• `خاموش دشمن` - غیرفعال کردن حالت دشمن
• `وضعیت` - نمایش وضعیت بات
• `راهنما` - این صفحه

🔥 **ویژگی‌ها:**
• تایم زنده ایران روی پروفایل
• پاسخ خودکار به پیام‌های خصوصی
• حالت دشمن (فحش رکیک)
• آنلاین 24/7 روی سرور ابری

⚠️ **توجه:**
این بات روی Railway اجرا می‌شود و کاملاً رایگان است.
            """
        
        await event.reply(help_text)
    
    async def show_welcome(self):
        """نمایش پیام خوش‌آمد"""
        try:
            me = await self.client.get_me()
            welcome_msg = f"""
🎉 **سلف بات فارسی فعال شد!**

👤 **کاربر:** {me.first_name}
📱 **شماره:** {PHONE_NUMBER}
🕒 **تایم ایران:** فعال
🔥 **حالت دشمن:** آماده

✅ بات با موفقیت راه‌اندازی شد و آماده استفاده است.
            """
            
            print(welcome_msg)
            
        except Exception as e:
            print(f"⚠️ خطا در نمایش خوش‌آمد: {e}")

# تابع اصلی
async def main():
    bot = PersianSelfBot()
    await bot.start()

# اجرا
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 سلف بات فارسی - نسخه Railway")
    print("🔥 توسط شما ساخته شده")
    print("="*60 + "\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 سلف بات توسط کاربر متوقف شد.")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")
        print("تلاش مجدد در 10 ثانیه...")
        time.sleep(10)
        asyncio.run(main())
