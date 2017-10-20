from flask import redirect, request, render_template

from . import app
from .models import Product


@app.route('/')
def index():
    return redirect('products')


@app.route('/products', endpoint='products')
def all_products():
    page = request.args.get('page', 1, type=int)
    pagination = Product.query.paginate(
        page, per_page=app.config['YMS_PRODUCTS_PER_PAGE'],
        error_out=False
    )
    products = pagination.items
    return render_template('products.html', products=products, pagination=pagination)


@app.route('/product/<int:id>', endpoint='product')
def get_product(id: int):
    product = Product.query.get_or_404(id)
    return render_template('product.html', product=product)
