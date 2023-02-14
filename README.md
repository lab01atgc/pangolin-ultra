# {author}
# Project Pangolin – Technical Documentation


### Note 1: Before reading the technical documentation, watch the included short video tutorial for visual walkthrough of steps with a DEMO FASTA file containing only 3 sequences. 

### Note 2: The included project folder includes the following files 

1. sequences_fasta_2022_11_07.tar.xz (this is the FASTA file downloaded from GISAID with ALL SEQ DATA from GISAID as of 2022-11-07. NOTE: This archive will expand to other 400GB! make sure plenty of disk space otherwise will get errors.)

2. metadata_tsv_2022_11_07.tar.xz (metadata file from GISAID for ALL GISAID DATA) 

3. subsampled_sequences_gisaid.fasta ( this contains filtered CA only seq data from the above GISAID Files – 755,865 CA sequences as of 2022_11_07) 

4. pango_vX (folders contain lineage calls on all CA sequences with Pangolin v2, v3, v4 – no v1)

### Note 3: To link the CSV file with the Image ID to release date / pangolin version in the folder there is a file vx_images.txt which links the ID to the Date/Version. Example:

CSV File name - ```a3a8cd4946ae_lineage_report.csv```

| REPOSITORY       | TAG                           | IMAGE ID      | CREATED          | SIZE    |
|------------------|-------------------------------|---------------|------------------|---------|
| staphb/pangolin  | 2.4.2-pangolearn-2021-05-19   | a3a8cd4946ae  | 18 months ago    | 2.35GB  |
| staphb/pangolin  | 2.4.2-pangolearn-2021-05-11   | 85924ba86045  | 18 months ago    | 2.36GB  |


### Note 3: NOT COVERED HERE - Steps to go from downloading the RAW data from GISAID with all global data and filtering only CA sequences. This was done by following steps from the NextStrain Team. 

General advice – subsampling will take a few hours running each of the commands. Recommend use TMUX to leave and come back to check on progress. 

Link - https://docs.nextstrain.org/projects/ncov/en/latest/guides/data-prep/gisaid-full.html





## Introduction 

Project PANGOLIN ULTRA, for a given SARS-CoV-2 viral sequence X we want to know what would have been the pangolin lineage call if the sequence was analyzed with pangolin today, 6 months ago or a year ago with whatever pangolin software version was available at the time. 

Additionally, if we have a file with say 100 combined FASTA sequences and we want to quickly generate all pangolin lineage calls using all versions of PANGOLIN at once - 

This guide provides a solution to these aims. 


## How can we accomplish this?

1. Need a list of all pangolin versions ever released with the version number and release date. Example:

| Date         | Version      |
| ------------ | ------------ |
| Jul 14, 2022 | pangolin v4.1.2  |
| Jun 30, 2022 | pangolin v4.1.12 |



