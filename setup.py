from setuptools import setup, find_packages

setup(
    name='communator-sytadin',
    version='0.9.0',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    install_requires=[
        'dbus-python',
        'beautifulsoup4',
        'requests',
        'sdnotify'
    ],
    entry_points={
        'console_scripts': [
            'commutator-sytadin=commutator_sytadin.main:main',
        ],
    },
    author='Guillaume Scigala',
    author_email='guillaume@scigala.fr',
    description='Sytadin dameon',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/gscigala/commutator-sytadin',
    license = "GPL-3.0-or-later",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
