# ui_view.py
# ==========================================
# View 層：視覺佈局與數據綁定
# ==========================================
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from viewmodel import RadioViewModel

FONT_PATH = 'NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    LabelBase.register(name='Roboto', fn_regular=FONT_PATH)

class RadioMainView(BoxLayout):
    def __init__(self, viewModel: RadioViewModel, **kwargs):
        super().__init__(**kwargs)
        self.vm = viewModel
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.lbl_status = Label(text=self.vm.status_info, size_hint_y=None, height=30, color=(1, 0.75, 0, 1))
        self.add_widget(self.lbl_status)

        self.lbl_timer = Label(text=self.vm.record_timer_text, font_size='24sp', size_hint_y=None, height=50, color=(0.9, 0.2, 0.2, 1))
        self.add_widget(self.lbl_timer)

        self.btn_record = Button(text=self.vm.record_btn_text, size_hint_y=None, height=50)
        self.btn_record.bind(on_press=lambda instance: self.vm.on_record_button_click())
        self.add_widget(self.btn_record)

        # ViewModel -> View 數據綁定
        self.vm.bind(status_info=self._update_status)
        self.vm.bind(record_timer_text=self._update_timer)
        self.vm.bind(record_btn_text=self._update_btn_text)

    def _update_status(self, instance, value):
        self.lbl_status.text = value

    def _update_timer(self, instance, value):
        self.lbl_timer.text = value

    def _update_btn_text(self, instance, value):
        self.btn_record.text = value
