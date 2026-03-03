import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivy.metrics import dp

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField

from profile.user_manager import user_manager

# ── Color palette ──────────────────────────────────────────────────────────
PRIMARY      = (0.08, 0.18, 0.50, 1)
PRIMARY_DARK = (0.05, 0.12, 0.38, 1)
PRIMARY_BG   = (0.88, 0.91, 0.97, 1)   # soft blue tint for avatar area
BG           = (0.95, 0.95, 0.97, 1)
CARD         = (1.00, 1.00, 1.00, 1)
RED          = (0.88, 0.18, 0.18, 1)
TEXT_MUTED   = (0.78, 0.85, 0.98, 1)   # light text on dark header


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
            md_bg_color=BG
        )
        self.add_widget(self.main_layout)
        self.refresh_ui()

    def refresh_ui(self):
        self.main_layout.clear_widgets()
        if user_manager.is_logged_in():
            self._show_logged_in_ui()
        else:
            self._show_guest_ui()

    # ── Guest UI ───────────────────────────────────────────────────────────
    def _show_guest_ui(self):
        # Top white panel
        top = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(300),
            radius=[0, 0, 0, 0],
            elevation=2,
            padding=[dp(30), dp(36), dp(30), dp(24)],
            spacing=dp(12),
            md_bg_color=CARD
        )

        # Avatar placeholder
        avatar = MDCard(
            size_hint=(None, None),
            size=(dp(88), dp(88)),
            radius=[dp(44), dp(44), dp(44), dp(44)],
            elevation=0,
            md_bg_color=PRIMARY_BG,
            pos_hint={'center_x': 0.5}
        )
        avatar.add_widget(MDIconButton(
            icon='account-circle',
            theme_text_color='Custom',
            text_color=PRIMARY,
            size_hint=(1, 1)
        ))
        top.add_widget(avatar)

        top.add_widget(MDLabel(
            text="Добре дошли!",
            font_style="H5",
            halign="center",
            bold=True,
            size_hint_y=None,
            height=dp(42)
        ))
        top.add_widget(MDLabel(
            text="Влезте в профила си за достъп\nдо любими места и още",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2",
            size_hint_y=None,
            height=dp(48)
        ))
        self.main_layout.add_widget(top)

        # Buttons
        btn_area = MDBoxLayout(
            orientation='vertical',
            padding=[dp(28), dp(28), dp(28), dp(0)],
            spacing=dp(12),
            size_hint_y=None,
            height=dp(140)
        )
        btn_area.add_widget(MDRaisedButton(
            text="ВХОД В ПРОФИЛ",
            size_hint=(1, None),
            height=dp(50),
            md_bg_color=PRIMARY,
            on_release=lambda x: self.show_login_dialog()
        ))
        btn_area.add_widget(MDFlatButton(
            text="РЕГИСТРАЦИЯ",
            size_hint=(1, None),
            height=dp(50),
            theme_text_color="Custom",
            text_color=PRIMARY,
            on_release=lambda x: self.show_register_dialog()
        ))
        self.main_layout.add_widget(btn_area)
        self.main_layout.add_widget(MDLabel(size_hint_y=1))

    # ── Logged-in UI ───────────────────────────────────────────────────────
    def _show_logged_in_ui(self):
        user = user_manager.get_current_user()
        initials = user['username'][0].upper() if user['username'] else '?'

        # ── Blue header banner ─────────────────────────────────────────────
        header = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(210),
            radius=[0, 0, 0, 0],
            elevation=4,
            padding=[dp(20), dp(28), dp(20), dp(20)],
            spacing=dp(8),
            md_bg_color=PRIMARY
        )

        # Avatar circle with initial
        avatar = MDCard(
            size_hint=(None, None),
            size=(dp(78), dp(78)),
            radius=[dp(39), dp(39), dp(39), dp(39)],
            elevation=0,
            md_bg_color=(1, 1, 1, 0.20),
            pos_hint={'center_x': 0.5}
        )
        avatar.add_widget(MDLabel(
            text=initials,
            font_style="H4",
            halign="center",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True
        ))
        header.add_widget(avatar)

        header.add_widget(MDLabel(
            text=user['username'],
            font_style="H6",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(34)
        ))
        header.add_widget(MDLabel(
            text=user['email'],
            font_style="Body2",
            halign="center",
            theme_text_color="Custom",
            text_color=TEXT_MUTED,
            size_hint_y=None,
            height=dp(24)
        ))
        self.main_layout.add_widget(header)

        # ── Stats card ─────────────────────────────────────────────────────
        self.main_layout.add_widget(MDLabel(size_hint_y=None, height=dp(16)))

        stats = MDCard(
            orientation='horizontal',
            size_hint=(0.88, None),
            height=dp(96),
            pos_hint={'center_x': 0.5},
            elevation=2,
            radius=[dp(16), dp(16), dp(16), dp(16)],
            padding=[dp(16), dp(12), dp(16), dp(12)],
            md_bg_color=CARD
        )

        # Favorites stat
        fav_col = MDBoxLayout(orientation='vertical', spacing=dp(4))
        fav_col.add_widget(MDLabel(
            text=str(len(user['favorites'])),
            font_style="H4",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=RED
        ))
        fav_col.add_widget(MDLabel(
            text="Любими",
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        ))
        stats.add_widget(fav_col)

        # Divider
        stats.add_widget(MDCard(
            size_hint=(None, 0.65),
            width=dp(1),
            elevation=0,
            md_bg_color=(0.82, 0.82, 0.82, 1),
            pos_hint={'center_y': 0.5}
        ))

        # Visited stat
        vis_col = MDBoxLayout(orientation='vertical', spacing=dp(4))
        vis_col.add_widget(MDLabel(
            text=str(len(user['visited'])),
            font_style="H4",
            halign="center",
            bold=True,
            theme_text_color="Custom",
            text_color=PRIMARY
        ))
        vis_col.add_widget(MDLabel(
            text="Посетени",
            font_style="Caption",
            halign="center",
            theme_text_color="Secondary"
        ))
        stats.add_widget(vis_col)

        self.main_layout.add_widget(stats)
        self.main_layout.add_widget(MDLabel(size_hint_y=1))

        # Logout button
        self.main_layout.add_widget(MDFlatButton(
            text="ИЗХОД ОТ ПРОФИЛ",
            size_hint=(0.8, None),
            height=dp(46),
            pos_hint={'center_x': 0.5},
            theme_text_color="Custom",
            text_color=RED,
            on_release=lambda x: self.do_logout()
        ))
        self.main_layout.add_widget(MDLabel(size_hint_y=None, height=dp(18)))

    # ── Dialogs ────────────────────────────────────────────────────────────
    def show_login_dialog(self):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200),
            padding=dp(10)
        )
        self.login_username = MDTextField(
            hint_text="Потребителско име",
            mode="rectangle"
        )
        self.login_password = MDTextField(
            hint_text="Парола",
            mode="rectangle",
            password=True
        )
        content.add_widget(self.login_username)
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
                    md_bg_color=PRIMARY,
                    on_release=lambda x: self.do_login()
                )
            ]
        )
        self.dialog.open()

    def show_register_dialog(self):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(280),
            padding=dp(10)
        )
        self.reg_username = MDTextField(hint_text="Потребителско име", mode="rectangle")
        self.reg_email    = MDTextField(hint_text="Email",              mode="rectangle")
        self.reg_password = MDTextField(hint_text="Парола (поне 8 символа)", mode="rectangle", password=True)
        self.reg_confirm  = MDTextField(hint_text="Потвърди парола",   mode="rectangle", password=True)

        content.add_widget(self.reg_username)
        content.add_widget(self.reg_email)
        content.add_widget(self.reg_password)
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
                    md_bg_color=PRIMARY,
                    on_release=lambda x: self.do_register()
                )
            ]
        )
        self.dialog.open()

    # ── Auth logic (unchanged) ─────────────────────────────────────────────
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
        email    = self.reg_email.text.strip()
        password = self.reg_password.text
        confirm  = self.reg_confirm.text
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
        msg = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    md_bg_color=PRIMARY,
                    on_release=lambda x: msg.dismiss()
                )
            ]
        )
        msg.open()
