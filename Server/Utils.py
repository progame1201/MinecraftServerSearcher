import re

def ver_filter(ver, filter):
    if filter in ver:
        return True
    return False

def pattern_filter(text, pattern):
    if pattern != None:
        f = re.findall(pattern, text)
        if f:
            return True
    return False

def filter(motd, pattern, version, version_filter):
    if pattern != None and version_filter != None:
        if ver_filter(version, version_filter) == True and pattern_filter(motd, pattern) == True:
            return True
        return False

    if pattern != None:
        if pattern_filter(motd, pattern) == True:
            return True
        return False

    if version_filter != None:
        if ver_filter(version, version_filter) == True:
            return True
        return False
    return True

def found_filter(text, online, pattern, version, version_filter, online_filter_raw):
        if online_filter_raw != -1 and online >= online_filter_raw:
          if filter(text, pattern, version, version_filter) != False:
              return True
        elif online_filter_raw != -1:
          return False
        if filter(text, pattern, version, version_filter) != False:
            return True
        return False