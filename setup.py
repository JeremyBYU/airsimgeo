from setuptools import setup, find_packages
setup(
    name="airsimgeo",
    version="0.0.1",
    packages=['airsimgeo'],
    scripts=[],

    install_requires=['airsim', 'pip', 'pyproj'],

    # metadata to display on PyPI
    author="Jeremy Castagno",
    author_email="jdcasta@umich.edu",
    description="AirSim with geographic coordinate systems",
    license="MIT",
    keywords="airsim pyproj coordinate systems",
    url="https://github.com/JeremyBYU/airsimgeo",   # project home page, if any
    project_urls={
        "Bug Tracker": "https://github.com/JeremyBYU/airsimgeo/issues",
    }
)