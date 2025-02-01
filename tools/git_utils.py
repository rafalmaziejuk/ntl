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

import git
import pathlib

repo = git.Repo('.', search_parent_directories=True)

def get_filtered_filepaths(directories=None, extensions=None):
    """
    Returns list of paths to files fitting the criteria.

    Args:
        directories:
            directories that should be a part of filepaths
        extensions:
            extensions that should be a part of filepaths
    Returns:
        list[pathlib.Path]:
            list of paths to all files
    """
    dirs = []
    if directories:
        dirs = [pathlib.Path(repo.working_tree_dir) / dir for dir in directories]
    else:
        dirs = [pathlib.Path(repo.working_tree_dir)]

    filepaths = []
    for dir in dirs:
        if extensions:
            filepaths += [path for path in dir.rglob('*') if path.suffix in extensions]
        else:
            filepaths += [path for path in dir.rglob('*')]

    return filepaths

def get_tracked_filepaths(directories=None):
    """
    Returns list of paths to files, tracked by git, fitting the criteria.

    Args:
        directories:
            directories that should be a part of filepaths

    Returns:
        list[pathlib.Path]:
            list of paths to tracked files
    """
    filepaths = [pathlib.Path(repo.working_tree_dir) / file.a_path
                 for file in repo.index.diff('HEAD', R=True)
                 if file.change_type != 'D']

    if directories:
        filepaths = [path for path in filepaths if not any(part in directories for part in path.parts)]

    return filepaths
