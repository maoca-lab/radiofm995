# tests/test_domain.py
# ==========================================
# 雲端純邏輯單元測試 (含動態根目錄路徑保護)
# ==========================================
import os
import sys

# 動態將專案根目錄加入 Python 模組搜尋路徑，避免 ModuleNotFoundError
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ports import IPermissionPort, IStoragePort
from viewmodel import RadioViewModel

class MockPermissionAdapter(IPermissionPort):
    def request_audio_permission(self, callback):
        # 模擬權限授權成功
        if callback:
            callback(True)

class MockStorageAdapter(IStoragePort):
    def get_save_directory(self) -> str:
        # 模擬測試用儲存路徑
        return "/tmp/mock_download"

def test_viewmodel_initialization():
    """測試 ViewModel 初始狀態"""
    vm = RadioViewModel(MockPermissionAdapter(), MockStorageAdapter())
    assert vm.is_recording is False
    assert vm.record_btn_text == "開始錄音"
    assert vm.status_info == "系統就緒"

def test_recording_toggle_state():
    """測試點擊錄音後的狀態切換邏輯"""
    vm = RadioViewModel(MockPermissionAdapter(), MockStorageAdapter())
    vm.on_record_button_click()
    assert vm.is_recording is True
    assert vm.record_btn_text == "停止錄音"
    assert vm.status_info == "錄音中..."
