from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy_garden.mapview import MapView


class MapScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='map',
            text='Карта',
            icon='map',
            **kwargs
        )
        self.build_ui()
        self.bind(on_enter=lambda x: self.reset_map())
    
    def build_ui(self):
        self.mapview = MapView(
            zoom=12,
            lat=41.65,
            lon=25.35
        )
        self.add_widget(self.mapview)
    
    def reset_map(self):
        self.mapview.center_on(41.65, 25.35)
        self.mapview.zoom = 11