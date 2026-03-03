import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kivy.metrics import dp

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDIconButton

from profile.user_manager import user_manager
from data.places_data import get_all_places

# ── Color palette ──────────────────────────────────────────────────────────
PRIMARY = (0.08, 0.18, 0.50, 1)
BG      = (0.95, 0.95, 0.97, 1)
CARD    = (1.00, 1.00, 1.00, 1)
RED     = (0.88, 0.18, 0.18, 1)

# ── Category meta ──────────────────────────────────────────────────────────
CATEGORY_ICONS = {
    "Природа":     "pine-tree",
    "Язовири":     "waves",
    "Исторически": "pillar",
    "Храмове":     "church",
}

CATEGORY_COLORS = {
    "Природа":     (0.18, 0.62, 0.28, 1),
    "Язовири":     (0.12, 0.48, 0.88, 1),
    "Исторически": (0.72, 0.48, 0.14, 1),
    "Храмове":     (0.58, 0.22, 0.68, 1),
}


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
        self.root_layout = MDBoxLayout(
            orientation='vertical',
            md_bg_color=BG
        )
        self.add_widget(self.root_layout)
        self.refresh_favorites()

    # ── Refresh ────────────────────────────────────────────────────────────
    def refresh_favorites(self):
        self.root_layout.clear_widgets()
        if not user_manager.is_logged_in():
            self._show_not_logged_in()
        else:
            self._show_favorites()

    # ── Empty states ───────────────────────────────────────────────────────
    def _show_not_logged_in(self):
        container = MDBoxLayout(
            orientation='vertical',
            padding=[dp(40), dp(0), dp(40), dp(0)],
            spacing=dp(14)
        )
        container.add_widget(MDLabel(size_hint_y=0.28))

        container.add_widget(MDLabel(
            text="",
            halign="center",
            font_style="H2",
            size_hint_y=None,
            height=dp(72)
        ))

        container.add_widget(MDLabel(
            text="Любими места",
            halign="center",
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(44)
        ))

        container.add_widget(MDLabel(
            text="Влезте в профила си,\nза да запазвате любими места",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(56)
        ))

        container.add_widget(MDLabel(size_hint_y=0.72))
        self.root_layout.add_widget(container)

    def _show_empty_favorites(self):
        container = MDBoxLayout(
            orientation='vertical',
            padding=[dp(40), dp(0), dp(40), dp(0)],
            spacing=dp(14)
        )
        container.add_widget(MDLabel(size_hint_y=0.28))

        container.add_widget(MDLabel(
            text="",
            halign="center",
            font_style="H2",
            size_hint_y=None,
            height=dp(72)
        ))

        container.add_widget(MDLabel(
            text="Нямате любими места",
            halign="center",
            font_style="H5",
            bold=True,
            size_hint_y=None,
            height=dp(44)
        ))

        container.add_widget(MDLabel(
            text="Добавете места от раздел 'Места'\nчрез натискане на иконата ",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body1",
            size_hint_y=None,
            height=dp(56)
        ))

        container.add_widget(MDLabel(size_hint_y=0.72))
        self.root_layout.add_widget(container)

    # ── Filled favorites ───────────────────────────────────────────────────
    def _show_favorites(self):
        user = user_manager.get_current_user()
        favorite_names = user.get("favorites", [])

        if not favorite_names:
            self._show_empty_favorites()
            return

        # Header bar
        header = MDCard(
            orientation='horizontal',
            size_hint=(1, None),
            height=dp(54),
            radius=[0, 0, 0, 0],
            elevation=2,
            padding=[dp(18), dp(0), dp(16), dp(0)],
            md_bg_color=CARD
        )
        header.add_widget(MDLabel(
            text=f"Любими места",
            font_style="H6",
            bold=True
        ))
        header.add_widget(MDCard(
            size_hint=(None, None),
            size=(dp(32), dp(26)),
            radius=[dp(13), dp(13), dp(13), dp(13)],
            elevation=0,
            md_bg_color=(*RED[:3], 0.12),
            padding=[dp(6), dp(0), dp(6), dp(0)]
        ))
        count_badge = MDLabel(
            text=str(len(favorite_names)),
            font_style="Caption",
            bold=True,
            theme_text_color="Custom",
            text_color=RED,
            halign="center",
            size_hint=(None, None),
            size=(dp(32), dp(26))
        )
        header.add_widget(count_badge)
        self.root_layout.add_widget(header)

        # Scrollable list
        scroll = MDScrollView()
        list_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            padding=[dp(12), dp(12), dp(12), dp(16)],
            size_hint_y=None
        )
        list_layout.bind(minimum_height=list_layout.setter('height'))

        all_places = get_all_places()
        for place_name in favorite_names:
            place = next((p for p in all_places if p["name"] == place_name), None)
            if place:
                list_layout.add_widget(self._create_favorite_card(place))

        scroll.add_widget(list_layout)
        self.root_layout.add_widget(scroll)

    # ── Card factory ───────────────────────────────────────────────────────
    def _create_favorite_card(self, place):
        cat   = place["category"]
        color = CATEGORY_COLORS.get(cat, (0.44, 0.44, 0.44, 1))
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
        badge.add_widget(MDIconButton(
            icon=icon,
            theme_text_color="Custom",
            text_color=color,
            size_hint=(1, 1)
        ))
        card.add_widget(badge)

        # Text column
        text_col = MDBoxLayout(orientation='vertical', spacing=dp(2))
        text_col.add_widget(MDLabel(
            text=place["name"],
            font_style="Subtitle1",
            bold=True,
            size_hint_y=None,
            height=dp(28),
            shorten=True,
            shorten_from='right'
        ))
        text_col.add_widget(MDLabel(
            text=cat,
            font_style="Caption",
            theme_text_color="Secondary",
            size_hint_y=None,
            height=dp(18)
        ))
        card.add_widget(text_col)

        # Remove button
        card.add_widget(MDIconButton(
            icon="heart-broken",
            theme_text_color="Custom",
            text_color=RED,
            size_hint=(None, None),
            size=(dp(46), dp(46)),
            on_release=lambda x, p=place: self.remove_favorite(p)
        ))

        return card

    # ── Actions ────────────────────────────────────────────────────────────
    def remove_favorite(self, place):
        user_manager.remove_favorite(place["name"])
        self.refresh_favorites()
