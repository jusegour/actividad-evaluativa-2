from utils.database_connection import JsonDatabase

class BaseRepository:
    def __init__(self, db_file, collection_name):
        self.db = JsonDatabase(db_file)
        self.collection_name = collection_name

    def get_all(self):
        return self.db.get_data(self.collection_name)

    def _save_all(self, items):
        self.db.save_data(self.collection_name, items)

    def _generate_id(self, items):
        if not items:
            return 1
        # Busca el ID máximo actual y suma 1. Mucho más seguro que len()
        return max(item['id'] for item in items) + 1

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__('db.json', 'products')

    def get_by_id(self, product_id):
        products = self.get_all()
        return next((p for p in products if p['id'] == product_id), None)
    
    def add(self, product_data):
        products = self.get_all()
        new_product = product_data.copy()
        new_product['id'] = self._generate_id(products)
        
        products.append(new_product)
        self._save_all(products)
        return new_product

class CategoryRepository(BaseRepository):
    def __init__(self):
        super().__init__('db.json', 'categories')

    def get_by_name(self, name):
        categories = self.get_all()
        return next((c for c in categories if c['name'] == name), None)

    def add(self, category_data):
        categories = self.get_all()
        new_category = category_data.copy()
        new_category['id'] = self._generate_id(categories)
        
        categories.append(new_category)
        self._save_all(categories)
        return new_category

    def delete(self, name):
        categories = self.get_all()
        # Filtramos la lista excluyendo la categoría a borrar
        updated_categories = [c for c in categories if c['name'] != name]
        self._save_all(updated_categories)

class FavoriteRepository(BaseRepository):
    def __init__(self):
        super().__init__('db.json', 'favorites')

    def add(self, favorite_data):
        favorites = self.get_all()
        favorites.append(favorite_data)
        self._save_all(favorites)

    def delete(self, user_id, product_id):
        favorites = self.get_all()
        updated = [
            f for f in favorites 
            if not (f['user_id'] == user_id and f['product_id'] == product_id)
        ]
        self._save_all(updated)


class InventoryRepository(BaseRepository):
    def __init__(self):
        super().__init__('db.json', 'inventory')
        
    def get_stock(self, product_id: int) -> int:
        #Obtiene el nivel de stock para un ID de producto específico.
        inventory = self.get_all()
        item = next((i for i in inventory if i['product_id'] == product_id), None)
        return item.get('stock', 0) if item else 0

    # Método para futura expansion (restar stock)
    def update_stock(self, product_id: int, quantity: int):
        inventory = self.get_all()
        # Lógica para encontrar y actualizar el stock
        pass