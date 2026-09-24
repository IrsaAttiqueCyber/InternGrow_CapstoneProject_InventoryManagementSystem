import csv
import logging
import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    send_file
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db, login_manager
from app.models import User, Product


main = Blueprint("main", __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@main.route("/")
def home():

    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("main.login"))


@main.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("main.register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for("main.register"))

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        logging.info("New user registered: %s", username)

        flash("Registration successful. Please login.")

        return redirect(url_for("main.login"))

    return render_template("register.html")


@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            login_user(user)

            logging.info("User logged in: %s", username)

            return redirect(url_for("main.dashboard"))

        logging.warning("Failed login attempt: %s", username)

        flash("Invalid username or password.")

    return render_template("login.html")


@main.route("/logout")
@login_required
def logout():

    logging.info(
        "User logged out: %s",
        current_user.username
    )

    logout_user()

    return redirect(url_for("main.login"))


@main.route("/dashboard")
@login_required
def dashboard():

    products = Product.query.all()

    total_products = len(products)

    total_stock = sum(
        product.quantity for product in products
    )

    return render_template(
        "dashboard.html",
        products=products,
        total_products=total_products,
        total_stock=total_stock
    )


@main.route("/products")
@login_required
def products():

    all_products = Product.query.all()

    return render_template(
        "products.html",
        products=all_products
    )


@main.route("/products/add", methods=["GET", "POST"])
@login_required
def add_product():

    if request.method == "POST":

        try:

            name = request.form.get("name")
            category = request.form.get("category")
            quantity = int(request.form.get("quantity"))
            price = float(request.form.get("price"))

            if not name or not category:
                flash("All fields are required.")
                return redirect(url_for("main.add_product"))

            product = Product(
                name=name,
                category=category,
                quantity=quantity,
                price=price
            )

            db.session.add(product)
            db.session.commit()

            logging.info(
                "Product added: %s",
                name
            )

            flash("Product added successfully.")

            return redirect(url_for("main.products"))

        except Exception as e:

            db.session.rollback()

            logging.error(
                "Error adding product: %s",
                str(e)
            )

            flash(
                "An error occurred while adding the product."
            )

    return render_template("add_product.html")


@main.route(
    "/products/edit/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def edit_product(id):

    product = Product.query.get_or_404(id)

    if request.method == "POST":

        try:

            product.name = request.form.get("name")
            product.category = request.form.get("category")
            product.quantity = int(
                request.form.get("quantity")
            )
            product.price = float(
                request.form.get("price")
            )

            db.session.commit()

            logging.info(
                "Product updated: %s",
                product.name
            )

            flash("Product updated successfully.")

            return redirect(url_for("main.products"))

        except Exception as e:

            db.session.rollback()

            logging.error(
                "Error updating product: %s",
                str(e)
            )

            flash("Error updating product.")

    return render_template(
        "edit_product.html",
        product=product
    )


@main.route("/products/delete/<int:id>")
@login_required
def delete_product(id):

    try:

        product = Product.query.get_or_404(id)

        name = product.name

        db.session.delete(product)
        db.session.commit()

        logging.info(
            "Product deleted: %s",
            name
        )

        flash("Product deleted successfully.")

    except Exception as e:

        db.session.rollback()

        logging.error(
            "Error deleting product: %s",
            str(e)
        )

        flash("Error deleting product.")

    return redirect(url_for("main.products"))


@main.route("/export")
@login_required
def export_csv():
    products = Product.query.all()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_dir = os.path.join(base_dir, "exports")

    os.makedirs(export_dir, exist_ok=True)

    file_path = os.path.join(export_dir, "inventory.csv")

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price"
        ])

        for product in products:
            writer.writerow([
                product.id,
                product.name,
                product.category,
                product.quantity,
                product.price
            ])

    logging.info("Inventory exported to CSV.")

    return send_file(
        file_path,
        as_attachment=True
    )