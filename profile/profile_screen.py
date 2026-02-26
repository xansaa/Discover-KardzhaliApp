import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel


class ProfileScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='profile',
            text='Профил',
            icon='account',
            **kwargs
        )
        self.build_ui()
    
    def build_ui(self):
        label = MDLabel(
            text="Моят профил\n\nНастройки и информация",
            halign="center",
            font_style="H6"
        )
        self.add_widget(label)