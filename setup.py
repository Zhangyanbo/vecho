from setuptools import setup, find_packages

setup(
    name='beam',
    version='0.1.0',
    packages=find_packages(),
    description='simple, fast vector database',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yanbo Zhang',
    author_email='zhangybspm@gmail.com',
    url='https://github.com/Zhangyanbo/beam',
    install_requires=[
        'numpy'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
