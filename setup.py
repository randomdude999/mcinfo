from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='mcinfo',
    version='0.1',
    description="Command-line tool to show information about Minecraft blocks and items.",
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment'
    ],
    keywords='minecraft',
    url='https://github.com/randomdude999/mcinfo',
    license='MIT',
    packages=['mcinfo'],
    entry_points={
        'console_scripts': [
            'mcinfo = mcinfo.cli:main'
        ]
    }
)
