[app]

# Название приложения
title = CNC Mobile Pro
package.name = cncmobilepro
package.domain = org.cnc

# Включаемые расширения файлов (обязательно укажите html и js для вашего интерфейса)
source.include_exts = py,png,jpg,kv,atlas,html,js

# Главный файл запуска Python
source.main_file = main.py

version = 1.0.0

# Точный и проверенный набор зависимостей для pywebview на Android
requirements = python3,kivy,pywebview,pyobjus,android

orientation = portrait

# Разрешения для работы с памятью (чтобы можно было открывать STL-файлы)
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
