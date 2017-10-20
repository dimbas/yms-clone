import os
import hashlib
import datetime
import random
import shutil
from xml.etree import ElementTree as ET

from sqlalchemy import event
from werkzeug.utils import secure_filename
from jinja2 import Markup
from flask import url_for
from markdown import markdown

from . import db
from .config import Config
from .utils import thumb_gen


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    image = db.Column(db.String(64), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    html_description = db.Column(db.Text)

    def __str__(self):
        return 'Product({}, title={})'.format(self.id, self.title)

    @property
    def image_thumbnail(self):
        return thumb_gen(self.image_path)

    @property
    def image_path(self):
        return os.path.join('img', self.image)

    @property
    def short_description(self):
        return markdown(self.description[:120], output_format='html5')

    @staticmethod
    def image_name_gen(obj, file_data):
        h = hashlib.md5()
        h.update(file_data.filename.encode() +
                 file_data.content_type.encode() +
                 bytes(file_data.content_length) +
                 str(datetime.datetime.utcnow().timestamp()).encode())
        h.hexdigest()

        _, ext = os.path.splitext(file_data.filename)
        return secure_filename(h.hexdigest() + ext)

    @staticmethod
    def create_image_thumbnail(view, context, model: 'Product', name):
        return Markup('<img src="{}">'.format(url_for('static', filename=model.image_thumbnail)))

    @staticmethod
    def on_product_delete(mapper, conn, target: 'Product'):
        f_name = os.path.join(Config.STATIC_DIR, target.image_path)
        if os.path.exists(f_name):
            os.remove(f_name)

        thumb_f_name = os.path.join(Config.STATIC_DIR, target.image_thumbnail)
        if os.path.exists(thumb_f_name):
            os.remove(thumb_f_name)

    @staticmethod
    def on_description_change(target: 'Product', value, oldvalue, initiator):
        target.html_description = markdown(value, output_format='html5')

    @staticmethod
    def create_db_fake_data(app, count):
        import urllib.request
        import urllib.error

        image_dir = os.path.join(app.static_folder, 'img')

        images_url = 'http://thecatapi.com/api/images/get?results_per_page={}&format=xml&types=jpg'.format(count)
        # resp = requests.get(images_url)
        resp = urllib.request.urlopen(images_url)
        root = ET.fromstring(resp.read().decode())

        for img in root.find('data').find('images').getchildren():
            # get random image from some source
            img_url = img.find('url').text
            try:
                img_data = urllib.request.urlopen(img_url)
            except urllib.error.URLError:
                continue
            # save to img folder with generated name from model
            h = hashlib.md5()
            h.update(img_url.encode() + str(datetime.datetime.utcnow().timestamp()).encode())
            image_file_name = h.hexdigest() + '.jpg'
            image_file_path = os.path.join(image_dir, image_file_name)
            with open(image_file_path, 'wb') as fd:
                fd.write(img_data.read())
            # create strange title
            title = 'cat do {}'.format(image_file_name)
            # create strange description
            description = '\n'.join(['* lots of some text!!!!!!'] * 20)
            # create random price
            price = random.randint(0, 100500)
            # generate thumbnail
            shutil.copyfile(image_file_path, thumb_gen(image_file_path))
            # create model inst and add to db.session
            product = Product(
                title=title,
                image=image_file_name,
                price=price,
                description=description
            )
            db.session.add(product)

        db.session.commit()


event.listen(Product, 'before_delete', Product.on_product_delete)
event.listen(Product.description, 'set', Product.on_description_change)
