from hpc_tools_framework.io import SSH, Server


def second_shell(ssh: SSH) -> SSH:
    new_ssh = SSH(Server(ssh.host, ssh.user, ssh.password))
    # take over client
    new_ssh.client = ssh.client
    new_ssh.open_shell()
    return new_ssh