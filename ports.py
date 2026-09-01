# ports.py
# ==========================================
# 六角架構 - Ports (埠介面層)
# 作用：定義系統輸入/輸出合約，徹底隔離 Android 平台邊界
# ==========================================
from abc import ABC, abstractmethod
from typing import Callable, List, Dict, Any

class IAudioPlayerPort(ABC):
    """網路電台串流播放器介面"""
    @abstractmethod
    def play(self, url: str) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def set_volume(self, volume: float) -> None:
        pass


class IAudioRecorderPort(ABC):
    """麥克風/廣播錄音介面"""
    @abstractmethod
    def start_recording(self, output_path: str) -> bool:
        pass

    @abstractmethod
    def stop_recording(self) -> str:
        pass


class IEqualizerPort(ABC):
    """音訊等化器介面"""
    @abstractmethod
    def get_bands(self) -> List[Dict[str, int]]:
        pass

    @abstractmethod
    def set_band_level(self, band: int, level: int) -> None:
        pass


class IPermissionPort(ABC):
    """系統權限請求介面"""
    @abstractmethod
    def request_audio_permission(self, callback: Callable[[bool], None]) -> None:
        pass


class IStoragePort(ABC):
    """本機資料與偏好設定儲存介面"""
    @abstractmethod
    def save(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def load(self, key: str, default: Any = None) -> Any:
        pass

