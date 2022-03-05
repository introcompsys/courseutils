from setuptools import setup

setup(
    name='syscourseutils',
    version='0.1.0',
    py_modules=['kwltracking'],
    install_requires=[
        'Click', 'pandas', 'lxml'
    ],
    entry_points={
        'console_scripts': [
            'kwlfilecheck = kwltracking:get_file_list',
        ],
    },
)
