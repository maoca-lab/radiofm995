# main.py
# ==========================================
# 水墨電台 - 支援權限自動檢查與公共目錄存取
# ==========================================
import os
import sys
from kivy.utils import platform

def get_public_download_path():
    """取得手機公共 Download 資料夾絕對路徑"""
    if platform == 'android':
        try:
            from android.storage import primary_external_storage_path
            primary_path = primary_external_storage_path()
            download_dir = os.path.join(primary_path, 'Download')
        except Exception:
            download_dir = '/sdcard/Download'
    else:
        download_dir = os.path.expanduser('~/Downloads')

    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)
    return download_dir

PUBLIC_DOWNLOAD_PATH = get_public_download_path()

def request_android_permissions(on_complete_callback=None):
    """請求 Android 錄音與儲存空間權限 (支援完成後回呼)"""
    if platform == 'android':
        try:
            from android.permissions import request_permissions, Permission, check_permission
            
            permissions = [
                Permission.RECORD_AUDIO,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE
            ]
            
            def callback(permissions, grants):
                # 檢查錄音權限是否被授予
                if all(grants):
                    print("[System] 所有權限已成功授予！")
                    if on_complete_callback:
                        on_complete_callback(True)
                else:
                    print("[System] 使用者拒絕了部分權限。")
                    if on_complete_callback:
                        on_complete_callback(False)

            request_permissions(permissions, callback)
        except Exception as e:
            print(f"[Warning] 權限請求失敗: {e}")
            if on_complete_callback:
                on_complete_callback(True)
    else:
        # 非 Android 環境直接視為授權成功
        if on_complete_callback:
            on_complete_callback(True)

if __name__ == '__main__':
    from ink_radio_kivy import InkRadioApp
    InkRadioApp().run()

