from setuptools import setup, find_packages

setup(
    name='web-scanner',
    version='1.0',
    author='Chrismon Biju',
    author_email='chrismonbiju188@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'web-scanner=web_scanner.main:main'
        ]
    },
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
