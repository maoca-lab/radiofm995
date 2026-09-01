# ui_view.py
# ==========================================
# 輕量 MVVM - View (Kivy UI 視圖層)
# 作用：僅綁定 ViewModel 狀態，完全解耦 Android 硬體
# ==========================================
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from viewmodel import RadioViewModel

class InkRadioView(BoxLayout):
    def __init__(self, viewmodel: RadioViewModel, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.vm = viewmodel

        # 1. 狀態顯示標籤
        self.status_label = Label(
            text=self.vm.status_info,
            font_size='18sp',
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.status_label)

        # 2. 播放 / 暫停按鈕
        self.play_btn = Button(
            text="播放 / 暫停",
            size_hint_y=None,
            height=50
        )
        self.play_btn.bind(on_release=self.on_play_click)
        self.add_widget(self.play_btn)

        # 3. 錄音控制按鈕
        self.record_btn = Button(
            text="開始錄音",
            size_hint_y=None,
            height=50
        )
        self.record_btn.bind(on_release=self.on_record_click)
        self.add_widget(self.record_btn)

        # 4. EQ 頻段調整標籤與滑桿
        self.eq_label = Label(
            text="音訊等化器 (60Hz 頻段)",
            size_hint_y=None,
            height=30
        )
        self.add_widget(self.eq_label)

        self.eq_slider = Slider(
            min=-10,
            max=10,
            value=0,
            size_hint_y=None,
            height=40
        )
        self.eq_slider.bind(value=self.on_eq_change)
        self.add_widget(self.eq_slider)

    def on_play_click(self, instance):
        """觸發播放狀態切換"""
        self.vm.toggle_play()
        self.update_ui()

    def on_record_click(self, instance):
        """觸發錄音流程"""
        self.vm.toggle_record()
        self.update_ui()

    def on_eq_change(self, instance, value):
        """觸發 EQ 調整"""
        self.vm.adjust_eq(0, int(value))
        self.update_ui()

    def update_ui(self):
        """根據 ViewModel 的最新狀態刷新介面"""
        self.status_label.text = self.vm.status_info
        self.record_btn.text = "停止錄音" if self.vm.is_recording else "開始錄音"

