from hpc_tools_framework.io import SSH
from hpc_tools_framework.models import ClusterInfo, Partition


def slurm_info(ssh: SSH) -> ClusterInfo:
    """View partition and node information for a system running Slurm.
    Read the docs about the slurm command 'sinfo' at https://slurm.schedmd.com/sinfo.html

    - Partition name followed by "*" for the default partition.
    - Number of nodes.
    - List of node names.

    Parameters
    ----------
    ssh : SSH
        The ssh connection to the server.

    Returns
    -------
    ClusterInfo
        A cluster info object.
    """
    output = ssh.run(f"sinfo --responding -h --format='%R | %D | %c | %e |'") #the information from https://slurm.schedmd.com/sinfo.html has some default values which wont work well. The memory for example is alsways 0.

    partitions = []

    for line in output:
        info_object = line.split("|")
    
        name = info_object[0]
        nodes = info_object[1]
        memory = info_object[3]
        cpus = info_object[2]
        
        partitions.append(Partition(name, nodes, memory, cpus))

    return ClusterInfo(partitions)
