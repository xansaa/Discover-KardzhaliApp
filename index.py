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
from kivy.uix.spinner import Spinner



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
        
        # Dropdown menu 
        self.category_spinner = Spinner(
            text='Категория: Всички',
            values=('Всички', 'Природа', 'Язовири', 'Исторически', 'Храмове'),
            size_hint=(1, None),
            height='44dp',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.category_spinner.bind(text=self.on_category_select)
        tab1_layout.add_widget(self.category_spinner)

        
        #Tab 1 - Places List
        scroll = MDScrollView()
        self.places_list = MDList()

        #All places
        self.all_places = [
            {"name" : "Пещера Утробата", "category": "Природа"},
            {"name" : "Язовир Кърджали", "category": "Язовири"},
            {"name" : "Перперикон", "category": "Исторически"},
            {"name" : "Храм Св. Успение Богородично", "category": "Храмове"},
            {"name" : "Пещера Венеца", "category": "Природа"},
            {"name" : "Язовир Студен кладенец", "category": "Язовири"},
            {"name" : "Крепост Моняк", "category": "Исторически"},
            {"name" : "Св. Йоан Предтеча", "category": "Храмове"},
            {"name" : "Дяволското гърло", "category": "Природа"},
            {"name" : "Язовир Ивайловград", "category": "Язовири"},
            {"name" : "Крепост Калето", "category": "Исторически"},
            {"name" : "Свети Георги Победоносец", "category": "Храмове"},
            {"name" : "Каменната сватба", "category": "Природа"},
            {"name" : "Каменните гъби", "category": "Природа"},
            {"name" : "Скални ниши край село Ненково", "category": "Природа"},
            {"name" : "Резерват Валчия дол", "category": "Природа"},
            {"name" : "Защитена местност Перперишки скални гъби", "category": "Природа"},
        ]

        self.update_places_list(self.all_places)
        scroll.add_widget(self.places_list)
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
    
    #UPDATE PLACES LIST
    def update_places_list(self, places):
        self.places_list.clear_widgets()
        for place in places:
            self.places_list.add_widget(OneLineListItem(text=place["name"]))
    
    #UPDATE FILTER PLACES
    def filter_places(self, category):
        if category == "Всички":
            filtered = self.all_places
        else:
            filtered = [p for p in self.all_places if p["category"] == category]
        
        self.update_places_list(filtered)

    def on_category_select(self, spinner, text):
        if ":" in text:
            category = text.split(": ")[1]
        else:
            category = text
    
        self.filter_places(category)
        spinner.text = f"Категория: {category}"

if __name__ == '__main__':
    DiscoverKardzhaliApp().run()