#!/usr/bin/env python3

# Copyright 2025 Rafal Maziejuk
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from datetime import datetime

from .git_utils import get_tracked_filepaths

EXTENSION_TO_COMMENT_STYLE = {
    '.cpp': '//',
    '.h': '//',
    '.inl': '//',
    '.py': '#',
}
COPYRIGHT_NOTICE_TEMPLATE = """
Copyright {year_range} Rafal Maziejuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

def _find_year_range(lines):
    """
    Finds a year range pattern match in lines read from file.

    Args:
        lines:
            list of string containing lines read from file
    Returns:
        int, tuple(str):
            index and matched groups tuple pair
    """
    year_pattern = r"Copyright (\d{4})(?:-(\d{4}))? Rafal Maziejuk"
    for index, line in enumerate(lines):
        match = re.search(year_pattern, line)
        if match:
            return index, match.groups()

    return None, None
    
def _update_copyright_notice(path):
    """
    Updates a copyright notice header in a given file.

    Args:
        path:
            path to file
    """
    with open(path, 'r') as file:
        lines = file.readlines()
    
    comment_style = EXTENSION_TO_COMMENT_STYLE[path.suffix]
    current_year = datetime.now().year
    index, year_range = _find_year_range(lines)
    if year_range:
        if any([year for year in year_range if year and int(year) == current_year]):
            return
        
        lines[index] = f"{comment_style}Copyright {year_range[0]}-{current_year} Rafal Maziejuk\n"
    else:
        index = 0
        if lines[0].startswith('#!'):
            index = index + 1

        lines.insert(index, '\n')
        if index > 0:
            index = index + 1

        copyright_notice = COPYRIGHT_NOTICE_TEMPLATE.format(year_range=current_year)[1:]
        copyright_notice_lines = [f"{comment_style} {line}" if line != '\n' else f"{comment_style}{line}" 
                                  for line in copyright_notice.splitlines(True)]
        lines.insert(index, ''.join(copyright_notice_lines))

    with open(path, 'w') as file:
        file.writelines(lines)

def _add_copyright(args):
    """
    Updates files that have a correct extensions with copyright notice.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            always 0 (success)
    """
    excluded_dirs = ('third_party')
    paths = get_tracked_filepaths(excluded_dirs)
    for path in paths:
        if path.suffix in EXTENSION_TO_COMMENT_STYLE.keys():
            _update_copyright_notice(path)

    return 0


def add_subparsers(subparsers):
    """
    Adds subparsers to the main parser.

    Args:
        subparsers:
            main parser subparsers
    """
    copyright_parser = subparsers.add_parser('copyright', help='Add copyright notice to new files')
    copyright_parser.set_defaults(func=_add_copyright)
