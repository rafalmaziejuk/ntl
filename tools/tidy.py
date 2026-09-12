#!/usr/bin/env python3

# Copyright 2025-2026 Rafal Maziejuk
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
    run_command_result
)

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

def _build(args):
    """
        Runs CMake build step.
    
        Args:
            args:
                arguments parsed from command-line
        Returns:
            int:
                0 on success, 1 on failure
        """
    cmd = f'cmake --build "{args.dir}"'
    return run_command_result(cmd)

def _check(args):
    """
    Configures and builds the project with clang-tidy check enabled.

    Args:
        args:
            arguments parsed from command-line
    Returns:
        int:
            0 on success, 1 on failure
    """
    if _configure(args) == 1:
        return 1

    if _build(args) == 1:
        return 1
    
    return 0

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
