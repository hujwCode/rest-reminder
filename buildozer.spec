[app]

# (str) Title of your application
title = 休息提醒

# (str) Package name
package.name = restreminder

# (str) Package domain (needed for android/ios packaging)
package.domain = org.myapp

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy,plyer

# (str) Preset of buildozer options
preset = android

# (str) Orientation
orientation = portrait

# (list) Permissions
android.permissions = VIBRATE,WAKE_LOCK

# (int) Target Android API
android.api = 33

# (int) Minimum Android API
android.minapi = 21

# (str) NDK version
android.ndk = 25b

# (list) Android architectures
android.archs = arm64-v8a,armeabi-v7a

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
