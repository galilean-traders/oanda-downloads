from setuptools import setup

setup(
    name='download_candles',
    version='0.1',
    py_modules=['download_candles'],
    install_requires=[
        'click',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        download_candles=download_candles:download_candles
    ''',
)
