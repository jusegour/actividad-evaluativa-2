from flask_restful import Resource, reqparse
from utils.security import token_required
from repositories import CategoryRepository

class CategoriesResource(Resource):
    def __init__(self):
        self.repo = CategoryRepository('db.json')

    @token_required
    def get(self, category_id=None):
        if category_id:
            category = self.repo.get_by_id(category_id)
            if category:
                return category, 200
            return {'message': 'Category not found'}, 404
         
        return self.repo.get_all(), 200 

    @token_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()
        
        name = args['name']
        
        if self.repo.get_by_name(name):
            return {'message': 'Category already exists'}, 400

        categories = self.repo.get_all()
        new_category = {
            'id': len(categories) + 1,
            'name': name
        }
        
        self.repo.add(new_category)
        return {'message': 'Category added successfully', 'category': new_category}, 201

    @token_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()
        
        category_name = args['name']
        
        # Validamos si existe antes de intentar borrar
        if not self.repo.get_by_name(category_name):
            return {'message': 'Category not found'}, 404
            
        self.repo.delete(category_name)
        return {'message': 'Category removed successfully'}, 200