# ports.py
# ==========================================
# 六角架構 - Ports (埠) 定義
# ==========================================
from abc import ABC, abstractmethod

class IPermissionPort(ABC):
    @abstractmethod
    def request_audio_permission(self, callback):
        pass

class IStoragePort(ABC):
    @abstractmethod
    def get_save_directory(self) -> str:
        pass
