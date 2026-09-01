# main.py
# ==========================================
# 應用程式入口點 (依賴注入與平台邊界組裝)
# ==========================================
import sys
from kivy.app import App
from kivy.utils import platform

from viewmodel import RadioViewModel
from adapters import (
    DesktopPlayerAdapter,
    DesktopRecorderAdapter,
    DesktopEqualizerAdapter,
    DesktopPermissionAdapter,
    AndroidEqualizerAdapter
)
from ui_view import InkRadioView

class InkRadioApp(App):
    def build(self):
        # 根據第一性原理：判斷執行平台並注入適當的邊界適配器
        if platform == 'android':
            print("[System] 檢測到 Android 平台，組裝 Android 原生適配器邊界...")
            player = DesktopPlayerAdapter()
            recorder = DesktopRecorderAdapter()
            equalizer = AndroidEqualizerAdapter()  # 注入帶 Exception 隔離保護的原生 EQ
            permission = DesktopPermissionAdapter()
        else:
            print("[System] 檢測到 Desktop 平台，組裝桌面模擬適配器邊界...")
            player = DesktopPlayerAdapter()
            recorder = DesktopRecorderAdapter()
            equalizer = DesktopEqualizerAdapter()
            permission = DesktopPermissionAdapter()

        # 將邊界適配器注入至純粹狀態 ViewModel
        vm = RadioViewModel(
            player=player,
            recorder=recorder,
            equalizer=equalizer,
            permission=permission
        )

        # 傳遞 ViewModel 並建構 UI
        return InkRadioView(viewmodel=vm)

if __name__ == '__main__':
    InkRadioApp().run()

