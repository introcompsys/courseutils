from setuptools import setup

setup(
    name='syscourseutils',
    version='0.4.0',
    py_modules=['kwltracking','tasktracking','sitetools','badges'],
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
            'sysgetbadgedate = tasktracking:get_badge_date',
            'kwlcsv = sitetools:kwl_csv',
            'verifybadge = badges:verify_badge',
            'verifyjson = badges:process_badges',
            'sysapprovedbadges = badges:cli_get_approved_titles',
            'cleandate = tasktracking:parse_date'
        ],
    },

    zip_safe=False,
    include_package_data=True,
)
