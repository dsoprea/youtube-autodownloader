import os
import setuptools

_SHORT_DESCRIPTION = \
    "Tool to auto-download new playlist entries."

_APP_PATH = os.path.dirname(__file__)
_RESOURCES_PATH = os.path.join(_APP_PATH, 'ytad', 'resources')

with open(os.path.join(_RESOURCES_PATH, 'README.rst')) as f:
    _LONG_DESCRIPTION = f.read()

with open(os.path.join(_RESOURCES_PATH, 'requirements.txt')) as f:
    _REQUIREMENTS = [s.strip() for s in f if s.strip() != '']

with open(os.path.join(_RESOURCES_PATH, 'version.txt')) as f:
    _VERSION = f.read().strip()

setuptools.setup(
    name="youtube-autodownloader",
    version=_VERSION,
    description=_SHORT_DESCRIPTION,
    long_description=_LONG_DESCRIPTION,
    classifiers=[],
    keywords='youtube',
    author='Dustin Oprea',
    author_email='dustin@randomingenuity.com',
    url="https://github.com/dsoprea/youtube-autodownloader",
    packages=setuptools.find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    package_data={
        'ytad': [
            'resources/README.rst',
            'resources/requirements.txt',
            'resources/version.txt',
        ],
    },
    scripts=[
        'ytad/resources/scripts/ytad_autodownload',
        'ytad/resources/scripts/ytad_search_playlists',
    ],
    install_requires=_REQUIREMENTS,
)
