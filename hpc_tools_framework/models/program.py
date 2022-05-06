from dataclasses import dataclass


@dataclass()
class Program:
    """Represents a program which can be analyzed by a tool."""

    id: int
    """The id of the program in the database."""
    name: str
    """The name of the program."""
    makefile_path: str
    """The path to the makefile of the program."""
    program_path: str
    """The path to the program."""
    directory: str
    """The directory of the program."""
