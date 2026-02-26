import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.places_data import get_all_places
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy.uix.label import Label
from data.places_data import get_all_places


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
            zoom=11,
            lat=41.6473,
            lon=25.3678
        )
        
        self.add_markers()
        
        self.add_widget(self.mapview)
    
    def add_markers(self):
        places = get_all_places()
        
        for place in places:
            marker = MapMarkerPopup(
                lat=place["lat"],
                lon=place["lon"]
            ) 

            popup_label = Label(
                text=f"{place['name']}\n{place['category']}",
                size_hint=(None, None),
                size=(200, 60),
                halign='center',
                valign='middle'
            )
            popup_label.bind(size=popup_label.setter('text_size'))
            
            marker.add_widget(popup_label)
            self.mapview.add_marker(marker)
    
    def reset_map(self):
        self.mapview.center_on(41.6473, 25.3678)
        self.mapview.zoom = 11