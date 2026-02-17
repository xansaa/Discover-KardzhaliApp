from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton



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
        
        # Tab 1 - Places
        tab1 = MDBottomNavigationItem(
            name='places',
            text='Места',
            icon='map-marker'
        )

        tab1_layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)
        #Search place
        
        self.search_field = MDTextField(
            hint_text="Търсене на място...",
            mode='rectangle',
            size_hint=(1, None),
            height='40dp',
            icon_right='magnify',)

        tab1_layout.add_widget(self.search_field)
        

        #Button categories
        buttons_layout = MDBoxLayout(
            orientation='horizontal',
            spacing=5,
            padding=[10, 5, 10, 5],
            size_hint_y=None,
            height='40dp'
        )

        #All button
        btn_all = MDRaisedButton(
            text="Всички",
            on_release=lambda x: print("Всички места")
        )

        #Nature button
        btn_nature = MDRaisedButton(
            text="Природа",
            on_release=lambda x: print("Природни феномени")
        )

        #Dams button
        btn_dams = MDRaisedButton(
            text="Язовири",
            on_release=lambda x: print("Язовири")
        )
 
        #History button
        btn_history = MDRaisedButton(
            text="Исторически",
            on_release=lambda x: print("Исторически места")
        )

        #Temples button 
        btn_tamples = MDRaisedButton(
            text="Храмове",
            on_release=lambda x: print("Храмове")
        )

        buttons_layout.add_widget(btn_all)
        buttons_layout.add_widget(btn_nature)
        buttons_layout.add_widget(btn_dams)
        buttons_layout.add_widget(btn_history)
        buttons_layout.add_widget(btn_tamples)
        tab1_layout.add_widget(buttons_layout)
        
        # Създаване на списък с места
        scroll = MDScrollView()
        places_list = MDList()
        
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
        tab1_layout.add_widget(scroll)
        tab1.add_widget(tab1_layout)
        
        # Tab 2 - Favorites
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
        
        # Tab 3 - Maps
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
        
        # Tab 4 - Profile
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