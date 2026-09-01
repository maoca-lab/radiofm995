# tests/test_domain.py
# ==========================================
# 雲端純邏輯單元測試 (解決 Pytest Exit Code 5 錯誤)
# ==========================================
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
    """測試 ViewModel 初始狀態 (確保 Pytest 成功收集測試)"""
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
