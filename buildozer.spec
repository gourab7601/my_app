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
android.permissions = INTERNET, CAMERA, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, BATTERY_STATS, FOREGROUND_SERVICE, WAKE_LOCK
icon.filename = icon.png
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.accept_sdk_license = True
android.archs = arm64-v8a
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1