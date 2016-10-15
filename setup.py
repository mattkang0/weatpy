import os

from setuptools import setup, find_packages
from distutils.command.build_py import build_py

CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.weatpyrc')


def generate_content():
    # generate the file content...
    return """# weatpy configuration
# Empty lines or lines starting with # will be ignored.
# All other lines must look like "KEY=VALUE" (without the quotes).
# The VALUE must not be enclosed in quotes as well!

# BACKEND to be used (default forecast.io)
backend=forecast.io

# NUMBER of days of weather forecast to be displayed (default 3)
numdays=3

# forecast backend: the api KEY to use (default )
api_key=

# forecast backend: the LANGUAGE to request from forecast.io (default zh)
lang=zh

# FRONTEND to be used (default ascii-art-table)
frontend=ascii-art-table

# LOCATION to be queried (default 40.748,-73.985)
location=22.5333,114.1333

# UNITSYSTEM to use for output.
# Choices are: metric, imperial, si (default metric)
unit=metric
"""


class my_build_py(build_py):
    def run(self):
        # honor the --dry-run flag
        if not self.dry_run:
            if not os.path.exists(CONFIG_FILE):
                print 'creating %s' % CONFIG_FILE
                with open(CONFIG_FILE, 'w') as f:
                    f.write(generate_content())

        # distutils uses old-style classes, so no super()
        build_py.run(self)

setup(
    name='Weatpy',
    version='0.0.1',
    url='',
    description='Weather forecast for the terminal. A Python implementation of wego',
    long_description=open('README.md').read(),
    author='mattkang',
    maintainer='mattkang',
    maintainer_email='mattkang@qq.com',
    license='MIT',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': ['weatpy = weatpy.main:main']
    },
    classifiers=[
        'Framework :: Weatpy',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'requests',
    ],
    cmdclass={'build_py': my_build_py},
)
