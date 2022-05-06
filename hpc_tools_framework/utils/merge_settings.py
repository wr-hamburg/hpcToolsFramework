from typing import TypeVar
from hpc_tools_framework.utils import is_list_of_strings, single_or_default
from hpc_tools_framework.models import (
    ToolInstallation,
    ToolJob,
    ToolCompiler,
    InstallationFlag,
)


T = TypeVar("T", ToolInstallation, ToolJob, ToolCompiler)


def extend_or_overwrite(default: T, extension: T) -> T:
    """Extends or overwrites the attributes of the default object by the attribute values of the provided extension object.

    Parameters
    ----------
    default : T
        The default object.
    extension : T
        The extension object which might contains attribute values which get prioritized.

    Returns
    -------
    T
        A new object which merges the attribute values of the default and extension object.
    """
    if not default:
        return extension
    if not extension:
        return default
    attr_names = [
        attr
        for attr in dir(default)
        if not attr.startswith("__") and not callable(getattr(default, attr))
    ]
    for attr_name in attr_names:
        attribute = getattr(default, attr_name)
        if isinstance(attribute, str):
            if getattr(extension, attr_name):
                setattr(default, attr_name, getattr(extension, attr_name))
        if isinstance(attribute, list):
            if is_list_of_strings(attribute):
                if getattr(extension, attr_name):
                    setattr(default, attr_name, getattr(extension, attr_name))
            else:
                overwrite_attr = list()
                ext_attribute = getattr(extension, attr_name)
                for elem in attribute:
                    name = getattr(elem, "name")
                    ext_elem = single_or_default(ext_attribute, "name", name)
                    if ext_elem:
                        overwrite_attr.append(ext_elem)
                        ext_attribute.remove(ext_elem)
                    else:
                        overwrite_attr.append(elem)
                overwrite_attr.extend(ext_attribute)
                setattr(default, attr_name, overwrite_attr)
    return default


if __name__ == "__main__":
    default = ToolInstallation(
        version="a", flags=[InstallationFlag(name="f", value="v")]
    )
    extension = ToolInstallation(
        version="b",
        flags=[
            InstallationFlag(name="f", value="v2"),
            InstallationFlag(name="f2", value="bla"),
        ],
    )
    test = extend_or_overwrite(default, extension)
    print(test)