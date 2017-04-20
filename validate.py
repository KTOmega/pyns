import re

IP_REGEX = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")
HOST_REGEX = re.compile("^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])+$")

def hostname(host):
    return HOST_REGEX.fullmatch(host) is not None

def ip(ip):
    return IP_REGEX.fullmatch(ip) is not None
