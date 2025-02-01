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

import platform
import subprocess

def find_executable(executable):
    """
    Finds an executable.

    Args:
        executable:
            executable name
    Returns:
        str:
            path to the executable, None if not found
    """
    cmd = "where" if platform.system() == "Windows" else "which"
    return run_command_output(cmd + " " + executable)
    
def run_command_result(command):
    """
    Runs a command and returns the result of that command.

    Args:
        command:
            command to run
    Returns:
        int:
            0 on success, 1 on failure
    """
    print(f'Running [{command}] command', flush=True)
    
    try:
        result = subprocess.run(command, 
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True)
    except subprocess.CalledProcessError:
        print(f'{command} failed to run', flush=True)
        return 1
    
    if result.returncode != 0:
        print("Failed\n")
        print(result.stdout.decode('utf-8'), flush=True)
        return 1

    print("Success\n")
    return 0

def run_command_output(command):
    """
    Runs a command and returns the output of that command.

    Args:
        command:
            command to run
    Returns:
        str:
            output of the command
    """
    try:
        result = subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError:
        print(f'[{command}] failed to run', flush=True)
        return None
    
    return result.decode('utf-8').rstrip()
