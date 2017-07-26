# https://docs.python.org/3/library/subprocess.html

from platform import system as system_name
import subprocess
import re

def ping(host):
    """
    Returns a CompletedProcess, containing the results of a system ping command.
    """
    parameters = "-n 2" if system_name().lower()=="windows" else "-c 1"
    return subprocess.run(["ping", parameters, host], stdout=subprocess.PIPE)

host = "www.google.se"
result = ping(host).stdout
rx = re.findall(r"time=(\d{1,}.\d{1,})", str(result))
print(host, '->', rx[0], 'ms')
