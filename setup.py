from setuptools import setup

setup(
    name='syscourseutils',
    version='0.1.0',
    py_modules=['kwltracking',
                'tasktracking','sitetools'],
    install_requires=[
        'Click', 'pandas', 'lxml', 'numpy','requests','html5lib'
    ],
    entry_points={
        'console_scripts': [
            'kwlfilecheck = kwltracking:get_file_list',
            'kwlfilecount = kwltracking:count_files',
            'kwlextracount = kwltracking:count_extra_files',
            'sysgetassignment = tasktracking:get_assignment',
            'sysfmtassignment = tasktracking:fetch_to_checklist',
            'kwlcsv = sitetools:get_kwl_files'
        ],
    },
)
