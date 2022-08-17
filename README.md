
#### Cristian 
#### CDPH Intern
#### Summer 2022


## Introduction

Project PANGOLIN ULTRA, for a given SARS-COV-2 viral sequence X we want to know what would have been the pangolin lineage call if the sequnce was analyzed with pangolin today, 6 months ago or a year ago.


How can we acomplish this ?

1. Need a list of all pangolin versions ever released with the version number and release date. Example:

Jul 14, 2022 | pangolin v4.1.2
Jun 30, 2022 | pangolin v4.1.1

2. Need all pangolin software versions ever released. As of 8/16/2022 there are 87 different releases. ( https://github.com/cov-lineages/pangolin )

Here we make use of docker containers made by APHL folks where each pangolin software version is enclosed in a separate continer with all dependencies to ensure reproducibility. Each docker container has a TAG with version and date. Example:

REPOSITORY        TAG                            IMAGE ID       CREATED         SIZE
staphb/pangolin   3.1.20-pangolearn-2022-02-28   1dacb73e8299   5 months ago    2.1GB
staphb/pangolin   2.3.6-pangolearn-2021-03-16    f9022682f004   16 months ago   2.5GB


**NOTE: The strategy here is to say that processing viral seq X with 3.1.20-pangolearn-2022-02-28, which is pangolin version 3 released on 2022-02-28
would serve as a proxy for saying what the lineage call would have been on 2022-02-28. We repeat this process over all 87 pangolin software versions resulting in a timeline of all possible pango lineage calls over time for sequence x. This historical pango lineage record would be recorded in IGED.
We do this for all CA sequnces in GISAID, aproximately 680, 000 sequnces**


3. Computational pipeline overview: We need a way to issue a single command or run a single script where we start one container at a time and run a command inside the container to process a combined FAST file containining all 680,000 CA sequences and collect the linege call CSV file for that containers. We do this for all 87 containers automaticaly to ensure reproducibility.



## Workflow Notes

Computer Hardware: Google Cloud Virtual Machine Instance with 32 CPU cores and X RAM. 

Computer Software: Ubuntu 20.04 LTS (x86)

NOTE: We start with a clean machine to ensure reproducibility

>script to initialize machine
```bash
sudo apt update 
sudo apt instal build-essential
sudo apt install htop
```



installing Docker ()

```bash
sudo apt-get update

# Update the apt package index and install packages to allow apt to use a repository over HTTPS:
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release


# Add Docker’s official GPG key:
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Use the following command to set up the repository:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null


# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Pro Tip - run this command to avoid having to use sudo for each docker command ( make sure restart machine)
```bash
sudo gpasswd --add $USER docker
```



Download docker continers to machine (https://hub.docker.com/r/staphb/pangolin/tags)

```bash
docker pull staphb/pangolin:3.1.20-pangolearn-2022-02-28
```


```bash
docker images
```
EPOSITORY        TAG                            IMAGE ID       CREATED         SIZE
staphb/pangolin   latest                         188e28949221   4 days ago      2.3GB
staphb/pangolin   3.1.20-pangolearn-2022-02-28   1dacb73e8299   5 months ago    2.1GB
staphb/pangolin   2.3.6-pangolearn-2021-03-16    f9022682f004   16 months ago   2.5GB
staphb/pangolin   1.1.14                         2a61652525ae   2 years ago     1.57GB



1. Run a simple command to access the docker container with pangolin 3.1.20-pangolearn-2022-02-28. (This uses the image we downloaded with docker pull and create an active session/container)

```bash
docker run -it 1dacb73e8299
```

2. When we run the container we also want to run our command to start pangolin and process the data inside the container. 

```bash
# -d flag is for detached so it runs in the background since we will start and stop many containers
docker run -itd 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"
```


3. We want to create and attach a Volume/Directory to each container where we have the INPUT FASTA file and the outputs in a separate Volume which we mount and unmount to each container to get the processed lineage call CSV from each container and provide the input FASTA file. 

```bash

# -v option specifies a mount Volume 
docker run -itd -v /home/project_cdph_1://data 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"
```


CHECKPOINT: What do we have so far ? 

We can now provide input data and run pangolin in the container and collect output from only 1 containers. (Note each outptu file include continer ID so we know which pangolin verison it was made from) How do we scale up ?

We can write a script where we loop over each IMAGE_ID (TAG or docker container version) where they run in sequences. For example, as one docker container completes running say 2.3.6-pangolearn-2021-03-16 it will outptu the lineage call, stop the container and start the next conatiner in sequence like 3.1.20-pangolearn-2022-02-28 and repeat for all containers. Example:


```bash 

# runs container 3.1.20-pangolearn-2022-02-28 
docker run -itd -v /home/project_cdph_1://data 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"























