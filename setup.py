from setuptools import setup, find_packages

setup(
    name='Statisk',
    version='0.0.10',
    packages=find_packages(),
    url='https://github.com/fiskurgit/PyStatisk',
    license='GNU General Public License v3.0',
    author='fiskurgit',
    author_email='fiskdebug@gmail.com',
    description='Simple markdown based low bandwidth static site generator',
    python_requires='>=3', install_requires=['markdown', 'termcolor', 'Pillow'],
    entry_points={
        'console_scripts': [
            'stsk = statisk.PyStatisk:main'
        ],
    }
)
