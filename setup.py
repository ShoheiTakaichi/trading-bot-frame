from setuptools import setup

setup(
    name="botframelib",
    version="0.0.1",
    install_requires=[
        "ccxt==1.91.12",
        "ccxws @ git+https://github.com/ShoheiTakaichi/ccxws.git",
        "loguru==0.6.0",
        "pandas>=1.4.3",
        "PyJWT==2.4.0"
    ],
    extras_require={},
    entry_points={},
)
