
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel


class FavoritesScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='favorites',
            text='Любими',
            icon='heart',
            **kwargs
        )
        self.build_ui()
    
    def build_ui(self):
        label = MDLabel(
            text="Любими места\n\nДобавете места в любими",
            halign="center",
            font_style="H6"
        )
        self.add_widget(label)