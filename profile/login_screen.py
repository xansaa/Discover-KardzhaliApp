import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from profile.user_manager import user_manager


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(name='login', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=20
        )
        
        title = MDLabel(
            text="Вход в профил",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(title)
        
        # Spacer
        layout.add_widget(MDLabel(size_hint_y=0.2))
        
        # Username 
        self.username_field = MDTextField(
            hint_text="Потребителско име",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.username_field)
        
        # Password 
        self.password_field = MDTextField(
            hint_text="Парола",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.password_field)
        
        # Spacer
        layout.add_widget(MDLabel(size_hint_y=0.2))
        
        # Login button
        login_btn = MDRaisedButton(
            text="Вход",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.do_login
        )
        layout.add_widget(login_btn)
        
        # Register buton
        register_btn = MDFlatButton(
            text="Нямате акаунт? Регистрирайте се",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_register
        )
        layout.add_widget(register_btn)
        
       #Back button
        back_btn = MDFlatButton(
            text="Назад",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def do_login(self, instance):
        username = self.username_field.text.strip()
        password = self.password_field.text
        
        if not username or not password:
            self.show_dialog("Грешка", "Моля попълнете всички полета")
            return
        
        success, message = user_manager.login(username, password)
        
        if success:
            self.show_dialog("Успех", message, on_dismiss=self.go_to_profile)
        else:
            self.show_dialog("Грешка", message)
    
    def go_to_register(self, instance):
        self.manager.current = 'register'
    
    def go_to_profile(self, *args):   
        self.manager.current = 'profile_main'
    
    def go_back(self, instance):
        self.manager.current = 'profile_main'
    
    def show_dialog(self, title, text, on_dismiss=None):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: (dialog.dismiss(), on_dismiss() if on_dismiss else None)
                )
            ]
        )
        dialog.open()