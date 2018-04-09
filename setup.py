from distutils.core import setup

version = '0.1.4'

setup(
  name='pipeop',
  packages=['pipeop'],
  version=version,
  description='A decorator that changes the >> operator to mimic Elixir-style function pipes',
  long_description=
  """
  Within the decorated function a >> b(...) becomes b(a, ...):
  
 
      from pipeop import pipes
    
      def add3(a, b, c):
          return a + b + c
      
      def times(a, b):
          return a * b
      
      @pipes
      def calc()
          print 1 >> add3(2, 3) >> times(3)  # prints 18

  """,
  long_description_content_type='text/plain',
  author='Robin Hilliard',
  author_email='robin@rocketboots.com',
  license='MIT',
  url='https://github.com/robinhilliard/pipes',
  download_url='https://github.com/robinhilliard/pipes/blob/master/dist/pipeop-{}.tar.gz'.format(version),
  keywords='python elixir pipe',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7'
  ],
)