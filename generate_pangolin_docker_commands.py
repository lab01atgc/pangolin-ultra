import os

# Function to read container IDs from file
def read_container_ids(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip() for line in file]
    return data

# Function to create Docker commands for each container ID
def create_docker_commands(container_ids):
    commands = []
    for container_id in container_ids:
        cmd = f'docker run -itd -v /home/project_cdph_1:/data {container_id} /bin/bash -c "pangolin -t 8 --outfile {container_id}_lineage_report.csv /data/gisaid_hcov-19_2022_08_19_16.fasta"'
        commands.append(cmd)
    return commands

# Function to write Docker commands to a bash script
def write_commands_to_file(commands, output_file):
    with open(output_file, "w") as fhandle:
        for cmd in commands:
            fhandle.write(f'{cmd}\n')

def main():
    container_ids_file = 'ids.txt'
    output_script = 'pango.sh'

    container_ids = read_container_ids(container_ids_file)
    docker_commands = create_docker_commands(container_ids)
    write_commands_to_file(docker_commands, output_script)
    os.chmod(output_script, 0o755)  # Make the output script executable

if __name__ == '__main__':
    main()
