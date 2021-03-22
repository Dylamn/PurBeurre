from src.api import api
from flask_restful import Resource, reqparse
from src.api.models import Product as ProductModel
from src.api.models import UserSubstitute as UserSubstituteModel
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserSubstitute(Resource):
    @jwt_required
    def get(self):
        """Display a listing of the resource."""
        substitutes = UserSubstituteModel.query.filter_by(
            user_id=get_jwt_identity()
        ).all()

        return {
                   'users_substitutes': [s.serialize() for s in substitutes]
               }, 200

    @jwt_required
    def post(self):
        """Store a newly created resource in storage."""
        parser = reqparse.RequestParser()
        parser.add_argument('substitute_id', type=int, required=True) \
            .add_argument('original_product_id', type=int, required=True)

        # Parse arguments...
        args = parser.parse_args()

        original_product_id = args['original_product_id']
        substitute_id = args['substitute_id']
        response = None

        for product_id in args.values():
            exists = ProductModel.query.filter_by(
                id=product_id
            ).first()

            if not exists:
                response = {
                   'status': 422,
                   'message': f'The Product ID {product_id} is invalid.'
                }, 422

            if response is None:
                user_substitute = UserSubstituteModel.first_or_create({
                    'user_id': get_jwt_identity(),
                    'original_product_id': original_product_id,
                    'substitute_product_id': substitute_id
                })

                if not user_substitute.is_recently_created:
                    response = {
                       'status': 422,
                       'message': 'This substitution already exists.'
                    }, 422
                else:
                    response = {
                       'message': 'Your new substitute has been created.',
                       'user_substitute': user_substitute.serialize()
                    }, 201

        return response

    @jwt_required
    def delete(self):
        """Remove the specified resource from storage."""
        parser = reqparse.RequestParser()

        parser.add_argument("original_product_id", type=int, required=True)
        parser.add_argument("substitute_product_id", type=int, required=True)

        args = parser.parse_args()

        user_substitute = UserSubstituteModel.query.filter_by(
            user_id=get_jwt_identity(),
            original_product_id=args["original_product_id"],
            substitute_product_id=args["substitute_product_id"]
        ).first_or_404(description="Substitute doesn't exist.")

        # The substitute exist, proceed with the deletion of it.
        user_substitute.delete()

        return {}, 204

api.add_resource(UserSubstitute, '/users/substitutes')
