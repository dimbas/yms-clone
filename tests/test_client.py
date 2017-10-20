import os
import unittest
import hashlib
import datetime
import random
import shutil
from xml.etree import ElementTree as ET

import requests
import requests.exceptions

from yms_clone import init_app, db
from yms_clone.models import Product
from yms_clone.utils import thumb_gen


class TestClient(unittest.TestCase):
    # @classmethod
    # def _create_db_fake_data(cls, count):
    #     image_dir = os.path.join(cls.app.static_folder, 'img')
    #
    #     images_url = 'http://thecatapi.com/api/images/get?results_per_page={}&format=xml&types=jpg'.format(count)
    #     resp = requests.get(images_url)
    #     root = ET.fromstring(resp.text)
    #
    #     for img in root.find('data').find('images').getchildren():
    #         # get random image from some source
    #         img_url = img.find('url').text
    #         try:
    #             img_data = requests.get(img_url).content
    #         except requests.exceptions.ConnectionError:
    #             continue
    #         # save to img folder with generated name from model
    #         h = hashlib.md5()
    #         h.update(img_url.encode() + str(datetime.datetime.utcnow().timestamp()).encode())
    #         image_file_name = h.hexdigest() + '.jpg'
    #         image_file_path = os.path.join(cls.app.static_folder, 'img', image_file_name)
    #         with open(image_file_path, 'wb') as fd:
    #             fd.write(img_data)
    #         # create strange title
    #         title = 'cat do {}'.format(image_file_name)
    #         # create strange description
    #         description = '\n'.join(['lots of some text!!!!!!'] * 20)
    #         # create random price
    #         price = random.randint(0, 100500)
    #         # generate thumbnail
    #         shutil.copyfile(image_file_path, thumb_gen(image_file_path))
    #         # create model inst and add to db.session
    #         product = Product(
    #             title=title,
    #             image=image_file_name,
    #             price=price,
    #             description=description
    #         )
    #         db.session.add(product)
    #
    #     db.session.commit()

    @classmethod
    def setUpClass(cls):
        cls.app = init_app('testing')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()
        Product.create_db_fake_data(cls.app, cls.app.config['FAKE_PRODUCTS_COUNT'])

        cls.client = cls.app.test_client(use_cookies=True)

    @classmethod
    def tearDownClass(cls):
        products = Product.query.all()
        for prod in products:
            # print('delete', prod)
            db.session.delete(prod)
            db.session.commit()

        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)

        resp = self.client.get('/', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('List of Products', resp.data.decode())

    def test_products(self):
        resp = self.client.get('/products')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('List of Products', resp.data.decode())

    def test_product(self):
        resp = self.client.get('/product/1')
        self.assertEqual(resp.status_code, 200)
