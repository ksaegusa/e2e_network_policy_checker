from setuptools import setup, find_packages

setup(
  name='e2e_network_policy_checker',
  version='1.0',
  packages=find_packages(),
  entry_points={
    'console_scripts':
    'e2e-network-policy-checker = e2e_network_policy_checker.cli:cli'
  },
  zip_safe=False,
  classifiers=[
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
  ],
  setup_requires=["click"],
)