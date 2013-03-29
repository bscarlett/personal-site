from distutils.core import setup

setup(
    name='PersonalSite',
    version='0.1',
    packages=['PersonalSite', 'PersonalSite.console', 'PersonalSite.models', 'PersonalSite.tests',
              'PersonalSite.tests.models', 'PersonalSite.tests.views', 'PersonalSite.tests.console'],
    url='',
    license='',
    author='Bradley Scarlett',
    author_email='brad.scarlett@gmail.com',
    description='',
    install_requires=[
        'Flask',
        'mongoengine',
        'nose',
        'lxml',
        'markdown'
    ],
    entry_points={
        'console_scripts': [
            'psconsole = PersonalSite:main'
        ]
    },
    package_data={
        'PersonalSite': ['templates/*.html', 'static/css/*.css', 'static/js/*.js']
    }
)
