# viewmodel.py
# ==========================================
# MVVM - ViewModel 狀態管理
# ==========================================
import os
import time
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from ports import IPermissionPort, IStoragePort

class RadioViewModel(EventDispatcher):
    record_btn_text = StringProperty("開始錄音")
    record_timer_text = StringProperty("00:00")
    is_recording = BooleanProperty(False)
    status_info = StringProperty("系統就緒")

    def __init__(self, perm_port: IPermissionPort, storage_port: IStoragePort, **kwargs):
        super().__init__(**kwargs)
        self.perm_port = perm_port
        self.storage_port = storage_port
        self._start_time = 0
        self._timer_event = None

    def on_record_button_click(self):
        if not self.is_recording:
            self.perm_port.request_audio_permission(self._on_permission_result)
        else:
            self.stop_recording()

    def _on_permission_result(self, granted: bool):
        if granted:
            self.start_recording()
        else:
            self.status_info = "錄音權限被拒絕"
            self.record_timer_text = "無權限"

    def start_recording(self):
        self.is_recording = True
        self.record_btn_text = "停止錄音"
        self.status_info = "錄音中..."
        self._start_time = time.time()
        self._timer_event = Clock.schedule_interval(self._update_timer, 1)

    def stop_recording(self):
        self.is_recording = False
        self.record_btn_text = "開始錄音"
        if self._timer_event:
            self._timer_event.cancel()
        
        save_dir = self.storage_port.get_save_directory()
        filename = f"錄音_{time.strftime('%m%d_%H%M%S')}.mp3"
        save_path = os.path.join(save_dir, filename)
        
        self.record_timer_text = "已存檔"
        self.status_info = f"檔案已儲存至 Download 資料夾"
        print(f"[ViewModel] 儲存路徑: {save_path}")

    def _update_timer(self, dt):
        elapsed = int(time.time() - self._start_time)
        mins, secs = divmod(elapsed, 60)
        self.record_timer_text = f"{mins:02d}:{secs:02d}"
