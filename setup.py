from setuptools import find_packages, setup

from chatterbox import __version__


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='chatterbox',
    version=__version__,
    description='Markov chain text generation.',
    long_description=long_description,
    url='https://github.com/thomasleese/chatterbox',
    author='Thomas Leese',
    author_email='inbox@thomasleese.me',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['chatterbox = chatterbox.cli:main']
    },
    test_suite='tests',
    download_url='https://github.com/thomasleese/chatterbox/releases',
    keywords=['markov', 'chain', 'text', 'generation'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
