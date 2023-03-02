from setuptools import setup, find_packages
from os.path import dirname
from os.path import realpath
from os.path import join
import io


def open_config_file(*names, **kwargs):
    current_dir = dirname(realpath(__file__))
    return io.open(
        join(current_dir, *names),
        encoding=kwargs.get('encoding', 'utf8')
    )

install_dependencies = open_config_file('requirements.txt').read().splitlines()

setup(
    name='y2k',
    version='0.1.0',
    author='lucyfer',
    description='insight into bonds',
    packages=find_packages(),
    install_requires=install_dependencies,
    entry_points={
        'console_scripts': [
            "watch = src.watcher:main",

        ]
    }
)
