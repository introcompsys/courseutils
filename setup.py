from setuptools import setup

setup(
    name='syscourseutils',
    version='0.2.0',
    py_modules=['kwltracking','tasktracking'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests'
    ],
    entry_points={
        'console_scripts': [
            'kwlfilecheck = kwltracking:get_file_list',
            'kwlfilecount = kwltracking:count_files',
            'kwlextracount = kwltracking:count_extra_files',
            'sysgetassignment = tasktracking:get_assignment'

        ],
    },
)
