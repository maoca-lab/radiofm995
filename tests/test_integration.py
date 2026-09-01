# tests/test_integration.py
# ==========================================
# 六角架構 - 全系統整合測試
# 作用：驗證 main.py 依賴注入與 ui_view.py 畫面建構合約
# ==========================================
import os
import sys

# 動態註冊專案根目錄，防範 ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import InkRadioApp
from viewmodel import RadioViewModel
from ui_view import InkRadioView

def test_app_dependency_injection_and_build():
    """驗證 App 在無頭環境下能正確完成依賴注入並建立 View"""
    app = InkRadioApp()
    view = app.build()
    
    # 1. 驗證 UI 視圖是否成功建立
    assert isinstance(view, InkRadioView)
    
    # 2. 驗證 ViewModel 是否成功注入至 UI
    assert isinstance(view.vm, RadioViewModel)
    
    # 3. 驗證初始狀態符合預期
    assert view.vm.is_playing is False
    assert view.vm.is_recording is False
    assert view.status_label.text == "系統就緒"

def test_ui_button_interaction_flow():
    """驗證點擊 UI 按鈕時，狀態能正確流轉並同步更新介面文字"""
    app = InkRadioApp()
    view = app.build()
    
    # 模擬使用者點擊播放按鈕
    view.on_play_click(None)
    assert view.vm.is_playing is True
    assert "正在播放" in view.status_label.text
    
    # 模擬使用者點擊錄音按鈕
    view.on_record_click(None)
    assert view.vm.is_recording is True
    assert view.record_btn.text == "停止錄音"
