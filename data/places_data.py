PLACES = [
    {"name": "Пещера Утробата", "category": "Природа", "lat": 41.9889, "lon": 25.4639},
    {"name": "Язовир Кърджали", "category": "Язовири", "lat": 41.6344, "lon": 25.3539},
    {"name": "Перперикон", "category": "Исторически", "lat": 41.9511, "lon": 25.4711},
    {"name": "Храм Св. Успение Богородично", "category": "Храмове", "lat": 41.6500, "lon": 25.3700},
    {"name": "Пещера Венеца", "category": "Природа", "lat": 41.5000, "lon": 25.5000},
    {"name": "Язовир Студен кладенец", "category": "Язовири", "lat": 41.5800, "lon": 25.4200},
    {"name": "Крепост Моняк", "category": "Исторически", "lat": 41.7300, "lon": 25.5100},
    {"name": "Св. Йоан Предтеча", "category": "Храмове", "lat": 41.6470, "lon": 25.3680},
    {"name": "Дяволското гърло", "category": "Природа", "lat": 41.5800, "lon": 24.9400},
    {"name": "Язовир Ивайловград", "category": "Язовири", "lat": 41.5300, "lon": 26.1200},
    {"name": "Крепост Калето", "category": "Исторически", "lat": 41.6400, "lon": 25.3600},
    {"name": "Свети Георги Победоносец", "category": "Храмове", "lat": 41.6473, "lon": 25.3678},
    {"name": "Каменната сватба", "category": "Природа", "lat": 41.4900, "lon": 25.3300},
    {"name": "Каменните гъби", "category": "Природа", "lat": 41.5200, "lon": 25.5800},
    {"name": "Скални ниши край село Ненково", "category": "Природа", "lat": 41.7100, "lon": 25.5200},
    {"name": "Резерват Валчия дол", "category": "Природа", "lat": 41.6100, "lon": 25.4500},
    {"name": "Защитена местност Перперишки скални гъби", "category": "Природа", "lat": 41.9600, "lon": 25.4800},
]

CATEGORIES = ["Всички", "Природа", "Язовири", "Исторически", "Храмове"]

#Get all places
def get_all_places():
    return PLACES

#Filter places by category
def get_places_by_category(category):
    if category == "Всички":
        return PLACES
    return [p for p in PLACES if p["category"] == category]

#Search places by name
def search_places(query):
    return [p for p in PLACES if query.lower() in p["name"].lower()]