import subprocess
import os
import time
import psutil


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

try:
    os.rename('A2A/settings_.py', 'A2A/settings_local.py')

    # Windows
    if os.name == 'nt':
        os.system('init abc')
    else:
        os.system('sh init.sh abc')
    webdriver_manager = subprocess.Popen('webdriver-manager start', shell=True)
    server = subprocess.Popen('python manage.py runserver', shell=True)

    time.sleep(5)
    os.chdir('functional_test')
    exit_code = os.system('protractor conf.js')
    print exit_code
    os.chdir('..')

    kill(webdriver_manager.pid)
    kill(server.pid)
    os.rename('A2A/settings_local.py', 'A2A/settings_.py')
    return exit_code
except:
    os.rename('A2A/settings_local.py', 'A2A/settings_.py')
    return -1
