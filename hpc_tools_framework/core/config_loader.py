import logging
from typing import Dict, List
from hpc_tools_framework.models import (
    InstallationFlag,
    SingleEnvVar,
    ListedEnvVar,
    Tool,
    ToolInstallation,
    ToolJob,
    ToolSetting,
    ToolCompiler,
    SettingType,
    ToolOutput,
    OutputType,
)

import yaml
import importlib.resources
from yaml.loader import SafeLoader
from yaml.parser import ParserError
import hpc_tools_framework.configs as configs


def dict_2_compiler(data: Dict) -> ToolCompiler:
    if not data:
        return None
    compiler_name = data.get("compiler", None)
    cflags = data.get("cflags", None)
    libs = data.get("libs", None)
    include_link = data.get("include_link", None)
    library_link = data.get("library_link", None)
    compiler_level = data.get("compiler_level", None)
    compiler = ToolCompiler(
        compiler_name, cflags, libs, include_link, library_link, compiler_level
    )
    return compiler


def dict_2_job(data: Dict) -> ToolJob:
    if not data:
        return None
    single_env_variables = list()
    single_env_vars = data.get("single_env_variables", None)
    if single_env_vars:
        for single_env_var in single_env_vars:
            # hack to fix yaml parsing of the string true as bool and then using the capitalized python True
            if isinstance(single_env_var["value"], bool):
                single_env_var["value"] = str(single_env_var["value"]).lower()

            s_env_var = SingleEnvVar(
                name=single_env_var["name"], value=single_env_var["value"]
            )
            single_env_variables.append(s_env_var)
    listed_env_variables = list()
    listed_env_vars = data.get("listed_env_variables", None)
    if listed_env_vars:
        for listed_env_var in listed_env_vars:
            l_env_variables = ListedEnvVar(
                name=listed_env_var["name"],
                values=listed_env_var["values"],
                separator=listed_env_var.get("separator", " "),
            )
            listed_env_variables.append(l_env_variables)
    job = ToolJob(
        single_env_variables=single_env_variables,
        listed_env_variables=listed_env_variables,
        pre_mpi_command=data.get("pre_mpi_command", None),
        post_mpi_command=data.get("post_mpi_command", None),
        post_binary_flags=data.get("post_binary_flags", None),
        cp=data.get("cp", None),
        source=data.get("source", None),
    )
    return job


def dict_2_installation(data: Dict) -> ToolInstallation:
    if not data:
        return None
    flags = list()
    for flag in data["flags"]:
        install_flag = InstallationFlag(
            name=flag["name"],
            value=flag["value"],
            prefix=flag.get("prefix", None),
            suffix=flag.get("suffix", None),
        )
        flags.append(install_flag)
    installation = ToolInstallation(version=data.get("version", None), flags=flags)
    return installation


def dict_2_output(data: Dict) -> ToolOutput:
    if not data:
        return None
    # parse type as OutputType object
    output = ToolOutput(type=OutputType[data["type"]])
    return output


def dict_2_tool(data: Dict) -> Tool:
    compiler = dict_2_compiler(data.get("compiler", None))
    job = dict_2_job(data.get("job", None))
    installation = dict_2_installation(data.get("installation", None))
    output = dict_2_output(data.get("output", None))
    settings = list()
    data_settings = data.get("settings", list())
    if data_settings:
        for setting in data_settings:
            tool_setting = ToolSetting(
                name=setting["name"],
                # parse type as SettingType object
                type=SettingType[setting["type"].lower().capitalize()],
                description=setting.get("description", None),
                values=setting.get("values", None),
                compiler=dict_2_compiler(setting.get("compiler", None)),
                job=dict_2_job(setting.get("job", None)),
                installation=dict_2_installation(setting.get("installation", None)),
            )
            # check if values exist for settings of type set
            if tool_setting.type == SettingType.Set and tool_setting.values == None:
                raise ParserError(f"Values missing for setting '{tool_setting.name}'")
            settings.append(tool_setting)
    tool = Tool(
        title=data["title"],
        fulltitle=data["fulltitle"],
        url=data["url"],
        name=data["name"],
        description=data["description"],
        compiler=compiler,
        job=job,
        installation=installation,
        output=output,
        settings=settings,
    )
    return tool


def load_configs() -> List[Tool]:
    """Loads all yaml config files from the configs folder as tool objects.

    Returns
    -------
    List[Tool]
        List of tool objects with all their settings.
    """
    contents = importlib.resources.contents(configs)
    config_files = [
        file for file in contents if file.endswith(".yml") or file.endswith(".yaml")
    ]
    tools = list()
    for file in config_files:
        try:
            yaml_content = importlib.resources.read_text(configs, file)
            tool_dict = yaml.load(yaml_content, Loader=SafeLoader)
            tool = dict_2_tool(tool_dict)
            tools.append(tool)
            logging.info(f"Loaded {file} successfully.")
        except KeyError as e:
            logging.error(
                f"Could not load {file} because the file format does not match the entity model. There was a keyerror for {e}.",
            )
        except ParserError as e:
            logging.error(
                f"Could not load {file} because the file format does not match the entity model. {e}.",
            )
    return tools