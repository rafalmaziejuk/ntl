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

from .git_utils import get_filtered_filepaths
from .utils import (
    find_executable,
    run_command_result
)

CLANG_FORMAT_CMD = find_executable('clang-format')

def _check_prerequisites():
    """
    Checks prerequisites necessary for running a command.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            0 on success, 1 on failure
    """
    if any([CLANG_FORMAT_CMD is None]):
        print("Prerequisites not satisfied")
        return 1
    
    return 0

def _check(args, sources):
    """
    Runs clang-format check on all sources in this repository.

    Args:
        args:
            arguments parsed from command-line
        sources:
            string of space-delimited paths to source files for formatting
    Returns:
        int:
            0 on success, 1 on check failure, 2 on check prerequisites failure
    """
    if _check_prerequisites() == 1:
        return 2

    cmd = f'"{CLANG_FORMAT_CMD}" -Werror --dry-run {sources}'
    return run_command_result(cmd)

def _fix(args, sources):
    """
    Runs clang-format in place fix on all sources in this repository.

    Args:
        args:
            arguments parsed from command-line
        sources:
            string of space-delimited paths to source files for formatting
    Returns:
        int:
            0 on success, 1 on failure
    """
    if _check_prerequisites() == 1:
        return 1

    cmd = f'"{CLANG_FORMAT_CMD}" -Werror --i {sources}'
    return run_command_result(cmd)

def add_subparsers(subparsers):
    """
    Adds subparsers to the main parser.

    Args:
        subparsers:
            main parser subparsers
    """
    format_parser = subparsers.add_parser('format', help='Format code via clang-format')
    format_parser.set_defaults(func=lambda x: format_parser.print_help())

    format_subparsers = format_parser.add_subparsers(help='Format subcommands (<subcommand> -h for subcommand help)',
                                                     dest='command')
    
    dirs = ('include',
            'sandbox',
            'src',
            'tests')
    extensions = ('.cpp',
                  '.h',
                  '.inl')
    sources = get_filtered_filepaths(dirs, extensions)
    sources = ' '.join([str(source) for source in sources])

    format_check_parser = format_subparsers.add_parser("check", help="Check sources formatting")
    format_check_parser.set_defaults(func=lambda args: _check(args, sources))

    format_fix_parser = format_subparsers.add_parser("fix", help="Fix sources formatting")
    format_fix_parser.set_defaults(func=lambda args: _fix(args, sources))
