import config
import os
import subprocess
import time
import shlex

ADD_TEMPLATE = """
server {ns}
zone {zone}
update add {{name}}.{zone}. 86400 A {{ip}}
send
""".format(ns=config.nameserver, zone=config.zone)
DELETE_TEMPLATE = """
server {ns}
zone {zone}
update delete {{name}}.{zone}. A
send
""".format(ns=config.nameserver, zone=config.zone)

FILENAME_TMPL = "{name}-{time}"

def add(name, ip):
    if not os.path.isdir(config.cache_dir):
        os.mkdir(config.cache_dir)

    ns_file = ADD_TEMPLATE.format(name=name, ip=ip)
    ns_filename = FILENAME_TMPL.format(name=name, time=int(time.time()))
    ns_filepath = "{}/{}.txt".format(config.cache_dir, ns_filename)

    with open(ns_filepath, "w") as ns_fd:
        ns_fd.write(ns_file)

    ns_command = "nsupdate -k {} -v {}".format(shlex.quote(config.key_file), shlex.quote(ns_filepath))

    try:
        ns_output = subprocess.check_output(ns_command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        ns_debugpath = "{}/{}.out".format(config.cache_dir, ns_filename)
        with open(ns_debugpath, "wb") as ns_dbg_fd:
            ns_dbg_fd.write(e.output)
        return False

    ns_debugpath = "{}/{}.out".format(config.cache_dir, ns_filename)
    with open(ns_debugpath, "wb") as ns_dbg_fd:
        ns_dbg_fd.write(ns_output)
    return True

def delete(name):
    if not os.path.isdir(config.cache_dir):
        os.mkdir(config.cache_dir)

    ns_file = DELETE_TEMPLATE.format(name=name)
    ns_filename = FILENAME_TMPL.format(name=name, time=int(time.time()))
    ns_filepath = "{}/{}.txt".format(config.cache_dir, ns_filename)

    with open(ns_filepath, "w") as ns_fd:
        ns_fd.write(ns_file)

    ns_command = "nsupdate -k {} -v {}".format(shlex.quote(config.key_file), shlex.quote(ns_filepath))

    try:
        ns_output = subprocess.check_output(ns_command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        ns_debugpath = "{}/{}.out".format(config.cache_dir, ns_filename)
        with open(ns_debugpath, "wb") as ns_dbg_fd:
            ns_dbg_fd.write(e.output)
        return False

    ns_debugpath = "{}/{}.out".format(config.cache_dir, ns_filename)
    with open(ns_debugpath, "wb") as ns_dbg_fd:
        ns_dbg_fd.write(ns_output)
    return True
