from setuptools import setup
setup(
    name='clean-folder',
    description='sort folder',
    url='http://www.sort folder.ua',
    author='Vadym Marchenko',
    author_email='topim31@gmail.com',
    license='MIT',
    include_package_data=True,
    entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)

