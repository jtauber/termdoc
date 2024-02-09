from pathlib import Path
from setuptools import setup


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="termdoc",
    version="0.3",
    description="Python library and tools for working with term-document matrices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/jtauber/termdoc",
    author="James Tauber",
    author_email="jtauber@jtauber.com",
    license="MIT",
    packages=["termdoc"],
)
