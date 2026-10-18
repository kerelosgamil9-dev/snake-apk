[app]
title = Snake Game
package.name = snakegame
package.domain = org.snake
source.dir = .
source.include_exts = py,png,jpg,ttf,wav,json
version = 1.0
requirements = python3,kivy==2.3.0,arabic-reshaper,plyer,pyjnius
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png
android.permissions = VIBRATE
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
