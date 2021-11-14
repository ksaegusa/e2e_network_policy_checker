from setuptools import setup, find_packages
 
setup(
    name="e2e_network_policy_checker",
    version="1.0",
    author="ksaegusa",
    author_email="snack11monster@gmail.com",
    description="e2e-network-policy-checker is my own python package",
    entory_points = {
      "console_scripts":[
        "e2e-network-policy-checker = src.main:cli"
      ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires = [
      'fire',
    ],
    url = "https://github.com/ksaegusa/e2e_network_policy_checker.git",
    packages=find_packages(),
)