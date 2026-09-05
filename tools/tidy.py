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

from .utils import (
    find_executable,
    run_command_result
)

CLANG_TIDY_SCRIPT = find_executable('run-clang-tidy')
CLANG_TIDY_CMD = find_executable('clang-tidy')

def _check_prerequisites():
    """
    Check if prerequisites are satisfied.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            0 on success, 1 on failure
    """
    if any([CLANG_TIDY_CMD is None, 
            CLANG_TIDY_SCRIPT is None]):
        print("Prerequisites not satisfied")
        return 1
    
    return 0

def _configure(args):
    """
    Runs CMake configure step.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            0 on success, 1 on failure
    """
    cmd = f'cmake -B "{args.dir}" --preset clang-tidy'
    return run_command_result(cmd)

def _prepare_compile_commands_file(args):
    """
    Prepares compile_commands.json so that clang-tidy is not run for 3rd party dependencies.

    Args:
        args:
            arguments parsed from command-line
    """
    import json
    from pathlib import Path

    compile_commands_path = Path(args.dir) / 'compile_commands.json'
    with open(compile_commands_path, 'r', encoding='utf-8') as file:
        entries = json.load(file)

    entries = [
        entry
        for entry in entries
        if 'third_party' not in Path(entry['file']).parts
    ]
    
    from re import sub
    for entry in entries:
        entry['command'] = sub(r"(-I)([^ ]*third_party[^ ]*include\b)", r"-isystem \2", entry['command'])
        entry['command'] = sub(r"@[^ ]+\.modmap", "", entry['command'])

    with open(compile_commands_path, 'w', encoding='utf-8') as file:
        json.dump(entries, file, indent=2)

def _check(args):
    """
    Runs clang-tidy check on the whole repository.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            0 on success, 1 on failure
    """
    if _check_prerequisites() == 1:
        return 1

    if _configure(args) == 1:
        return 1
    
    _prepare_compile_commands_file(args)

    cmd = f'python "{CLANG_TIDY_SCRIPT}" -clang-tidy-binary "{CLANG_TIDY_CMD}" -p "{args.dir}"'
    return run_command_result(cmd)

def add_subparsers(subparsers):
    """
    Adds subparsers to the main parser.

    Args:
        subparsers:
            main parser subparsers
    """
    tidy_parser = subparsers.add_parser('tidy', help='Check code via clang-tidy')
    tidy_parser.set_defaults(func=_check)
    tidy_parser.add_argument('--dir', '-d',
                             help='Output binary directory',
                             default='build-tidy',
                             dest='dir')
