from setuptools import setup, find_packages

setup(
  name='e2e_network_policy_checker',
  version='1.0',
  author="ksaegusa",
  author_email="snack11monster@gmail.com",
  url = "https://github.com/ksaegusa/e2e_network_policy_checker.git",
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
  setup_requires=["click","streamlit"],
)