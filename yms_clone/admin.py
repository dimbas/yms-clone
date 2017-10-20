import os

from flask_admin import form
from flask_admin.contrib.sqla import ModelView

from . import db, config
from .models import Product


thumbnail_size = (100, 100, True)


class ProductionAdminView(ModelView):
    column_formatters = {
        'image': Product.create_image_thumbnail
    }

    form_extra_fields = {
        'image': form.ImageUploadField(
            'Image',
            namegen=Product.image_name_gen,
            base_path=os.path.join(config.Config.STATIC_DIR, 'img'),
            thumbnail_size=thumbnail_size)
    }

    column_exclude_list = ['html_description']


def init_admin(admin):
    admin.add_view(ProductionAdminView(Product, db.session))
