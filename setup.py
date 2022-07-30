
# import tools to create the C extension
from distutils.core import setup, Extension

module_name = 'wordle_fast'
# the files your extension is comprised of
c_files = ['c_extension/test.cpp']

extension = Extension(
    module_name,
    c_files
)

setup(
    name=module_name,
    version='1.0',
    description='The package description',
    author='Ben Payne',
    ext_modules=[extension]
)