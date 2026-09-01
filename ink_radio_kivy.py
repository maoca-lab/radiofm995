# ink_radio_kivy.py
# ==========================================
# 水墨電台 - 修復 EQ 樣式與錄音權限同步問題
# ==========================================
import os
import json
import time
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import platform

try:
    from main import PUBLIC_DOWNLOAD_PATH, request_android_permissions
except ImportError:
    PUBLIC_DOWNLOAD_PATH = os.path.expanduser('~/Downloads')
    def request_android_permissions(cb=None):
        if cb: cb(True)

FONT_PATH = 'NotoSansCJK-Regular.ttc'
if os.path.exists(FONT_PATH):
    LabelBase.register(name='Roboto', fn_regular=FONT_PATH)

# 主題顏色
COLOR_BG = (0.1, 0.1, 0.1, 1)          # 黑色暗色底
COLOR_CARD = (0.18, 0.18, 0.18, 1)     # 暗色卡片底色
COLOR_TEXT_GOLD = (1, 0.75, 0, 1)      # 暗金黃字體
COLOR_TEXT_RED = (0.9, 0.2, 0.2, 1)     # 紅色字體
COLOR_BORDER = (0.3, 0.3, 0.3, 1)      # 邊框

# 自訂 EQ 下拉選單項目的視覺樣式 (修復灰色底無顯示問題)
class EQSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.25, 0.25, 0.25, 1)
        self.color = COLOR_TEXT_GOLD
        self.font_size = '14sp'
        self.height = 40

class InkCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 8
        with self.canvas.before:
            Color(*COLOR_CARD)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(*COLOR_BORDER)
            self.line = Line(rect=(self.x, self.y, self.width, self.height), width=1)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.line.rect = (instance.x, instance.y, instance.width, instance.height)

