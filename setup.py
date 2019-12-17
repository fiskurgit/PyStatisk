from setuptools import setup

setup(
    name='PyStatisk',
    version='0.0.2',
    packages=['pystatisk'],
    url='https://github.com/fiskurgit/PyStatisk',
    license='GNU General Public License v3.0',
    author='fiskurgit',
    author_email='fiskdebug@gmail.com',
    description='Simple markdown based low bandwidth static site generator',
    python_requires='>=3', install_requires=['markdown', 'termcolor', 'Pillow'],
    entry_points={
        'console_scripts': [
            'pystatisk = PyStatisk:main',
        ],
    }
)
