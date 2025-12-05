from flask_restful import Resource, reqparse
from utils.security import token_required
from repositories import FavoriteRepository

class FavoritesResource(Resource):
    def __init__(self):
        self.repo = FavoriteRepository()

    @token_required
    def get(self):
        return self.repo.get_all(), 200

    @token_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')

        args = parser.parse_args()
        new_favorite = {
            'user_id': args['user_id'],
            'product_id': args['product_id']
        }

        self.repo.add(new_favorite)
        return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201

    @token_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('product_id', type=int, required=True, help='Product ID is required')

        args = parser.parse_args()
        
        # Delegamos la lógica de borrado al repositorio
        self.repo.delete(args['user_id'], args['product_id'])

        return {'message': 'Product removed from favorites'}, 200