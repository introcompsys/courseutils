from setuptools import setup, find_packages


setup(
    name='syscourseutils',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'pandas', 'lxml'
    ],
    entry_points={
        'console_scripts': [
            'kwlfilecheck = utils.kwltracking:get_file_list',
            'systodo = utils.task_tracking:get_task_text'
        ],
    },
)
