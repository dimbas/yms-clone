from setuptools import find_packages, setup

with open('yms_clone/__init__.py') as fd:
    for line in fd:
        if line.startswith('__version__'):
            VERSION = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        VERSION = '0.0.1'

with open('README.rst') as fd:
    README = fd.read()

with open('requirements/common.txt') as fd:
    REQUIRES = [x.strip() for x in fd.readlines()]

with open('requirements/testing.txt') as fd:
    TEST_REQUIRES = [x.strip() for x in fd.readlines()]

setup(
    name='yms-clone',
    version=VERSION,
    description='',
    long_description=README,
    author='Tambovcev D.A.',
    author_email='tambovcev.dmitry@yandex.ru',
    maintainer='Tambovcev D.A.',
    maintainer_email='tambovcev.dmitry@yandex.ru',
    url='https://github.com/dimbas/yms-clone',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    install_requires=REQUIRES,
    tests_require=TEST_REQUIRES,

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'yms-clone = yms_clone.cli:manager.run',
        ],
    },
)
