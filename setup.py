from distutils.core import setup

version = '0.1.8'

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
  name='pipeop',
  packages=['pipeop'],
  version=version,
  description="A decorator that changes the >> and << operators to mimic Elixir-style function pipes",
  long_description=long_description,
  long_description_content_type='text/x-rst',
  author='Robin Hilliard',
  author_email='robin@rocketboots.com',
  license='MIT',
  url='https://github.com/robinhilliard/pipes',
  download_url='https://github.com/robinhilliard/pipes/blob/master/dist/pipeop-{}.tar.gz?raw=true'.format(version),
  keywords='python elixir pipe',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6'
  ],
)