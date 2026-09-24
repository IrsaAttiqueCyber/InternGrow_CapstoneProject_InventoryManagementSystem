from flask import Blueprint, jsonify, request

from app import db
from app.models import Product


api = Blueprint("api", __name__)


@api.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()

    return jsonify([
        {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "quantity": product.quantity,
            "price": product.price
        }
        for product in products
    ])


@api.route("/products", methods=["POST"])
def create_product():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "JSON data is required"
            }), 400

        product = Product(
            name=data["name"],
            category=data["category"],
            quantity=int(data["quantity"]),
            price=float(data["price"])
        )

        db.session.add(product)
        db.session.commit()

        return jsonify({
            "message": "Product created successfully",
            "id": product.id
        }), 201

    except KeyError as e:

        db.session.rollback()

        return jsonify({
            "error": f"Missing field: {e.args[0]}"
        }), 400

    except (ValueError, TypeError) as e:

        db.session.rollback()

        return jsonify({
            "error": f"Invalid data: {str(e)}"
        }), 400

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "error": str(e)
        }), 500