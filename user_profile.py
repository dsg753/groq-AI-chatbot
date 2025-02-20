import os
import json

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.profile_dir = "user_profiles"
        self.profile_path = f"{self.profile_dir}/{user_id}.json"
        self.ensure_profile_dir_exists()
        self.profile = self.load_profile()

    def ensure_profile_dir_exists(self):
        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as file:
                return json.load(file)
        else:
            return {
                "favorite_topics": [],
                "preferred_language": "en",
                "search_history": [],
                "conversation_history": []
            }

    def save_profile(self):
        with open(self.profile_path, 'w') as file:
            json.dump(self.profile, file)

    def update_profile(self, key, value):
        self.profile[key] = value
        self.save_profile()

    def get_profile(self):
        return self.profile
