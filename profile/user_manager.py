import json
import os


class UserManager:
    
    def __init__(self):
        self.users_file = "data/users.json"
        self.current_user = None
        self._load_users()
    
    def _load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def _save_users(self):
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def register(self, username, email, password):
        if username in self.users:
            return False, "Потребителят вече съществува"
        
        if len(password) < 6:
            return False, "Паролата трябва да е поне 6 символа"
        
        self.users[username] = {
            "email": email,
            "password": password,
            "favorites": [],
            "visited": []
        }
        self._save_users()
        return True, "Успешна регистрация"
    
    def login(self, username, password):
        if username not in self.users:
            return False, "Потребителят не съществува"
        
        if self.users[username]["password"] != password:
            return False, "Грешна парола"
        
        self.current_user = username
        return True, "Успешен вход"
    
    def logout(self):
        self.current_user = None
    
    def is_logged_in(self):
        return self.current_user is not None
    
    #Current user data
    def get_current_user(self):
        if self.current_user:
            return {
                "username": self.current_user,
                "email": self.users[self.current_user]["email"],
                "favorites": self.users[self.current_user].get("favorites", []),
                "visited": self.users[self.current_user].get("visited", [])
            }
        return None
    
    #Favorites management
    def add_favorite(self, place_name):
        if self.current_user:
            if place_name not in self.users[self.current_user]["favorites"]:
                self.users[self.current_user]["favorites"].append(place_name)
                self._save_users()
                return True
        return False
    
    #Remove from favorites
    def remove_favorite(self, place_name):
        if self.current_user:
            if place_name in self.users[self.current_user]["favorites"]:
                self.users[self.current_user]["favorites"].remove(place_name)
                self._save_users()
                return True
        return False


# Singleton instance
user_manager = UserManager()