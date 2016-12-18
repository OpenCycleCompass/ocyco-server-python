from setuptools import setup

setup(
    name='OCYCO-Server',
    version='0.0.2',
    packages=['app', 'app.about', 'app.cost_dynamic', 'app.cost_dynamic_precalculated', 'app.cost_static', 'app.geo',
              'app.geocoding', 'app.profile_descriptions', 'app.profiles', 'app.routing', 'app.track_points',
              'app.tracks', 'app.users', 'app.way_type_descriptions', 'app.way_types'],
    url='https://github.com/OpenCycleCompass/ocyco-server-python',
    license='AGPLv3',
    author='Raphael Lehmann',
    author_email='postmaster+pythonserver@open-cycle-compass.de',
    description='Ocyco Server Application - Beta'
)
