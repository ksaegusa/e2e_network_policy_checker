from setuptools import setup, find_packages
 
setup(
    name="e2e-network-policy-checker",
    version="1.0",
    author="ksaegusa",
    author_email="snack11monster@gmail.com",
    description="e2e-network-policy-checker is my own python package",
    entory_points = {
      "console_scripts":[
        "e2e-network-policy-checker = src.main:cli"
      ]
    },
    install_requires = ['fire'],
    url = "",
    packages=find_packages(),
)