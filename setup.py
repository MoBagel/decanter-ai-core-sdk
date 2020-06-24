import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = [
    'requests',
    'pandas',
    'matplotlib',
    'tqdm',
    'numpy'
]

dev_requirements = [
    'twine',
    'tox',
    'pytest',
    'responses',
    'flake8',
    'pylint-quotes'
]

setuptools.setup(
    name='decanter-ai-core-sdk',
    version='0.1.3',
    author='',
    author_email='',
    description='Decanter AI Core SDK for the easy use of Decanter Core API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MoBagel/decanter-ai-core-sdk',
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
