[app]
title = CNC Mobile Pro
package.name = cncmobilepro
package.domain = org.cnc
source.include_exts = py,png,jpg,kv,atlas,html,js,css
source.main_entry = main.py
version = 1.0
requirements = python3,pywebview,pyjnius,android,requests
orientation = portrait
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1