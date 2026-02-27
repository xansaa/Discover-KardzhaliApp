from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.boxlayout import MDBoxLayout
from places.places_screen import PlacesScreen
from favorites.favorites_screen import FavoritesScreen
from map.map_screen import MapScreen
from profile.profile_screen import ProfileScreen


class DiscoverKardzhaliApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        screen = MDScreen()
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top toolbar
        toolbar = MDTopAppBar(
            title="D I S C O V E R  •  K A R D Z H A L I",
            md_bg_color=(0.1, 0.3, 0.6, 1),
            elevation=4
        )
        main_layout.add_widget(toolbar)
        
        # Bottom Navigation
        bottom_nav = MDBottomNavigation()
        bottom_nav.add_widget(PlacesScreen())
        bottom_nav.add_widget(FavoritesScreen())
        bottom_nav.add_widget(MapScreen())
        bottom_nav.add_widget(ProfileScreen())
        
        main_layout.add_widget(bottom_nav)
        screen.add_widget(main_layout)
        
        return screen


if __name__ == '__main__':
    DiscoverKardzhaliApp().run()