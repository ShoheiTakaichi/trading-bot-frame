from setuptools import setup

setup(
    name="botlib",
    version="0.0.1",
    install_requires=[
        "ccxt==1.91.12",
        "ccxws @ git+https://oauth2:gl@gitlab.com//trading_bot/ccxws.git",
        "loguru==0.6.0",
        "PyJWT==2.4.0"
    ],
    extras_require={},
    entry_points={},
)
