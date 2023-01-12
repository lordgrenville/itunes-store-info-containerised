import setuptools


setuptools.setup(
    name="itunes-app-scraper-dmi",
    version="0.9.5",
    author="Digital Methods Initiative",
    author_email="stijn.peeters@uva.nl",
    description="A lightweight iTunes App Store scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["requests", "pytest", "behave"],
)
