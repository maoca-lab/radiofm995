# adapters.py
# ==========================================
# 六角架構 - Adapters (適配器層)
# 作用：包含 Desktop 模擬與 Android 原生 jnius 實作
# ==========================================
import sys
import os
from ports import IAudioPlayerPort, IAudioRecorderPort, IEqualizerPort, IPermissionPort

# ------------------------------------------
# 1. 桌面版安全模擬適配器 (Desktop / PC / CI)
# ------------------------------------------
class DesktopPlayerAdapter(IAudioPlayerPort):
    def play(self, url: str) -> None:
        print(f"[Desktop Player] 開始播放串流: {url}")

    def stop(self) -> None:
        print("[Desktop Player] 停止播放")

    def set_volume(self, volume: float) -> None:
        print(f"[Desktop Player] 音量設定為: {volume}")


class DesktopRecorderAdapter(IAudioRecorderPort):
    def start_recording(self, output_path: str) -> bool:
        print(f"[Desktop Recorder] 開始錄音並儲存至: {output_path}")
        return True

    def stop_recording(self) -> str:
        print("[Desktop Recorder] 停止錄音")
        return "/tmp/desktop_sample.wav"


class DesktopEqualizerAdapter(IEqualizerPort):
    def __init__(self):
        self._bands = [
            {'band': 0, 'freq': 60, 'gain': 0},
            {'band': 1, 'freq': 230, 'gain': 0},
            {'band': 2, 'freq': 910, 'gain': 0},
            {'band': 3, 'freq': 3600, 'gain': 0},
            {'band': 4, 'freq': 14000, 'gain': 0},
        ]

    def get_bands(self):
        return self._bands

    def set_band_level(self, band: int, level: int) -> None:
        if 0 <= band < len(self._bands):
            self._bands[band]['gain'] = level
            print(f"[Desktop EQ] Band {band} 調整為 {level} dB")


class DesktopPermissionAdapter(IPermissionPort):
    def request_audio_permission(self, callback) -> None:
        print("[Desktop Permission] 桌面環境預設權限通過")
        if callback:
            callback(True)


# ------------------------------------------
# 2. Android 原生適配器 (帶 Exception 隔離保護)
# ------------------------------------------
class AndroidEqualizerAdapter(IEqualizerPort):
    """安全封裝 Android Equalizer 原生 API"""
    def __init__(self, audio_session_id: int = 0):
        self._eq = None
        try:
            from jnius import autoclass
            Equalizer = autoclass('android.media.audiofx.Equalizer')
            self._eq = Equalizer(0, audio_session_id)
            self._eq.setEnabled(True)
        except Exception as e:
            print(f"[Android EQ Warning] 原生等化器初始化失敗，切換安全模式: {e}")

    def get_bands(self):
        if not self._eq:
            return DesktopEqualizerAdapter().get_bands()
        try:
            num_bands = self._eq.getNumberOfBands()
            bands = []
            for i in range(num_bands):
                freq = self._eq.getCenterFreq(i) // 1000
                level = self._eq.getBandLevel(i)
                bands.append({'band': i, 'freq': freq, 'gain': level})
            return bands
        except Exception:
            return DesktopEqualizerAdapter().get_bands()

    def set_band_level(self, band: int, level: int) -> None:
        if self._eq:
            try:
                self._eq.setBandLevel(band, level)
            except Exception as e:
                print(f"[Android EQ Error] 設定頻段失敗: {e}")

