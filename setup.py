from setuptools import setup

from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()
license = (this_dir / "LICENSE").read_text()

setup(
    name="Koi Language",
    version="2.0.0",
    description="Koi Programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Israel Waldner",
    author_email="imky171@gmail.com",
    packages=["src", "src.koi", "src.koi.std"],
    entry_points={"console_scripts": ["koi=src.__main__:main"]},
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    project_urls={"Homepage": "https://github.com/IsraelWald/Koi"},
    install_requires=["typing_extensions"],
)
