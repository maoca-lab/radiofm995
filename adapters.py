# adapters.py
# ==========================================
# 六角架構 - Adapters (適配器)
# 封裝 Android 原生 API 與 @mainthread 安全執行緒
# ==========================================
import os
from ports import IPermissionPort, IStoragePort
from kivy.utils import platform
from kivy.clock import mainthread

class AndroidPermissionAdapter(IPermissionPort):
    def request_audio_permission(self, callback):
        if platform == 'android':
            try:
                from android.permissions import request_permissions, Permission, check_permission
                
                @mainthread
                def _safe_callback(perms, grants):
                    has_perm = check_permission(Permission.RECORD_AUDIO)
                    if callback: callback(has_perm)

                request_permissions([Permission.RECORD_AUDIO], _safe_callback)
            except Exception as e:
                print(f"[Android Adapter Error] {e}")
                if callback: callback(True)
        else:
            if callback: callback(True)

class AndroidStorageAdapter(IStoragePort):
    def get_save_directory( -> str:
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                base_path = primary_external_storage_path()
                path = os.path.join(base_path, 'Download') if base_path else '/sdcard/Download'
            except Exception:
                path = '/sdcard/Download'
        else:
            path = os.path.expanduser('~/Downloads')
        
        os.makedirs(path, exist_ok=True)
        return path
