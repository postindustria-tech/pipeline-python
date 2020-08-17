import setuptools

setuptools.setup(
    name="fiftyone_pipeline_core",
    version="0.0.1",
    author="51Degrees",
    python_requires='>=2.7',
    packages=["fiftyone_pipeline_core"],
    install_requires=[
          'chevron',
          'jsmin'
    ],
    include_package_data=True
)