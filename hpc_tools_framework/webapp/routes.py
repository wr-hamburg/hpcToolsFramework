import logging
from flask import render_template, request, redirect, url_for
from hpc_tools_framework.utils import single_or_default, str2int
from hpc_tools_framework.models import MailType, SettingType
from hpc_tools_framework.core import load_configs
from functools import wraps


def init_app(app, messenger):
    # TODO move this in separate file
    def authorize(func):
        """A decorator which is used to limit access to a route to authorized users only."""

        @wraps(func)
        def decorated_function(*args, **kwargs):
            messenger.send("LoginCheck")
            _, data = messenger.receive()
            if not bool(data["loggedin"]):
                return render_template("401.html")
            return func(*args, **kwargs)

        return decorated_function

    @app.route("/")
    def index():
        return redirect(url_for("login"))

    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            messenger.send("Login", request.form)
            _, data = messenger.receive()
            success = bool(data["success"])
            if success:
                return redirect(url_for("home"))
            else:
                return render_template("login_unsuccessful.html")
        if request.method == "GET":
            return render_template("login.html")
            

    @app.route("/home", methods=["GET"])
    # @authorize
    def home():
        tools = load_configs()
        # TODO list of programs
        programs = ["Dummy 1", "Dummy 2", "Dummy 3", "Dummy 4"]
        mail_notifications = [mail.name for mail in MailType]
        partitions = ["west"]
        # TODO input files
        input_files = ["Dummy 1", "Dummy 2", "Dummy 3", "Dummy 4"]
        return render_template(
            "index.html",
            tools=tools,
            programs=programs,
            input_files=input_files,
            partitions=partitions,
            notifications=mail_notifications,
        )

    @app.route("/partitions", methods=["GET"])
    @authorize
    def partitions():
        return """["west", "abu"]"""
        messenger.send("Partitions")
        _, partitions = messenger.receive()
        return partitions

    @app.route("/submit", methods=["POST"])
    @authorize
    def submit():
        print(request.form)
        tools = load_configs()
        # create dict from the request forms
        # replace some keys with a list of all associated values
        data = dict(request.form)
        data["mail_notifications"] = dict(request.form.lists()).get(
            "mail_notifications", list()
        )
        data["tools"] = dict(request.form.lists()).get("tools", list())
        for selected_tool in data["tools"]:
            associated_tool_config = single_or_default(tools, "title", selected_tool)
            for setting in associated_tool_config.settings:
                setting_identifier = f"{associated_tool_config.name}-{setting.name}"
                if setting_identifier not in data:
                    continue
                else:
                    values = dict(request.form.lists()).get(setting_identifier, list())
                    if setting.type == SettingType.Bool:
                        data[setting_identifier] = ""
                    elif setting.type == SettingType.File:
                        if values == [""]:
                            del data[setting_identifier]
                        else:
                            data[setting_identifier] = values[0]
                    elif setting.type == SettingType.Set:
                        data[setting_identifier] = values
                    elif setting.type == SettingType.Textinput:
                        if values == [""]:
                            del data[setting_identifier]
                        else:
                            data[setting_identifier] = values[0]
                    elif setting.type == SettingType.Numberinput:
                        if values == [""]:
                            del data[setting_identifier]
                        else:
                            data[setting_identifier] = str2int(values[0])
        messenger.send("Submit", data)
        message, data = messenger.receive()
        if message == "Error":
            logging.error(data)
        # TODO stop reloading the page
        return redirect(url_for("home"))

    @app.route("/close")
    def close():
        messenger.send("Close")
        _, _ = messenger.receive()
        return "Closed worker!"

    @app.route("/jobs", methods=["GET"])
    # @authorize
    def jobs():
        return render_template("jobs.html")

    @app.route("/jobs/list", methods=["GET"])
    def jobs_list():
        return """[{"name":"dummy", "tool":"likwid", "setting":"example setting", "state":"running", "starttime":100, "duration":100},
        {"name":"dummy2", "tool":"likwid", "setting":"example setting2", "state":"queued", "starttime":0, "duration":100},
        {"name":"dummy3", "tool":"likwid", "setting":"example setting3", "state":"finished", "starttime":0, "duration":200},
        {"name":"dummy4", "tool":"likwid", "setting":"example setting4", "state":"failed", "starttime":10, "duration":100}]"""
        # TODO use these instead of the dummy data
        messenger.send("Jobs")
        _, jobs = messenger.receive()
        return jsonify(jobs)

    @app.route("/programs", methods=["GET"])
    @authorize
    def programs():
        messenger.send("Programs")
        _, programs = messenger.receive()
        return programs

    @app.route("/download", methods=["POST"])
    @authorize
    def download():
        return ""
