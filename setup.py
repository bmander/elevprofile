import setuptools

setuptools.setup(
    name="elevprofile",
    version="0.1.0",

    author="Brandon Martin-Anderson",
    author_email="badhill@gmail.com",

    description="Find elevation profiles of linestrings.",

    packages=setuptools.find_packages(),

    install_requires=["rasterio","numpy","scipy","shapely"],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
