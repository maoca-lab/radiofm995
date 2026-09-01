# tests/test_domain.py
# ==========================================
# 雲端純邏輯單元測試
# ==========================================
import pytest
from ports import IPermissionPort, IStoragePort
from viewmodel import RadioViewModel

class MockPermissionAdapter(IPermissionPort):
    def request_audio_permission(self, callback):
        if callback: callback(True)

class MockStorageAdapter(IStoragePort):
    def get_save_directory( -> str:
        return "/tmp/mock_download"

def test_viewmodel_initial_state():
    vm = RadioViewModel(MockPermissionAdapter(), MockStorageAdapter())
    assert vm.is_recording is False
    assert vm.record_btn_text == "開始錄音"

def test_recording_toggle():
    vm = RadioViewModel(MockPermissionAdapter(), MockStorageAdapter())
    vm.on_record_button_click()
    assert vm.is_recording is True
    assert vm.record_btn_text == "停止錄音"
