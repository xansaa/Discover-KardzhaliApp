from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView

class DiscoverKardzhaliApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        
        screen = MDScreen()
        
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top toolbar
        toolbar = MDTopAppBar(
            title="D I S C O V E R  •  K A R D Z H A L I",
            md_bg_color=(0.1, 0.3, 0.6, 1),
            elevation = 4
        )
        main_layout.add_widget(toolbar)
        
        # Bottom Navigation
        bottom_nav = MDBottomNavigation()
        
        # Tab 1 - Места (със списък)
        tab1 = MDBottomNavigationItem(
            name='places',
            text='Места',
            icon='map-marker'
        )
        
        # Създаване на списък с места
        scroll = MDScrollView()
        places_list = MDList()
        
        # Примерни данни за места
        places = [
            "Перперикон",
            "Каменна сватба",
            "Юмрук скала",
            "Църква Св. Георги",
            "Централна джамия",
            "Обсерватория Славей Златев",
            "Крепост Устра",
            "Язовир Кърджали",
            "Екопътека Шампион",
            "Историческия музей"
        ]
        
        for place in places:
            places_list.add_widget(
                OneLineListItem(text=place)
            )
        
        scroll.add_widget(places_list)
        tab1.add_widget(scroll)
        
        # Tab 2 - Любими
        tab2 = MDBottomNavigationItem(
            name='favorites',
            text='Любими',
            icon='heart'
        )
        tab2.add_widget(MDLabel(
            text="Любими места\n\nДобавете места в любими",
            halign="center",
            font_style="H6"
        ))
        
        # Tab 3 - Карта
        tab3 = MDBottomNavigationItem(
            name='map',
            text='Карта',
            icon='map'
        )
        tab3.add_widget(MDLabel(
            text="GPS Карта\n\n(Ще добавим скоро)",
            halign="center",
            font_style="H6"
        ))
        
        # Tab 4 - Профил
        tab4 = MDBottomNavigationItem(
            name='profile',
            text='Профил',
            icon='account'
        )
        tab4.add_widget(MDLabel(
            text="Моят профил\n\nНастройки и информация",
            halign="center",
            font_style="H6"
        ))
        
        bottom_nav.add_widget(tab1)
        bottom_nav.add_widget(tab2)
        bottom_nav.add_widget(tab3)
        bottom_nav.add_widget(tab4)
        
        main_layout.add_widget(bottom_nav)
        screen.add_widget(main_layout)
        
        return screen

if __name__ == '__main__':
    DiscoverKardzhaliApp().run()