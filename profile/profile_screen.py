import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from profile.user_manager import user_manager


class ProfileScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='profile',
            text='Профил',
            icon='account',
            **kwargs
        )
        self.dialog = None
        self.build_ui()
        self.bind(on_enter=lambda x: self.refresh_ui())
    
    def build_ui(self):
        self.main_layout = MDBoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        self.add_widget(self.main_layout)
        self.refresh_ui()
    
    def refresh_ui(self):
        self.main_layout.clear_widgets()
        
        if user_manager.is_logged_in():
            self.show_logged_in_ui()
        else:
            self.show_guest_ui()
    
    #guest UI 
    def show_guest_ui(self):
        title = MDLabel(
            text="Добре дошли!",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height="60dp"
        )
        self.main_layout.add_widget(title)
        
        subtitle = MDLabel(
            text="Влезте в профила си за достъп до любими места и още",
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="40dp"
        )
        self.main_layout.add_widget(subtitle)
        
        # Spacer
        self.main_layout.add_widget(MDLabel(size_hint_y=0.3))
        
        # Login button
        login_btn = MDRaisedButton(
            text="Вход в профил",
            size_hint=(0.8, None),
            height="50dp",
            pos_hint={'center_x': 0.5},
            md_bg_color=(0.2, 0.4, 0.8, 1),
            on_release=lambda x: self.show_login_dialog()
        )
        self.main_layout.add_widget(login_btn)
        
        # REgistration button
        register_btn = MDFlatButton(
            text="Регистрация",
            size_hint=(0.8, None),
            height="50dp",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.show_register_dialog()
        )
        self.main_layout.add_widget(register_btn)
        
        # Spacer
        self.main_layout.add_widget(MDLabel(size_hint_y=0.5))
    
    def show_logged_in_ui(self):
        user = user_manager.get_current_user()
        
        # Profile card
        profile_card = MDCard(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.9, None),
            height="150dp",
            pos_hint={'center_x': 0.5},
            elevation=2
        )
        
        name_label = MDLabel(
            text=f"👤 {user['username']}",
            font_style="H5",
            bold=True
        )
        profile_card.add_widget(name_label)
        
        email_label = MDLabel(
            text=user['email'],
            theme_text_color="Secondary"
        )
        profile_card.add_widget(email_label)
        
        self.main_layout.add_widget(profile_card)
        
        # Statistics card
        stats_card = MDCard(
            orientation='vertical',
            padding=20,
            spacing=10,
            size_hint=(0.9, None),
            height="120dp",
            pos_hint={'center_x': 0.5},
            elevation=2
        )
        
        stats_title = MDLabel(
            text="Статистики",
            font_style="H6",
            bold=True
        )
        stats_card.add_widget(stats_title)
        
        favorites_count = len(user['favorites'])
        visited_count = len(user['visited'])
        
        stats_label = MDLabel(
            text=f"❤️ Любими места: {favorites_count}\n📍 Посетени: {visited_count}"
        )
        stats_card.add_widget(stats_label)
        
        self.main_layout.add_widget(stats_card)
        
        # Spacer
        self.main_layout.add_widget(MDLabel(size_hint_y=0.5))
        
        # Output button
        logout_btn = MDFlatButton(
            text="Изход от профил",
            size_hint=(0.8, None),
            height="50dp",
            pos_hint={'center_x': 0.5},
            on_release=lambda x: self.do_logout()
        )
        self.main_layout.add_widget(logout_btn)
    
    def show_login_dialog(self):
        # Layout 
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height="200dp",
            padding=10
        )
        
        self.login_username = MDTextField(
            hint_text="Потребителско име",
            mode="rectangle"
        )
        content.add_widget(self.login_username)
        
        self.login_password = MDTextField(
            hint_text="Парола",
            mode="rectangle",
            password=True
        )
        content.add_widget(self.login_password)
        
        self.dialog = MDDialog(
            title="Вход в профил",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ОТКАЗ",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="ВХОД",
                    on_release=lambda x: self.do_login()
                )
            ]
        )
        self.dialog.open()
    
    def show_register_dialog(self):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None,
            height="280dp",
            padding=10
        )
        
        self.reg_username = MDTextField(
            hint_text="Потребителско име",
            mode="rectangle"
        )
        content.add_widget(self.reg_username)
        
        self.reg_email = MDTextField(
            hint_text="Email",
            mode="rectangle"
        )
        content.add_widget(self.reg_email)
        
        self.reg_password = MDTextField(
            hint_text="Парола (поне 6 символа)",
            mode="rectangle",
            password=True
        )
        content.add_widget(self.reg_password)
        
        self.reg_confirm = MDTextField(
            hint_text="Потвърди парола",
            mode="rectangle",
            password=True
        )
        content.add_widget(self.reg_confirm)
        
        self.dialog = MDDialog(
            title="Регистрация",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="ОТКАЗ",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="РЕГИСТРАЦИЯ",
                    on_release=lambda x: self.do_register()
                )
            ]
        )
        self.dialog.open()
    
    def do_login(self):
        username = self.login_username.text.strip()
        password = self.login_password.text
        
        if not username or not password:
            self.show_message("Грешка", "Моля попълнете всички полета")
            return
        
        success, message = user_manager.login(username, password)
        
        if success:
            self.dialog.dismiss()
            self.show_message("Успех", message)
            self.refresh_ui()
        else:
            self.show_message("Грешка", message)
    
    def do_register(self):
        username = self.reg_username.text.strip()
        email = self.reg_email.text.strip()
        password = self.reg_password.text
        confirm = self.reg_confirm.text
        
        if not username or not email or not password:
            self.show_message("Грешка", "Моля попълнете всички полета")
            return
        
        if password != confirm:
            self.show_message("Грешка", "Паролите не съвпадат")
            return
        
        success, message = user_manager.register(username, email, password)
        
        if success:
            self.dialog.dismiss()
            self.show_message("Успех", f"{message}\nМоже да влезете в профила си")
        else:
            self.show_message("Грешка", message)
    
    def do_logout(self):
        user_manager.logout()
        self.refresh_ui()
        self.show_message("Изход", "Излязохте от профила си")
    
    def show_message(self, title, text):
        msg_dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: msg_dialog.dismiss()
                )
            ]
        )
        msg_dialog.open()