"""The utility module."""

from hpc_tools_framework.utils.list_extensions import (
    single_or_default,
    is_list_of_strings,
)
from hpc_tools_framework.utils.path_helper import split_filepath
from hpc_tools_framework.utils.merge_settings import extend_or_overwrite
from hpc_tools_framework.utils.cron import add_cronjob, remove_cronjob
from hpc_tools_framework.utils.formatter import (
    time_string,
    home_from_output,
)
from hpc_tools_framework.utils.string_extensions import find_indices_of_substring, str2int
from hpc_tools_framework.utils.variables import Variables
from hpc_tools_framework.utils.git import (
    clone_repo,
    update_repo,
    repo_exists,
    url2dir,
    clone_or_update,
)
from hpc_tools_framework.utils.rpc import call_remote_function
from hpc_tools_framework.utils.object_extensions import values_of_object

__all__ = [
    "single_or_default",
    "is_list_of_strings",
    "extend_or_overwrite",
    "add_cronjob",
    "remove_cronjob",
    "time_string",
    "home_from_output",
    "find_indices_of_substring",
    "str2int",
    "Variables",
    "clone_repo",
    "update_repo",
    "repo_exists",
    "url2dir",
    "clone_or_update",
    "call_remote_function",
    "values_of_object",
    "split_filepath",
]
