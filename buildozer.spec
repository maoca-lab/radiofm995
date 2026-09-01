[app]

# (str) 應用程式標題
title = 水墨電台

# (str) 套件名稱 (僅限小寫英文字母與數字)
package.name = inkradio

# (str) 套件網域 (反向網域名稱)
package.domain = org.inkradio

# (str) 專案原始碼所在目錄
source.dir = .

# (list) 包含在 APK 中的檔案副檔名
source.include_exts = py,png,jpg,kv,atlas,ttc,ttf,json

# (str) 應用程式版本號
version = 1.0.0

# (list) 應用程式依賴套件 (已鎖定 Cython==0.29.33 防編譯崩潰)
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,android,Cython==0.29.33

# (str) 螢幕方向 (portrait: 直向, landscape: 橫向)
orientation = portrait

# (bool) 是否全螢幕顯示
fullscreen = 0

# (list) Android 系統權限
android.permissions = INTERNET, ACCESS_NETWORK_STATE, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target Android API (預設 33 相容主流系統)
android.api = 33

# (int) Minimum Android API (預設 21 支援 Android 5.0+)
android.minapi = 21

# (2) 強制指定使用穩定的 NDK r25b (防止自動下載破壞性的 NDK r28c)
android.ndk = 25b

# (bool) 自動接受 Android SDK 授權條款
android.accept_sdk_license = True

# (list) 支援的 CPU 架構
android.archs = arm64-v8a, armeabi-v7a

# (bool) 啟用 Android 介面升級
p4a.branch = master


[buildozer]

# (int) 日誌輸出級別 (2 表示詳細除錯模式)
log_level = 2

# (str) 警告提示過濾
warn_on_root = 1