class InkRadioUI(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = False
        self.is_playing = False
        self.is_recording = False
        self.record_start_time = 0
        self.record_event = None

        self.stations = [
            {"name": "綠邨電台直播", "url": "http://stream.example.com/live"}
        ]

        self.main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=12,
            spacing=12
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        self.add_widget(self.main_layout)

        self._build_player_section()
        self._build_eq_section()
        self._build_recorder_section()

    def _build_player_section(self):
        card = InkCard(size_hint_y=None, height=180)
        
        # 狀態標題
        self.lbl_status = Label(
            text="🟡 已暫停",
            font_size='16sp',
            color=COLOR_TEXT_GOLD,
            size_hint_y=None,
            height=30,
            halign='left'
        )
        self.lbl_status.bind(size=self.lbl_status.setter('text_size'))
        card.add_widget(self.lbl_status)

        # 電台名稱
        self.lbl_current_station = Label(
            text="目前：綠邨電台直播",
            font_size='14sp',
            color=COLOR_TEXT_RED,
            size_hint_y=None,
            height=25,
            halign='left'
        )
        self.lbl_current_station.bind(size=self.lbl_current_station.setter('text_size'))
        card.add_widget(self.lbl_current_station)

        # 典藏輸入列
        input_box = BoxLayout(size_hint_y=None, height=35, spacing=5)
        self.input_name = TextInput(hint_text="電台名稱", multiline=False, size_hint_x=0.35)
        self.input_url = TextInput(hint_text="串流網址 .m3u8 / .mp3", multiline=False, size_hint_x=0.45)
        btn_add = Button(text="典藏", size_hint_x=0.2, background_color=(0.3, 0.3, 0.3, 1), color=COLOR_TEXT_GOLD)
        btn_add.bind(on_press=self.add_station)
        input_box.add_widget(self.input_name)
        input_box.add_widget(self.input_url)
        input_box.add_widget(btn_add)
        card.add_widget(input_box)

        # 電台列表
        self.station_list_box = BoxLayout(orientation='vertical', size_hint_y=None, height=40)
        card.add_widget(self.station_list_box)
        self.main_layout.add_widget(card)
        self.refresh_station_list()

    def _build_eq_section(self):
        """均衡器 (EQ) 區塊修復"""
        card = InkCard(size_hint_y=None, height=100)
        card.add_widget(Label(
            text="均衡器 (EQ)",
            font_size='15sp',
            color=COLOR_TEXT_GOLD,
            size_hint_y=None,
            height=25,
            halign='left'
        ))

        # 建立具備高對比視覺樣式的 EQ Spinner 下拉選單
        self.spn_eq = Spinner(
            text='標準 (Flat)',
            values=('標準 (Flat)', '人聲增強 (Vocal)', '重低音 (Bass Boost)', '古典水墨 (Classic)'),
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=(0.2, 0.2, 0.2, 1),
            color=COLOR_TEXT_GOLD,
            option_cls=EQSpinnerOption  # 指定客製化的選項類別
        )
        card.add_widget(self.spn_eq)
        self.main_layout.add_widget(card)

    def _build_recorder_section(self):
        """錄音 (麥克風) 區塊"""
        card = InkCard(size_hint_y=None, height=130)
        card.add_widget(Label(
            text="錄音 (麥克風)",
            font_size='15sp',
            color=COLOR_TEXT_GOLD,
            size_hint_y=None,
            height=25,
            halign='left'
        ))

        rec_box = BoxLayout(size_hint_y=None, height=45, spacing=15)
        self.btn_record = Button(
            text="開始錄音",
            background_color=(0.3, 0.3, 0.3, 1),
            color=COLOR_TEXT_GOLD,
            size_hint_x=0.7
        )
        self.btn_record.bind(on_press=self.on_record_btn_click)

        self.lbl_record_timer = Label(
            text="00:00",
            font_size='16sp',
            color=COLOR_TEXT_RED,
            size_hint_x=0.3
        )
        rec_box.add_widget(self.btn_record)
        rec_box.add_widget(self.lbl_record_timer)
        card.add_widget(rec_box)

        self.main_layout.add_widget(card)

    def on_record_btn_click(self, instance):
        """點擊錄音按鈕時，自動先檢查/申請權限再切換狀態"""
        if not self.is_recording:
            # 發起權限申請，傳入授權後的回呼函式
            def on_permission_result(granted):
                if granted:
                    # 授權成功，立即切換為錄音狀態
                    self.start_recording()
                else:
                    self.lbl_record_timer.text = "無權限"

            request_android_permissions(on_permission_result)
        else:
            # 已在錄音中，直接停止
            self.stop_recording()

    def start_recording(self):
        """啟動錄音與更新 UI"""
        self.is_recording = True
        self.btn_record.text = "停止錄音"
        self.btn_record.color = COLOR_TEXT_RED
        self.record_start_time = time.time()
        self.record_event = Clock.schedule_interval(self._update_record_timer, 1)

    def stop_recording(self):
        """停止錄音並儲存"""
        self.is_recording = False
        self.btn_record.text = "開始錄音"
        self.btn_record.color = COLOR_TEXT_GOLD
        if self.record_event:
            self.record_event.cancel()

        filename = f"錄音_{time.strftime('%m%d_%H%M')}.mp3"
        save_path = os.path.join(PUBLIC_DOWNLOAD_PATH, filename)
        self.lbl_record_timer.text = "已存檔"
        print(f"[Record] 錄音檔案已成功儲存至: {save_path}")

    def _update_record_timer(self, dt):
        elapsed = int(time.time() - self.record_start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        self.lbl_record_timer.text = f"{mins:02d}:{secs:02d}"

    def add_station(self, instance):
        name = self.input_name.text.strip()
        url = self.input_url.text.strip()
        if name and url:
            self.stations.append({"name": name, "url": url})
            self.input_name.text = ""
            self.input_url.text = ""
            self.refresh_station_list()

    def refresh_station_list(self):
        self.station_list_box.clear_widgets()
        for idx, item in enumerate(self.stations):
            row = BoxLayout(size_hint_y=None, height=35, spacing=5)
            row.add_widget(Label(text=item['name'], color=COLOR_TEXT_GOLD, size_hint_x=0.7))
            btn_play = Button(text="播放", size_hint_x=0.3, background_color=(0.3, 0.3, 0.3, 1), color=COLOR_TEXT_GOLD)
            row.add_widget(btn_play)
            self.station_list_box.add_widget(row)

class InkRadioApp(App):
    def build(self):
        self.title = "水墨電台"
        return InkRadioUI()

    def on_start(self):
        # App 啟動時自動主動發起權限申請
        request_android_permissions()

if __name__ == '__main__':
    InkRadioApp().run()

