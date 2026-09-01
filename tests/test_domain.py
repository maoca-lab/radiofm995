# tests/test_domain.py
# ==========================================
# 六角架構 - 純邏輯 ViewModel 完整單元測試
# 作用：10 秒內極速驗證播放、錄音與 EQ 狀態流轉
# ==========================================
import os
import sys

# 註冊專案根目錄路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from viewmodel import RadioViewModel
from adapters import (
    DesktopPlayerAdapter,
    DesktopRecorderAdapter,
    DesktopEqualizerAdapter,
    DesktopPermissionAdapter
)

def test_viewmodel_initial_state():
    """測試 1: 驗證 ViewModel 初始狀態"""
    vm = RadioViewModel(
        player=DesktopPlayerAdapter(),
        recorder=DesktopRecorderAdapter(),
        equalizer=DesktopEqualizerAdapter(),
        permission=DesktopPermissionAdapter()
    )
    assert vm.is_playing is False
    assert vm.is_recording is False
    assert vm.status_info == "系統就緒"

def test_viewmodel_play_and_stop_flow():
    """測試 2: 驗證播放與停止控制邏輯"""
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

    # 觸發暫停
    vm.toggle_play()
    assert vm.is_playing is False
    assert vm.status_info == "已停止播放"

def test_viewmodel_record_and_eq_flow():
    """測試 3: 驗證錄音與 EQ 等化器調整邏輯"""
    vm = RadioViewModel(
        player=DesktopPlayerAdapter(),
        recorder=DesktopRecorderAdapter(),
        equalizer=DesktopEqualizerAdapter(),
        permission=DesktopPermissionAdapter()
    )
    # 觸發錄音
    vm.toggle_record()
    assert vm.is_recording is True
    assert vm.status_info == "錄音中..."

    # 調整 EQ
    vm.adjust_eq(band=0, level=5)
    assert "EQ 頻段 0 調整為 5" in vm.status_info
