import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel

from data.places_data import get_all_places, get_places_by_category, search_places, CATEGORIES
from profile.user_manager import user_manager

# ── Color palette ──────────────────────────────────────────────────────────
PRIMARY      = (0.08, 0.18, 0.50, 1)   # deep navy blue
PRIMARY_DARK = (0.05, 0.12, 0.38, 1)
ACCENT       = (0.95, 0.55, 0.10, 1)   # warm orange
BG           = (0.95, 0.95, 0.97, 1)   # off-white background
CARD         = (1.00, 1.00, 1.00, 1)   # white cards
RED          = (0.88, 0.18, 0.18, 1)   # heart / favorites
GRAY         = (0.68, 0.68, 0.68, 1)   # inactive icons

# ── Category meta ──────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    "Природа":      "pine-tree",
    "Язовири":      "waves",
    "Исторически":  "pillar",
    "Храмове":      "church",
    "Всички":       "map-marker-multiple",
}

CATEGORY_COLORS = {
    "Природа":     (0.18, 0.62, 0.28, 1),
    "Язовири":     (0.12, 0.48, 0.88, 1),
    "Исторически": (0.72, 0.48, 0.14, 1),
    "Храмове":     (0.58, 0.22, 0.68, 1),
    "Всички":      (0.44, 0.44, 0.44, 1),
}


class PlacesScreen(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(
            name='places',
            text='Места',
            icon='map-marker',
            **kwargs
        )
        self.all_places = get_all_places()
        self.current_category = "Всички"
        self.category_buttons = {}
        self.build_ui()
        self.bind(on_enter=lambda x: self.refresh_list())

    # ── Build ──────────────────────────────────────────────────────────────
    def build_ui(self):
        root = MDBoxLayout(
            orientation='vertical',
            md_bg_color=BG
        )

        # ── Top controls panel ────────────────────────────────────────────
        controls = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(112),
            radius=[0, 0, 0, 0],
            elevation=3,
            padding=[dp(12), dp(8), dp(12), dp(6)],
            spacing=dp(6),
            md_bg_color=CARD
        )

        # Search field
        self.search_field = MDTextField(
            hint_text="Търсене на място...",
            mode='rectangle',
            size_hint=(1, None),
            height=dp(46),
            icon_right='magnify',
        )
        self.search_field.bind(text=self.on_search_text)
        controls.add_widget(self.search_field)

        # Category chips – horizontal scroll
        chip_scroll = ScrollView(
            size_hint=(1, None),
            height=dp(48),
            do_scroll_y=False,
            bar_width=0
        )
        chip_row = BoxLayout(
            orientation='horizontal',
            size_hint=(None, 1),
            width=dp(520),
            spacing=dp(8),
            padding=[dp(2), dp(4), dp(2), dp(4)]
        )

        for cat in ["Всички", "Природа", "Язовири", "Исторически", "Храмове"]:
            is_active = cat == self.current_category
            btn = MDRaisedButton(
                text=cat,
                size_hint=(None, None),
                height=dp(34),
                width=dp(max(len(cat) * 11 + 28, 80)),
                elevation=0 if not is_active else 1,
                md_bg_color=PRIMARY if is_active else (0.88, 0.88, 0.92, 1),
                text_color=(1, 1, 1, 1) if is_active else (0.35, 0.35, 0.35, 1),
                on_release=lambda x, c=cat: self.on_category_select(c)
            )
            self.category_buttons[cat] = btn
            chip_row.add_widget(btn)

        chip_scroll.add_widget(chip_row)
        controls.add_widget(chip_scroll)
        root.add_widget(controls)

        # ── Scrollable places list ─────────────────────────────────────────
        scroll = MDScrollView()
        self.places_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(12), dp(12), dp(12), dp(16)],
            size_hint_y=None
        )
        self.places_container.bind(
            minimum_height=self.places_container.setter('height')
        )
        scroll.add_widget(self.places_container)
        root.add_widget(scroll)

        self.update_places_list(self.all_places)
        self.add_widget(root)

    # ── Helpers ────────────────────────────────────────────────────────────
    def _create_place_card(self, place, is_favorite):
        cat   = place["category"]
        color = CATEGORY_COLORS.get(cat, GRAY)
        icon  = CATEGORY_ICONS.get(cat, "map-marker")

        card = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(72),
            padding=[dp(12), dp(10), dp(6), dp(10)],
            spacing=dp(12),
            elevation=1,
            radius=[dp(14), dp(14), dp(14), dp(14)],
            md_bg_color=CARD
        )

        # Coloured icon badge
        badge = MDCard(
            size_hint=(None, None),
            size=(dp(46), dp(46)),
            radius=[dp(23), dp(23), dp(23), dp(23)],
            elevation=0,
            md_bg_color=(*color[:3], 0.15)
        )
        badge_icon = MDIconButton(
            icon=icon,
            theme_text_color="Custom",
            text_color=color,
            size_hint=(1, 1)
        )
        badge.add_widget(badge_icon)
        card.add_widget(badge)

        # Text column
        text_col = MDBoxLayout(orientation='vertical', spacing=dp(2))
        name_lbl = MDLabel(
            text=place["name"],
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(28),
            shorten=True,
            shorten_from='right',
            theme_text_color="Primary"
        )
        cat_lbl = MDLabel(
            text=cat,
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(18)
        )
        text_col.add_widget(name_lbl)
        text_col.add_widget(cat_lbl)
        card.add_widget(text_col)

        # Heart button
        heart_btn = MDIconButton(
            icon="heart" if is_favorite else "heart-outline",
            theme_text_color="Custom",
            text_color=RED if is_favorite else GRAY,
            size_hint=(None, None),
            size=(dp(46), dp(46)),
            on_release=lambda x, p=place: self.toggle_favorite(p)
        )
        card.add_widget(heart_btn)

        return card

    # ── Data methods ───────────────────────────────────────────────────────
    def update_places_list(self, places):
        self.places_container.clear_widgets()
        if not places:
            lbl = MDLabel(
                text="Няма намерени места",
                halign="center",
                theme_text_color="Secondary",
                font_style="Body1",
                size_hint_y=None,
                height=dp(80)
            )
            self.places_container.add_widget(lbl)
            return

        for place in places:
            is_favorite = False
            if user_manager.is_logged_in():
                user = user_manager.get_current_user()
                is_favorite = place["name"] in user.get("favorites", [])
            self.places_container.add_widget(
                self._create_place_card(place, is_favorite)
            )

    def refresh_list(self):
        filtered = get_places_by_category(self.current_category)
        self.update_places_list(filtered)

    def on_search_text(self, field, text):
        if text.strip():
            results = search_places(text.strip())
        else:
            results = get_places_by_category(self.current_category)
        self.update_places_list(results)

    def on_category_select(self, category):
        self.current_category = category
        self.search_field.text = ""

        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.md_bg_color = PRIMARY
                btn.text_color = (1, 1, 1, 1)
            else:
                btn.md_bg_color = (0.88, 0.88, 0.92, 1)
                btn.text_color = (0.35, 0.35, 0.35, 1)

        self.update_places_list(get_places_by_category(category))

    def toggle_favorite(self, place):
        if not user_manager.is_logged_in():
            return
        user = user_manager.get_current_user()
        if place["name"] in user.get("favorites", []):
            user_manager.remove_favorite(place["name"])
        else:
            user_manager.add_favorite(place["name"])
        self.refresh_list()
