# main.py
# ==========================================
# 水墨電台 - 入口與組裝
# ==========================================
from kivy.app import App
from adapters import AndroidPermissionAdapter, AndroidStorageAdapter
from viewmodel import RadioViewModel
from ui_view import RadioMainView

class InkRadioApp(App):
    def build(self):
        self.title = "水墨電台"
        perm_adapter = AndroidPermissionAdapter()
        storage_adapter = AndroidStorageAdapter()
        vm = RadioViewModel(perm_adapter, storage_adapter)
        return RadioMainView(viewModel=vm)

if __name__ == '__main__':
    InkRadioApp().run()

