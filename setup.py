from setuptools import setup

setup(
    name="Koi",
    version="1.1.1",
    description="Koi Language",
    author="Israel Waldner",
    author_email="imky171@gmail.com",
    packages=["src", "src.koi", "src.koi.std"],
    entry_points={"console_scripts": ["koi=src.__main__:main"]},
)
