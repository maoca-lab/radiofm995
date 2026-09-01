# viewmodel.py
# ==========================================
# 輕量 MVVM - ViewModel (純粹狀態管理)
# 作用：完全解耦 UI 與平台硬體，僅透過 Ports 溝通
# ==========================================
from ports import IAudioPlayerPort, IAudioRecorderPort, IEqualizerPort, IPermissionPort

class RadioViewModel:
    def __init__(
        self,
        player: IAudioPlayerPort,
        recorder: IAudioRecorderPort,
        equalizer: IEqualizerPort,
        permission: IPermissionPort
    ):
        self._player = player
        self._recorder = recorder
        self._equalizer = equalizer
        self._permission = permission

        # 應用程式純粹狀態 (States)
        self.current_station = "水墨清音台 (FM 99.5)"
        self.stream_url = "http://stream.example.com/live"
        self.is_playing = False
        self.is_recording = False
        self.status_info = "系統就緒"
        self.auto_play_on_boot = False

    def toggle_play(self):
        """控制播放 / 暫停狀態"""
        if self.is_playing:
            self._player.stop()
            self.is_playing = False
            self.status_info = "已停止播放"
        else:
            self._player.play(self.stream_url)
            self.is_playing = True
            self.status_info = f"正在播放: {self.current_station}"

    def toggle_record(self):
        """安全錄音流程（含權限檢查）"""
        if self.is_recording:
            saved_file = self._recorder.stop_recording()
            self.is_recording = False
            self.status_info = f"錄音儲存至: {saved_file}"
        else:
            def on_permission_result(granted: bool):
                if granted:
                    success = self._recorder.start_recording("/sdcard/Download/ink_radio.wav")
                    if success:
                        self.is_recording = True
                        self.status_info = "錄音中..."
                    else:
                        self.status_info = "錄音啟動失敗"
                else:
                    self.status_info = "缺乏麥克風權限"

            self._permission.request_audio_permission(on_permission_result)

    def adjust_eq(self, band: int, level: int):
        """調整 EQ 狀態"""
        self._equalizer.set_band_level(band, level)
        self.status_info = f"EQ 頻段 {band} 調整為 {level}"

