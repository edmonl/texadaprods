from setuptools import find_packages, setup

setup(
    name='texadaprods',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'flask-expects-json'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
