import re
from tooling.frame_generator import get_git

def parse_frames(url):
    COMMENT_REGEX = re.compile('(\/\*\*.*((\n.*)(\*.*)){0,})', re.MULTILINE)
    TEXT_FILTER_REGEX = re.compile('(?<!\/|\*)\*(?!\/)(.*)\n', re.MULTILINE)
    SOURCE_ANCHOR = "/** #PythonAnchor# */"

    git = get_git(url, SOURCE_ANCHOR)[1]
    matches = COMMENT_REGEX.findall(git)
    comments = [TEXT_FILTER_REGEX.findall(match[0]) for match in matches]
    return comments
