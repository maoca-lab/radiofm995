# tests/test_domain.py
# ==========================================
# 六角架構 - Domain / ViewModel 極速單元測試
# ==========================================
import os
import sys

# 註冊專案根目錄，防範模組匯入路徑問題
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from ports import IAudioPlayerPort, IAudioRecorderPort, IEqualizerPort, IPermissionPort, IStoragePort
from viewmodel import RadioViewModel
from adapters import (
    DesktopPlayerAdapter,
    DesktopRecorderAdapter,
    DesktopEqualizerAdapter,
    DesktopPermissionAdapter
)

def test_viewmodel_initial_state():
    """測試 ViewModel 初始狀態是否正確"""
    vm = RadioViewModel(
        player=DesktopPlayerAdapter(),
        recorder=DesktopRecorderAdapter(),
        equalizer=DesktopEqualizerAdapter(),
        permission=DesktopPermissionAdapter()
    )
    assert vm.is_playing is False
    assert vm.is_recording is False
    assert vm.status_info == "系統就緒"

def test_viewmodel_toggle_play_flow():
    """測試切換播放與暫停狀態邏輯"""
    vm = RadioViewModel(
        player=DesktopPlayerAdapter(),
        recorder=DesktopRecorderAdapter(),
        equalizer=DesktopEqualizerAdapter(),
        permission=DesktopPermissionAdapter()
    )
    # 觸發播放
    vm.toggle_play()
    assert vm.is_playing is True
    assert "正在播放" in vm.status_info

    # 觸發停止
    vm.toggle_play()
    assert vm.is_playing is False
    assert vm.status_info == "已停止播放"
