from dataclasses import dataclass


@dataclass
class Server:
    """A dataclass to store the host and the credentials to connect to a cluster."""

    host: str
    """The cluster address."""
    user: str
    """The username."""
    password: str
    """The password to login the username."""
