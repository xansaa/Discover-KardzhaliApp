from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivy.uix.spinner import Spinner
from data.places_data import get_all_places, get_places_by_category, CATEGORIES


class PlacesScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='places',
            text='Места',
            icon='map-marker',
            **kwargs
        )
        self.all_places = get_all_places()
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        
        #Search field
        self.search_field = MDTextField(
            hint_text="Търсене на място...",
            mode='rectangle',
            size_hint=(1, None),
            height='40dp',
            icon_right='magnify'
        )
        layout.add_widget(self.search_field)
        
        # Dropdown menu
        self.category_spinner = Spinner(
            text='Категория: Всички',
            values=CATEGORIES,
            size_hint=(1, None),
            height='44dp',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.category_spinner.bind(text=self.on_category_select)
        layout.add_widget(self.category_spinner)
        
        # Places List
        scroll = MDScrollView()
        self.places_list = MDList()
        scroll.add_widget(self.places_list)
        layout.add_widget(scroll)
        
        # Initial load of all places
        self.update_places_list(self.all_places)
        
        self.add_widget(layout)
    
    # Helper methods
    def update_places_list(self, places):
        self.places_list.clear_widgets()
        for place in places:
            self.places_list.add_widget(OneLineListItem(text=place["name"]))
    
    # Filtering
    def filter_places(self, category):
        filtered = get_places_by_category(category)
        self.update_places_list(filtered)
    
    # Event handlers
    def on_category_select(self, spinner, text):
        if ":" in text:
            category = text.split(": ")[1]
        else:
            category = text
        
        self.filter_places(category)
        spinner.text = f"Категория: {category}"