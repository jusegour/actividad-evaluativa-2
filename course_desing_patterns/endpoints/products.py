from flask import request
from flask_restful import Resource, reqparse
from utils.security import token_required
from repositories import ProductRepository,InventoryRepository

class ProductsResource(Resource):
    def __init__(self):
        # Inyección de dependencia "manual"
        self.repo = ProductRepository()
        self.inventory_repo = InventoryRepository()

    @token_required
    def get(self, product_id=None):
        
        products = self.repo.get_all()

        # Filtro por categoría
        category_filter = request.args.get('category')
        
        if category_filter:
            filtered = [p for p in products if p['category'].lower() == category_filter.lower()]
            return filtered, 200
        
        if product_id:
            product = self.repo.get_by_id(product_id)
            if product:
                return product, 200
            return {'message': 'Product not found'}, 404

        # Solo retornamos los productos disponibles
        available_products = []
        for product in products:
            product_id = product['id']
            # Consulta el stock usando el InventoryRepository inyectado
            stock = self.inventory_repo.get_stock(product_id) 
                
            if stock > 0:
                available_products.append(product)

        return available_products
              
        return products, 200

    @token_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('category', type=str, required=True, help='Category is required')
        parser.add_argument('price', type=float, required=True, help='Price is required')

        args = parser.parse_args()
        
        products = self.repo.get_all()
        new_product = {
            'id': len(products) + 1,
            'name': args['name'],
            'category': args['category'],
            'price': args['price']
        }

        new_product = self.repo.add(new_product)
        return {'message': 'Product added', 'product': new_product}, 201