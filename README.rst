yms-clone
=========

Simple market clone. Simply shows list of "products" and have simple per product page.

Have admin panel.

.. contents:: **Table of Contents**
    :backlinks: none

License
-------

yms-clone is distributed under the terms of the
`MIT License <https://choosealicense.com/licenses/mit>`_.

Usage
-----

First, specify db url connection and export it into shell `ENV` variable.

After you need to create database table^

.. code-block:: shell

    $ yms-clone shell
    >>> db.create_all()
    >>>

If you want to create demo fake data, you can use ``Product.create_db_fake_data`` in shell dialog to create. It finds `count-1` random images, using thecatapi.com api.

.. code-block:: shell

    >>> Product.create_db_fake_data(app, 25)
    >>>

It will takes some time to fetch all images and create db records.

To start application use cli:

.. code-block:: shell

    $ yms-clone runserver

Don't forget to use `-?` or `--help` if you want use some more options.

After you start server, you can go to `/` index page (it will redirect to `/products` page) or to `/admin` page, to access admin panel.
