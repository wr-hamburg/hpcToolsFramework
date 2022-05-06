from pssh.clients import SSHClient
from hpc_tools_framework.io import Server
from typing import List


class SSH:
    """Creates an SSH connection to the specified host and authenticates the user."""

    def __init__(self, server: Server, port: int = 22):
        self.host = server.host
        self.user = server.user
        self.password = server.password
        self.port = port

    def connect(self) -> None:
        self.client = SSHClient(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            num_retries=1,
        )

    def open_shell(self) -> None:
        self.shell = self.client.open_shell()

    def close_shell(self) -> None:
        self.shell.close()

    def __enter__(self):
        self.connect()
        self.open_shell()
        self._read_output()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close_shell()
        self.disconnect()

    def upload_file(self, local_file: str, remote_file: str):
        """Upload a file to the cluster.

        Parameters
        ----------
        local_file : str
            The file path on your local device.
        remote_file : str
            The path on the remote cluster.
        """
        self.client.scp_send(local_file, remote_file)

    def download_file(self, remote_file: str, local_file: str):
        """Download a file from the cluster to your device.

        Parameters
        ----------
        remote_file : str
            The file path on the remote cluster.
        local_file : str
            The file path on your local device.
        """
        self.client.scp_recv(remote_file, local_file)

    def run(self, cmd: str) -> List[str]:
        """Runs a command on the shell.

        Parameters
        ----------
        cmd : str
            The command to run.

        Returns
        -------
        List[str]
            The standard output.
        """
        self.shell.run(cmd)
        return self._read_output()

    def disconnect(self) -> None:
        self.client.disconnect()

    def _read_output(self):
        self.shell.run("echo EOF")
        output = list()
        for line in self.shell.stdout:
            if line == "EOF":
                break
            output.append(line)
        return output
