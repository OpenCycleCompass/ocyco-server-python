import subprocess
import time


__title__ = 'Ocyco'
__summary__ = 'Ocyco Server Application - Beta'
__uri__ = 'https://github.com/OpenCycleCompass/ocyco-server-python/'

__version__ = '0.0.2'

__author__ = 'Raphael Lehmann'
__email__ = 'postmaster+pythonserver@open-cycle-compass.de'

__license__ = 'AGPLv3'

try:
    ocyco_git = subprocess.check_output(['git', 'describe', '--always'])
except:
    pass

try:
    ocyco_git_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
except:
    pass

ocyco_start_time = time.time()
