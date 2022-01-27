from gettext import install


install_requires = [
    "dnspython==2.2.0",
    "montydb==2.3.12",
    "motor==2.5.1",
    "pymongo==3.12.3"
]

from distutils.core import setup
setup(
    name="autodb",
    packages=["autodb"],
    version="0.3",
    license="MIT",
    description="Auto database",
    author="Philippe Mathew",
    author_email="philmattdev@gmail.com",
    url="https://github.com/bossauh/autodb",
    download_url="",
    keywords=["helper", "database"],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
        "Programming Language :: Python :: 3.8"
    ]
)

