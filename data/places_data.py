PLACES = [
    {"name": "Пещера Утробата", "category": "Природа"},
    {"name": "Язовир Кърджали", "category": "Язовири"},
    {"name": "Перперикон", "category": "Исторически"},
    {"name": "Храм Св. Успение Богородично", "category": "Храмове"},
    {"name": "Пещера Венеца", "category": "Природа"},
    {"name": "Язовир Студен кладенец", "category": "Язовири"},
    {"name": "Крепост Моняк", "category": "Исторически"},
    {"name": "Св. Йоан Предтеча", "category": "Храмове"},
    {"name": "Дяволското гърло", "category": "Природа"},
    {"name": "Язовир Ивайловград", "category": "Язовири"},
    {"name": "Крепост Калето", "category": "Исторически"},
    {"name": "Свети Георги Победоносец", "category": "Храмове"},
    {"name": "Каменната сватба", "category": "Природа"},
    {"name": "Каменните гъби", "category": "Природа"},
    {"name": "Скални ниши край село Ненково", "category": "Природа"},
    {"name": "Резерват Валчия дол", "category": "Природа"},
    {"name": "Защитена местност Перперишки скални гъби", "category": "Природа"},
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