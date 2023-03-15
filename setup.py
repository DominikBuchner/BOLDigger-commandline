import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="boldigger-cline",
    version="2.1.1",
    author="Dominik Buchner",
    author_email="dominik.buchner524@googlemail.com",
    description="BOLDigger as a command-line tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DominikBuchner/BOLDigger-commandline",
    packages=setuptools.find_packages(),
    license="MIT",
    install_requires=["tqdm >= 4.32.2", "boldigger >= 2.1.2"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "boldigger-cline = boldigger_cline.__main__:main",
        ]
    },
)
