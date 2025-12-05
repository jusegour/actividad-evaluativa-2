import json
import os

class JsonDatabase:
    def __init__(self, file_path):
        self.file_path = file_path

    def _load(self):
        if not os.path.exists(self.file_path):
            return {}
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def _save(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_data(self, key):
        #Obtiene la lista asociada a una clave (ej: 'products')
        data = self._load()
        return data.get(key, [])

    def save_data(self, key, new_list):
        #Guarda la lista actualizada bajo una clave específica
        full_data = self._load()
        full_data[key] = new_list
        self._save(full_data)