from setuptools import setup, find_packages

setup(
    name='battlemetrics',          # The name of your package
    version='1',                    # The version of your package
    author='Gnomeslayer',                 # The author of the package
    author_email='declan.otten@live.com.au',# The author's email address
    description='Battlemetrics API wrapper.',  # Short description
    long_description=open('README.md').read(),  # Long description from README file
    long_description_content_type='text/markdown',  # Content type of long description
    url='https://github.com/Gnomeslayer/battlemetrics',  # URL of your package
    packages=find_packages(),          # List of packages to include
    classifiers=[                      # Classifiers to categorize your package
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='battlemetrics battlemetricsapi api gaming', # Keywords related to your package
    install_requires=[                  # List of dependencies required by your package
        'aiohttp==3.9.3'
    ],
    python_requires='>=3.6',           # Python version requirements
)