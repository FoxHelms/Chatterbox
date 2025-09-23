# Chatterbox
Virtual network of chatters

A local network that spins up pairs of containers to "chat" using 
PrivateGPT. Optionally, stores conversations in a shared database. 

## DESIGN

![Alt text](Rough network design)
<img src="./architecture/network-architecture-design.png">

### Setting up Docker Network

This configuration uses a MACVLAN so that the host computer can also 
connect to another container for a chat, or to the database. Importantly, 
MACVLAN only works properly on Linux, because MacOS runs Docker in a VM, 
so there is an internet interface mismatch. You could run this on mac by 
using a bridge or host network instead, but rememmber to expose the ports of your database server so that 
your host mmachine can access conversations.

```
docker network create -d macvlan \ 
--subnet=192.168.1.0/24 \
--ip-range=192.168.1.128/25 \
--gateway=192.168.1.1 \
-o parent=eth0 chatterbox-network
```


TO DO AFTER DINNER??

- simplify your scope: integrate llama with the simple chatroom you have right now, don't worry about 
private connections. 


TO DO

- [ ] Write a turn based chat app wrapper for Ollama python library
- [ ] Implement a shared database
