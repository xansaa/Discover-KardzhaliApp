import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton
from profile.user_manager import user_manager
from data.places_data import get_all_places


class FavoritesScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='favorites',
            text='Любими',
            icon='heart',
            **kwargs
        )
        self.build_ui()
        self.bind(on_enter=lambda x: self.refresh_favorites())
    
    def build_ui(self):
        self.main_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)
        self.refresh_favorites()
    
    def refresh_favorites(self):
        self.main_layout.clear_widgets()
        
        if not user_manager.is_logged_in():
            self.show_login_message()
        else:
            self.show_favorites()
    
    def show_login_message(self):
        label = MDLabel(
            text="❤️ Любими места\n\nВлезте в профила си за да запазвате любими места",
            halign="center",
            font_style="H6"
        )
        self.main_layout.add_widget(label)
    
    def show_favorites(self):
        user = user_manager.get_current_user()
        favorite_names = user.get("favorites", [])
        
        if not favorite_names:
            #Nothing in favorites
            label = MDLabel(
                text="❤️ Любими места\n\nОще нямате любими места\nДобавете места от раздел 'Места'",
                halign="center",
                font_style="H6"
            )
            self.main_layout.add_widget(label)
        else:
            #Name of the section with count
            title = MDLabel(
                text=f"❤️ Любими места ({len(favorite_names)})",
                font_style="H5",
                halign="center",
                size_hint_y=None,
                height="50dp"
            )
            self.main_layout.add_widget(title)
            
            #List of favorites
            scroll = MDScrollView()
            favorites_list = MDList()
            
            all_places = get_all_places()
            
            for place_name in favorite_names:
                #Find place by name
                place = next((p for p in all_places if p["name"] == place_name), None)
                
                if place:
                    item = TwoLineAvatarIconListItem(
                        text=place["name"],
                        secondary_text=place["category"]
                    )
                    
                    #Remove button
                    remove_btn = MDIconButton(
                        icon="delete",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1),
                        on_release=lambda x, p=place: self.remove_favorite(p)
                    )
                    item.add_widget(remove_btn)
                    
                    favorites_list.add_widget(item)
            
            scroll.add_widget(favorites_list)
            self.main_layout.add_widget(scroll)
    
    def remove_favorite(self, place):
        user_manager.remove_favorite(place["name"])
        self.refresh_favorites()