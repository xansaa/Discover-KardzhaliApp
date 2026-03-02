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


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(name='register', **kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = MDBoxLayout(
            orientation='vertical',
            padding=40,
            spacing=15
        )
        
        title = MDLabel(
            text="Регистрация",
            font_style="H4",
            halign="center",
            size_hint_y=None,
            height="50dp"
        )
        layout.add_widget(title)
        
        # Spacer
        layout.add_widget(MDLabel(size_hint_y=0.1))
        
        # Username 
        self.username_field = MDTextField(
            hint_text="Потребителско име",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.username_field)
        
        # Email 
        self.email_field = MDTextField(
            hint_text="Email",
            mode="rectangle",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.email_field)
        
        # Password 
        self.password_field = MDTextField(
            hint_text="Парола (поне 6 символа)",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.password_field)
        
        # Confirm password 
        self.confirm_password_field = MDTextField(
            hint_text="Потвърди парола",
            mode="rectangle",
            password=True,
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(self.confirm_password_field)
        
        # Spacer
        layout.add_widget(MDLabel(size_hint_y=0.1))
        
        # Register button
        register_btn = MDRaisedButton(
            text="Регистрирай се",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.do_register
        )
        layout.add_widget(register_btn)
        
        # Login button
        login_btn = MDFlatButton(
            text="Имате акаунт? Влезте",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_login
        )
        layout.add_widget(login_btn)
        
        # Back button
        back_btn = MDFlatButton(
            text="Назад",
            size_hint_x=0.8,
            pos_hint={'center_x': 0.5},
            on_release=self.go_back
        )
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    #Logic for registration
    def do_register(self, instance):
        username = self.username_field.text.strip()
        email = self.email_field.text.strip()
        password = self.password_field.text
        confirm_password = self.confirm_password_field.text
        
        if not username or not email or not password:
            self.show_dialog("Грешка", "Моля попълнете всички полета")
            return
        
        if password != confirm_password:
            self.show_dialog("Грешка", "Паролите не съвпадат")
            return
        
        success, message = user_manager.register(username, email, password)
        
        if success:
            self.show_dialog("Успех", message, on_dismiss=self.go_to_login)
        else:
            self.show_dialog("Грешка", message)
    
    def go_to_login(self, instance=None):
        self.manager.current = 'login'
    
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