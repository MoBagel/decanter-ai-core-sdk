import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'requests',
    'pandas',
    'matplotlib',
    'progressbar2',
    'tqdm'
]

dev_requirements = [
    'twine',
    'tox',
    'pytest',
    'responses',
    'flake8'
]

setuptools.setup(
    name='mobagel-corex',
    version='0.1.3',
    author='',
    author_email='',
    description='Mobagel ptyhon coreX sdk for the easy use of coreX API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://gitlab.ct.mobagel.com:7979/GEN/corex-python-sdk',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requires,
    extras_require={
        'dev': dev_requirements
    },
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)
