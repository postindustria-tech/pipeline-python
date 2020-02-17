from setuptools import setup

setup(name='pipeline-python-core',
      version='0.0.1',
      description='Python Install for the 51Degrees Pipeline API',
      url='https://github.com/Octophin/pipeline-python-core.git',
      author='Octophin Digital / 51 Degrees',
      author_email='hello@octophin.com',
      license='MIT',
      packages=['fiftyone_pipeline_core'],
      install_requires=[flask,requests],
      include_package_data=True,
      zip_safe=False)