2. Need all pangolin software versions ever released. As of Oct 11, 2022, there are 88 different releases. (https://github.com/cov-lineages/pangolin/releases)


Here we make use of docker containers made by APHL folks where each pangolin software version is enclosed in a separate container with all dependencies to ensure reproducibility. Almost all docker containers have a TAG with version and date. For docker container with no date tag need to match the Pangolin version with the release data from previous link. ( https://hub.docker.com/r/staphb/pangolin ) 

Example:

| REPOSITORY       | TAG                            | IMAGE ID       | CREATED         | SIZE   |
| ---------------- | ------------------------------ | -------------- | --------------- | ------ |
| staphb/pangolin  | 3.1.20-pangolearn-2022-02-28  | 1dacb73e8299   | 5 months ago    | 2.1GB  |
| staphb/pangolin  | 2.3.6-pangolearn-2021-03-16   | f9022682f004   | 16 months ago   | 2.5GB  |

(Only 77 docker containers available AND only 1 docker container for Pangolin v1. Instruction on building your own Docker Containers in the Appendix).


The strategy here is to say that processing viral seq X with 3.1.20-pangolearn-2022-02-28, which is pangolin version 3 released on 2022-02-28 would serve as a proxy for saying what the lineage call would have been if went back in time and processed on 2022-02-28. We repeat this process over all pangolin software versions resulting in a timeline of all possible pango lineage calls over time for sequence X. This historical pango lineage record would be recorded in IGED.

We do this for all CA sequences in GISAID, approximately 755,865 sequences as of 2022-11-07.

3. Computational pipeline overview

We need a way to issue a single command or run a single script where we start one container at a time and run a command inside the container to process a combined FASTA file containing all 755,865 CA sequences and collect the lineage call CSV file for those containers. We do this for all containers automatically in parallel to ensure reproducibility.




## Workflow Notes

Computer Hardware: Google Cloud Virtual Machine with 96 CPU cores and 1.38T RAM. 
Computer Software: Ubuntu 20.04 LTS (x86)
Machine type: m1-megamem-96
CPU platform: Intel Skylake
Architecture: x86/64

NOTE: From my calculations in terms of speed and cost, my current assessment is that one instance with above configuration - 

can successfully process a batch of all docker images from only 1 major Pango version, so 1 Virtual Machine Instance with Pangolin v3 can process all Pango V3 23 containers successfully and will take about 36 hours max to complete the job on 755,865 sequences. To compute Pango V2 spin up another Google Cloud instance with same configuration etc. and another for Pango V4. 



Processing time ~ 36 hours
Total cost ~ 36 hours x 8$/hour = $288

755,865 sequences x 

- 3.1.20-pangolearn-2022-02-28
- 3.1.20-pangolearn-2022-02-02
- 3.1.19-pangolearn-2022-01-20
- 3.1.18-pangolearn-2022-01-20
- 3.1.17-pangolearn-2022-01-05
- 3.1.17-pangolearn-2021-12-06
- 3.1.17-pangolearn-2021-11-25
- 3.1.16-pangolearn-2021-11-25
- 3.1.16-pangolearn-2021-11-18
- 3.1.16-pangolearn-2021-11-09
- 3.1.16-pangolearn-2021-11-04
- 3.1.16-pangolearn-2021-10-18
- 3.1.14-pangolearn-2021-10-13
- 3.1.14-pangolearn-2021-09-28
- 3.1.11-pangolearn-2021-09-17
- 3.1.11-pangolearn-2021-08-24
- 3.1.11-pangolearn-2021-08-09
- 3.1.10-pangolearn-2021-07-28
- 3.1.8-pangolearn-2021-07-28
- 3.1.7-pangolearn-2021-07-09
- 3.1.5-pangolearn-2021-07-07-2
- 3.1.5-pangolearn-2021-06-15
- 3.0.5-pangolearn-2021-06-05




NOTE: We start with a clean machine to ensure reproducibility


-	script to initialize machine

```bash
# script to initialize machine
sudo apt update
sudo apt install build-essential
sudo apt install htop
```


```bash
# installing Docker ( https://docs.docker.com/engine/install/ubuntu/ ) 
sudo apt-get update
sudo apt-get install \
  ca-certificates \
  curl \
  gnupg \
  lsb-release 
```


```bash
# add Docker’s official GPG key:
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
 "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
 $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 

```

```bash
# install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

Pro Tip – run this command to avoid having to use sudo for each docker command (make sure restart machine.

```bash
sudo gpasswd --add $USER docker
```

Download docker containers to machine (https://hub.docker.com/r/staphb/pangolin/tags)

**Example with only 1 container (links provided in the Appendix and the above link)***

```bash
docker pull staphb/pangolin:3.1.20-pangolearn-2022-02-28
```

```bash
# the ---all-tags option will automatically download all docker images at once
docker pull --all-tags staphb/pangolin
```

```bash
docker images
```

EPOSITORY        TAG                          IMAGE ID      CREATED        SIZE
staphb/pangolin  3.1.20-pangolearn-2022-02-28 1dacb73e8299  5 months ago   2.1GB
staphb/pangolin  2.3.6-pangolearn-2021-03-16  f9022682f004  16 months ago  2.5GB

Note: Steps 1 and 2 can be skipped and go straight to Step 3

1. Run a simple command to access the docker container with pangolin 3.1.20-pangolearn-2022-02-28. (This uses the image we downloaded with docker pull and create an active session/container)

```bash
docker run -it 1dacb73e8299
```

2. When we run the container, we also want to run our command to start pangolin and process the data inside the container.

```bash
# -d flag is for detached so it runs in the background since we will start and stop many containers
docker run -itd 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"
```

3. We want to create and attach a Volume/Directory to each container where we have the INPUT FASTA file and the outputs in a separate Volume which we mount and unmount to each container to get the processed lineage call CSV from each container and provide the input FASTA file.


```bash
# -v option specifies a mount Volume
docker run -itd -v /home/project_cdph_1:/data 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"
```
Note: we can also use this equivalent option for step 3 where $(pwd) maps data from current directory to inside docker container, and from within container back out

```bash
# -v option specifies a mount Volume
docker run -itd -v $(pwd):/data 1dacb73e8299 /bin/bash -c "pangolin --outfile 188e28949221_lineage_report.csv /data/gisaid_hcov-19_2022_08_14_01.fasta"
```



***CHECKPOINT:***

What do we have so far?

We can now provide input data and run pangolin in the container and collect output from only 1 container. 

NOTE: each output file includes container ID so we know which pangolin version it was made from) 

How do we scale up?

We can write a script where we loop over each IMAGE_ID (TAG or docker container version) where they run in sequences. 

For example, as one docker container completes running say 2.3.6-pangolearn-2021-03-16 it will output the lineage call and continue to the next container in sequence like 3.1.20-pangolearn-2022-02-28 and repeat for all containers. 


Step 1 – Generate container IDs to generate job start commands and CSV files names

```bash
# grab all container ID and write them to file ids.txt 
docker images | awk '{print $3}' | tail -n +2 > ids.txt 
```

Step 2 – Python script will loop over ID file from Step1 and generate custom compute commands. (If want to run on a different FASTA file or change parameters for PANGOLIN this is where you would make changes and it will generate commands for all containers at once). 

NOTE: Need to run python script in same directory as previous ids.txt file. 

This will generate a pango.sh in same directory file which we run to start all containers. 

```python
## import the txt file with container IDs 
with open('ids.txt', 'r') as file:  data = []
  for line in file:    data.append(line.strip())

## initialize loop to create bash script ## we loop over container id 
pango = []
for i in data:  pango.append(str('docker run -itd -v /home/project_cdph_1://data ') + i + str(' /bin/bash -c "pangolin -t 8 --outfile ') + i + str('_lineage_report.csv /data/gisaid_hcov-19_2022_08_19_16.fasta"'))

## write out the docker commands with open('pango.sh', "w") as fhandle:
 for line in pango:
  fhandle.write(f'{line}\n')
```

Step 3 – run pango.sh which will start all containers

```bash
bash pango.sh 
```



Step 4 – Upload the data to Google Cloud Bucket 

```bash
# Lists all current files in your google bucket
gsutil ls gs://
```

```bash
# replace gs://<insert> with your own bucket path
gsutil cp <file_name> gs://cdph/
```


## Conclusion

The output is a collection of CSV lineage call files. 

From here it is just data wrangling in R/Python. 

Since all CSV files have the same sequence name, CSV files can be merged on the unique sequence name for further analysis looking at how the lineage calls changed over time etc. 



**APPENDIX**

1. Creating your own Docker Images 

GitHub link to all Docker Build Files for Pangolin Containers

Link - https://github.com/StaPH-B/docker-builds/tree/master/pangolin

Guide to build own docker containers from authors of current pangolin containers 

Link - https://staphb.org/docker-builds/make_containers/

```dockerfile
## Dockerfile for building image
FROM ubuntu:xenial

ENV PANGOLIN_VERSION="2.0.4"\ 
  PANGOLIN_LEARN_VERSION="2020-07-20"\
  PANGOLIN_LINEAGES_COMMIT_HASH="549d108a55cad80b35255f4ecda24e351eeadadb"

LABEL base.image="ubuntu:xenial"
LABEL dockerfile.version="1"
LABEL software="pangolin"
LABEL software.version=${PANGOLIN_VERSION}
LABEL description="Conda environment for Pangolin. Pangolin: Software package for assigning SARS-CoV-2 genome sequences to global lineages."
LABEL website="https://github.com/cov-lineages/pangolin"
LABEL license="GNU General Public License v3.0"
LABEL license.url="https://github.com/cov-lineages/pangolin/blob/master/LICENSE.txt"
LABEL maintainer="Erin Young"
LABEL maintainer.email="eriny@utah.gov"
LABEL maintainer2="Anders Goncalves da Silva"
LABEL maintainer2.email="andersgs@gmail.com"

# install needed software for conda install
RUN apt-get update && apt-get install -y \
  wget \
  git \
  build-essential

# get miniconda and the pangolin repo
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
 bash ./Miniconda3-latest-Linux-x86_64.sh -p /miniconda -b  && \
  rm Miniconda3-latest-Linux-x86_64.sh && \
  wget "https://github.com/cov-lineages/pangolin/archive/v${PANGOLIN_VERSION}.tar.gz" && \
  tar -xf v${PANGOLIN_VERSION}.tar.gz && \
  mv pangolin-${PANGOLIN_VERSION} pangolin

# set the environment
ENV PATH="/miniconda/bin:$PATH" \
 LC_ALL=C

# create the conda environment and set as default
RUN conda env create -f /pangolin/environment.yml
RUN echo "source activate pangolin" > /etc/bash.bashrc
ENV PATH /miniconda/envs/pangolin/bin:$PATH
RUN cd pangolin && \
 python setup.py install && \
 mkdir /data

# install and update pangolin learn
# do it here to allow for caching of the previous layers

RUN /bin/bash -c 'cd .. && \
 source activate pangolin && \
 wget https://github.com/cov-lineages/pangoLEARN/archive/${PANGOLIN_LEARN_VERSION}.tar.gz && \
 tar -xf ${PANGOLIN_LEARN_VERSION}.tar.gz && \
 cd pangoLEARN-${PANGOLIN_LEARN_VERSION} && \
 pip install .'

# install the latest lineages release
# looks like it will be deprecated
# because no more tagged releases are planned,
# I am working off commit hashes to aid in 
# reproduciability

RUN /bin/bash -c 'cd .. && \
 source activate pangolin && \
 git clone https://github.com/cov-lineages/lineages.git && \
 cd lineages && \
 git checkout ${PANGOLIN_LINEAGES_COMMIT_HASH} && \
 pip install .'

WORKDIR /data

RUN pangolin -v && pangolin -lv && pangolin -pv
```


2. General TIPS

Use HTOP to monitor how CPU and RAM usage.
Use NCDU to monitor disk usage. 
Use TMUX to safely exit a running process so it does not stop when get disconnected from terminal or other issues leading to loss of connection. 

These can be installed with: 

```sudo apt install htop ncdu tmux```

3. Pangolin Docker Links (also included in CSV files in the project folder)

| Tag                       | Command                                              |
|---------------------------|------------------------------------------------------|
| 2.4.2-pangolearn-2021-05-19 | docker pull staphb/pangolin:2.4.2-pangolearn-2021-05-19 |
| 2.4.2-pangolearn-2021-05-11 | docker pull staphb/pangolin:2.4.2-pangolearn-2021-05-11 |
| 2.4.2-pangolearn-2021-05-10 | docker pull staphb/pangolin:2.4.2-pangolearn-2021-05-10 |
| 2.4.2-pangolearn-2021-04-28 | docker pull staphb/pangolin:2.4.2-pangolearn-2021-04-28 |
| 2.4.1-pangolearn-2021-04-28 | docker pull staphb/pangolin:2.4.1-pangolearn-2021-04-28 |
| 2.4-pangolearn-2021-04-28   | docker pull staphb/pangolin:2.4-pangolearn-2021-04-28   |
| 2.3.8-pangolearn-2021-04-23 | docker pull staphb/pangolin:2.3.8-pangolearn-2021-04-23 |
| 2.3.8-pangolearn-2021-04-21 | docker pull staphb/pangolin:2.3.8-pangolearn-2021-04-21 |
| 2.3.8-pangolearn-2021-04-14 | docker pull staphb/pangolin:2.3.8-pangolearn-2021-04-14 |
| 2.3.8-pangolearn-2021-04-01 | docker pull staphb/pangolin:2.3.8-pangolearn-2021-04-01 |
| 2.3.6-pangolearn-2021-03-29 | docker pull staphb/pangolin:2.3.6-pangolearn-2021-03-29 |
| 2.3.6-pangolearn-2021-03-16 | docker pull staphb/pangolin:2.3.6-pangolearn-2021-03-16 |
| 2.3.5-pangolearn-2021-03-16 | docker pull staphb/pangolin:2.3.5-pangolearn-2021-03-16 |
| 2.3.4-pangolearn-2021-03-16 | docker pull staphb/pangolin:2.3.4-pangolearn-2021-03-16 |
| 2.3.3-pangolearn-2021-03-16 | docker pull staphb/pangolin:2.3.3-pangolearn-2021-03-16 |
| 2.3.2-pangolearn-2021-02-21 | docker pull staphb/pangolin:2.3.2-pangolearn-2021-02-21 |

| Version                      | Command                                          | Date                   |
|------------------------------|--------------------------------------------------|------------------------|
| 4.1.3-pdata-1.15.1           | docker pull staphb/pangolin:4.1.3-pdata-1.15.1    | Oct 12, 2022 at 6:15 am |
| 4.1.2-pdata-1.14             | docker pull staphb/pangolin:4.1.2-pdata-1.14      | Sep 1, 2022 at 1:22 pm  |
| 4.1.2-pdata-1.13             | docker pull staphb/pangolin:4.1.2-pdata-1.13      | Aug 12, 2022 at 9:45 am |
| 4.1.2-pdata-1.12             | docker pull staphb/pangolin:4.1.2-pdata-1.12      | Jul 14, 2022 at 4:46 pm |
| 4.1.1-pdata-1.11             | docker pull staphb/pangolin:4.1.1-pdata-1.11      | Jul 1, 2022 at 12:01 pm |
| 4.0.6-pdata-1.9              | docker pull staphb/pangolin:4.0.6-pdata-1.9       | Jun 2, 2022 at 12:40 pm |
| 4.0.6-pdata-1.8-constellations-0.1.10 | docker pull staphb/pangolin:4.0.6-pdata-1.8-constellations-0.1.10 | May 13, 2022 at 9:51 am |
| 4.0.6-pdata-1.8              | docker pull staphb/pangolin:4.0.6-pdata-1.8       | Apr 29, 2022 at 12:55 pm |
| 4.0.6-pdata-1.6              | docker pull staphb/pangolin:4.0.6-pdata-1.6       | Apr 22, 2022 at 9:45 am |
| 4.0.5-pdata-1.3              | docker pull staphb/pangolin:4.0.5-pdata-1.3       | Apr 12, 2022 at 9:28 am |
| 4.0.4-pdata-1.2.133          | docker pull staphb/pangolin:4.0.4-pdata-1.2.133   | Apr 8, 2022 at 7:11 am  |
| 4.0.3-pdata-1.2.133          | docker pull staphb/pangolin:4.0.3-pdata-1.2.133   | Apr 7, 2022 at 1:17 pm  |
| 4.0.2-pdata-1.2.133          | docker pull staphb/pangolin:4.0.2-pdata-1.2.133   | Apr 6, 2022 at 1:30 pm  |
| 4.0.1                        | docker pull staphb/pangolin:4.0.1                | Apr 4, 2022 at 2:54

