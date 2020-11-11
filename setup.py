from setuptools import setup, find_packages


setup(name='renjuu',
      version='1.3',
      url='https://github.com/Ferocius-Gosling/renjuu',
      description='Game renjuu where you should put 5 stones in line',
      packages=find_packages(),
      test_suite='tests',
      install_requires=['pygame==1.9.6', 'pytest'],
      entry_points={
          'console_scripts': ['renjuu-gui=renjuu.__main__']
      }
      )