import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivy.uix.spinner import Spinner
from data.places_data import get_all_places, get_places_by_category, CATEGORIES
from profile.user_manager import user_manager


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
        self.bind(on_enter=lambda x: self.refresh_list())
    
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
        
        # Dropdown for category filter
        self.category_spinner = Spinner(
            text='Категория: Всички',
            values=CATEGORIES,
            size_hint=(1, None),
            height='44dp',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.category_spinner.bind(text=self.on_category_select)
        layout.add_widget(self.category_spinner)
        
        #List of places
        scroll = MDScrollView()
        self.places_list = MDList()
        scroll.add_widget(self.places_list)
        layout.add_widget(scroll)
        
        self.update_places_list(self.all_places)
        
        self.add_widget(layout)
    
    def refresh_list(self):
        #Save current category filter
        current_category = self.category_spinner.text.split(": ")[1] if ":" in self.category_spinner.text else "Всички"
        filtered = get_places_by_category(current_category)
        self.update_places_list(filtered)
    
    def update_places_list(self, places):
        self.places_list.clear_widgets()
        
        for place in places:
            #Validate if place is in user's favorites
            is_favorite = False
            if user_manager.is_logged_in():
                user = user_manager.get_current_user()
                is_favorite = place["name"] in user.get("favorites", [])
            
            item = TwoLineAvatarIconListItem(
                text=place["name"],
                secondary_text=place["category"]
            )
            
            #Heart icon for favorites
            heart_icon = MDIconButton(
                icon="heart" if is_favorite else "heart-outline",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1) if is_favorite else (0.5, 0.5, 0.5, 1),
                on_release=lambda x, p=place: self.toggle_favorite(p)
            )
            item.add_widget(heart_icon)
            
            self.places_list.add_widget(item)
    
    def toggle_favorite(self, place):
        """Добавя/премахва място от любими"""
        if not user_manager.is_logged_in():
            print("Трябва да влезете в профила си")
            return
        
        user = user_manager.get_current_user()
        
        if place["name"] in user.get("favorites", []):
            #Remove from favorites
            user_manager.remove_favorite(place["name"])
        else:
            #Add to favorites
            user_manager.add_favorite(place["name"])
        
        # Refresh list
        self.refresh_list()
    
    def filter_places(self, category):
        filtered = get_places_by_category(category)
        self.update_places_list(filtered)
    
    def on_category_select(self, spinner, text):
        if ":" in text:
            category = text.split(": ")[1]
        else:
            category = text
        
        self.filter_places(category)
        spinner.text = f"Категория: {category}"