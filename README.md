# Internet_Security
This project implements several internet security related tools and conceptions in high-level perspective. The scripts are primarily written in Python language.

## Command Tools
- `ifconfig` command, check out network interface in the host
- `nc -lnv <port>` command, set up netcat TCP listenning application from any host to the port number <port> in this host
- `mtr -n <host IP>` command, find the traceroute from current host to destiny host in real time
- `kill -9 <pid>`, to kill process <pid>. `ps`, to find all avaiable processes in OS
- `echo "String" > /dev/<protocol(udp/tcp)>/<IP>/<Port>`, send a single packet with payload "String" to host <IP> <Port> using <protocol>
- `chown -R USER:GROUP DIRECTORY`, change ownership of a directory recursively to User and Group, user or group is optional to fill in

## Environment
- Oracle VM VirtualBox 6.1.42r155177(Qt5.6.2)
- 64 bit Ubuntu 20.04.1 LTS
```
$ uname -ra
Linux VM 5.4.0-54-generic #60-Ubuntu SMP Fri Nov 6 10:37:59 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
$ gcc --version
gcc (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0
Copyright (C) 2019 Free Software Foundation, Inc.

$ python3 --version
Python 3.8.5
$ python3 -m pip show scapy
Name: scapy
Version: 2.4.4
$ wireshark -v
Wireshark 3.2.3 (Git v3.2.3 packaged as 3.2.3-1)
Copyright 1998-2020 Gerald Combs <gerald@wireshark.org> and contributors.

```
## Docker Manual
Docker command alias has permission problem comparing to the full command. Container might not build or run, if type `dcbuild` command in terminal, but `docker-compose build` would work.
```
$ docker-compose build  # Build the container image
$ docker-compose up     # Start the container
$ docker-compose down   # Shut down the container
$ docker network ls     # Find out network ID of docker containers
$ docker network prune  # remove all networks not running in containers now
$ docker rm <name>      # remove the duplicated container name before generating new one
$ docker ps             # List all the running containers in docker
$ dockps        // Alias for: docker ps --format "{{.ID}}  {{.Names}}"
$ docksh <id>   // Alias for: docker exec -it <id> /bin/bash
```

## Notes
Write a function in `~/.bashrc` file, and type `source ~/.bashrc` to activate the function that changes tab name in the Ubunutu terminal. \
`st $TabName`, change the tab name in the default Ubuntu terminal to $TabName

```
alias st=settitle
settitle() {
    TITLE="\[\e]2;$@\a\]"
    PS1=${PS1}${TITLE}
}
```
Other alias set up in SEED image
```
alias ll='ls -l'
PROMPT_DIRTRIM=1
PATH=$PATH:.

# Commands for for docker 
alias dcbuild='docker-compose build'
alias dcup='docker-compose up'
alias dcdown='docker-compose down'
alias dockps='docker ps --format "{{.ID}}  {{.Names}}"'
docksh() { docker exec -it $1 /bin/bash; }
```
## Acknowledge
Python scripts provided in this repository is built upon work in SEED Lab led by Dr.Du who is a professor in Syracuse University.
- https://ecs.syracuse.edu/faculty-staff/wenliang-kevin-du
- https://web.ecs.syr.edu/~wedu/?_gl=1*1c9a7gf*_ga*NDY1OTg1MDU2LjE2NzI4NDcxOTI.*_ga_QT13NN6N9S*MTY3NTI2OTYyMy4xNC4xLjE2NzUyNjk5NzkuNjAuMC4w
- https://seedsecuritylabs.org/index.html

## License
Copyright © 2006 -2020 by Wenliang Du. 

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0International License. If you remix, transform, or build upon the material, this copyright notice must be left intact, or reproduced in a way that is reasonable to the medium in which the work is being republished.