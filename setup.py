from setuptools import setup, find_packages

from essentials.pathing import path


def read_requirements():
    with open(path('configuration', 'requirements.txt'), 'r') as f:
        return f.read().split()


if __name__ == "__main__":
    setup(
        name="Demonically",
        version="1.1.1",
        author="Xithrius",
        description="A demonic bot",
        license="MIT",
        url="https://github.com/Xithrius/Demonically",
        packages=find_packages(),
        install_requires=read_requirements()
    )
