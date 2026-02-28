[app]
title = Gourab
package.name = gourab
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,android,pyjnius,plyer,requests,certifi,urllib3,idna,charset-normalizer
orientation = portrait
fullscreen = 1

# এই পারমিশনগুলো আপডেট করা হয়েছে
android.permissions = INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, VIBRATE, FOREGROUND_SERVICE, WAKE_LOCK, POST_NOTIFICATIONS, FLASHLIGHT, ACCESS_FINE_LOCATION

icon.filename = icon.png
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.bootstrap = sdl2

# --- এই লাইনটি অবশ্যই যোগ করবি ---
services = myservice:service.py

[buildozer]
log_level = 2
warn_on_root = 1
