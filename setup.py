from setuptools import setup
import re

packages = []
with open('packages.txt') as f:
    packages = f.read().splitlines()

version = ''
with open('bot/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


setup(name='Demonically',
      author='Xithrius',
      url='https://github.com/Xithrius/Demonically',
      project_urls={
        "Documentation": "https://github.com/Xithrius/Demonically#demonically",
        "Issue tracker": "https://github.com/Xithrius/Demonically/issues",
        "Wiki": "https://github.com/Xithrius/Demonically/wiki"
      },
      version=version,
      packages=['bot', 'bot.essentials'],
      license='MIT',
      description='A demonic bot',
      include_package_data=True,
      install_requires=packages,
      python_requires='>=3.7.2')
