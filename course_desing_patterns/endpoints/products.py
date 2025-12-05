from flask import request
from flask_restful import Resource, reqparse
from utils.security import token_required
from repositories import ProductRepository

class ProductsResource(Resource):
    def __init__(self):
        # Inyección de dependencia "manual"
        self.repo = ProductRepository('db.json') 

    @token_required
    def get(self, product_id=None):
        # Filtro por categoría
        category_filter = request.args.get('category')
        
        if category_filter:
            products = self.repo.get_all()
            filtered = [p for p in products if p['category'].lower() == category_filter.lower()]
            return filtered, 200
        
        if product_id:
            product = self.repo.get_by_id(product_id)
            if product:
                return product, 200
            return {'message': 'Product not found'}, 404
              
        return self.repo.get_all(), 200

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

        self.repo.add(new_product)
        return {'message': 'Product added', 'product': new_product}, 201