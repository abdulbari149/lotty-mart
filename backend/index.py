from email.mime import image
import mimetypes
import os
from flask import Blueprint, Flask, render_template, url_for, send_file
from app.auth import AuthService
from app.cart import CartService
from app.order import OrderService
from app.product import ProductService
from app.users import UserService
from flask_cors import CORS
app = Flask(__name__)
app.config['SECRET_KEY']='some-secret-xyz'
app.config.from_pyfile(filename="config.py")
CORS(app)
app.register_blueprint(ProductService().app)
app.register_blueprint(UserService().app)
app.register_blueprint(CartService().app)
app.register_blueprint(OrderService().app)
app.register_blueprint(AuthService().app)

@app.route("/")
def index():
    return { "message": "This is the backend of Lotty Mart written in flask" }
@app.route("/images/<image_name>")
def get_images(image_name):
    print(image_name)
    try:
        ROOT_DIR = os.path.abspath(os.curdir)
        image_path = f"{ROOT_DIR}/static/images/{image_name}"
        mime_type, encoding = mimetypes.guess_type(image_path)
        return send_file(image_path, mimetype=mime_type)
    except FileNotFoundError:
        return { "message": "file not found"}, 404

if __name__ == "__main__":
    app.run(debug=True)