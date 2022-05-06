import logging
import time
import traceback
from typing import Dict, Tuple

from hpc_tools_framework.webapp.messenger import Messenger
from hpc_tools_framework.models import (
    Configuration,
    JobConfiguration,
    ProgramConfiguration,
    SettingConfiguration,
    ToolConfiguration,
    SettingType,
)
from hpc_tools_framework.utils import single_or_default, str2int
from hpc_tools_framework.core import Core
import zmq
import json

# logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
logging.getLogger("pssh").setLevel(logging.ERROR)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

core = Core()
messenger = Messenger(socket)


def submit(message, data):
    try:
        program = core.get_program_by_path(data["program_path"])
    except FileNotFoundError as e:
        logging.error(e)
        messenger.send(
            "Error", f"Program {data['program_path']} does not have a Makefile."
        )
    program_config = ProgramConfiguration(program, data["program_parameters"])

    job_config = JobConfiguration(
        minnodes=str2int(data["minnodes"]),
        task_number=str2int(data["ntasks"]),
        partition=data["partition"],
        processes=str2int(data["processes"]),
        source=None,
        cp=None,
        memory=data["memory"],
        timeout=str2int(data["timeout"]),
        mail_notifications=data["mail_notifications"],
        maxnodes=str2int(data["maxnodes"]),
    )

    tool_configs = list()
    for selected_tool in data["tools"]:
        associated_tool_config = single_or_default(core.tools, "title", selected_tool)
        setting_configs = list()
        for setting in associated_tool_config.settings:
            setting_identifier = f"{associated_tool_config.name}-{setting.name}"
            if setting_identifier in data:
                values = data[setting_identifier]
                if setting.type == SettingType.Bool:
                    values = None
                elif setting.type == SettingType.File:
                    pass
                elif setting.type == SettingType.Set:
                    pass
                elif setting.type == SettingType.Textinput:
                    pass
                elif setting.type == SettingType.Numberinput:
                    values = int(values)
                setting_config = SettingConfiguration(
                    name=setting.name, type=setting.type, values=values
                )
                setting_configs.append(setting_config)
        tool_config = ToolConfiguration(
            name=associated_tool_config.name, settings=setting_configs
        )
        tool_configs.append(tool_config)
    config = Configuration(
        job_config,
        tool_configs,
        program_config,
    )
    core.submit(config)
    messenger.send("Submit")


def main():
    while True:
        #  Wait for next request from client
        message, data = messenger.receive()

        if message == "Login":
            success = core.login(
                cluster=data["cluster_name"],
                username=data["username"],
                password=data["password"],
            )
            messenger.send("Login", {"success": success})
            if success:
                core.init_cluster()

        elif message == "LoginCheck":
            loggedin = core.ssh != None
            messenger.send("LoginCheck", {"loggedin": loggedin})

        elif message == "Close":
            messenger.send("Close")
            time.sleep(1)
            raise Exception

        elif message == "Tools":
            messenger.send("Tools", core.tools)

        elif message == "Partitions":
            cluster_info = core.get_cluster_info()
            partitions = [
                partition.name.strip() for partition in cluster_info.partitions
            ]
            messenger.send("Partitions", partitions)

        elif message == "Submit":
            submit(message, data)

        elif message == "Jobs":
            jobs = core.get_all_jobs()
            messenger.send("Jobs", jobs)

        elif message == "Programs":
            programs = core.get_programs()
            messenger.send("Programs", programs)

        else:
            messenger.send("Unknown message")


if __name__ == "__main__":
    try:
        logging.info("Started worker!")
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        messenger.send("Error", e.args)
        traceback.print_exc()
    finally:
        socket.close()
        context.term()
