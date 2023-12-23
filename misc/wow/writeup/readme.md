- [2023 PingCTF - misc - wow](#2023-pingctf-misc-wow)
  - [Background information of challenge](#background-information-of-challenge)
  - [Idea](#idea)
  - [Why we can do it](#why-we-can-do-it)
  - [Psudo-code](#psudo-code)
  - [Solution](#solution)
  - [Reproduce the challenge](#reproduce-the-challenge)


# 2023 PingCTF - misc - wow

## Background information of challenge
This game also has a name: Death rolling. It is a mini-game within World of Warcraft (Wow).

## Idea
Bruteforce the seed

## Why we can do it
We know that if a seed is set, the value of random function only depends on the number of times we call it. Here, the server fixes a seed randomly between 1 and 10_000_000 at the beginning of each connection. The server also shows all the value of random function that they run each round.

There is a python module `randcrack`. However, it requires the values of 625 consecutive random function with same range. This module can not be used for this challenge. In this challenge, the ranges are changing. We have to write our own program. Note that although the range of random function changes, but we know exactly what is the range.

## Psudo-code
- Doing about 150 bets with the server. Parse the return from server, extract all random values and store it in a file `data.txt`. With 150 bets, we have approximate 900 random values in `data.txt`.
- Bruteforce the seed between 1-10_000_000 by computing the values of consecutive 625 random functions with that seed and comparing with the values in `data.txt`. I don't know how much consecutive random functions are enough, just take 625 as same as in `randcrack` module. The running time is only about 1 minute.
- After having the seed, we fix the seed and do again 150bets with a simulate game function (not bet with the server) to make the value of random function from the simulate game align with the value of random function in the server.
- Now, before betting with the server, we check the result of the simulate game. If it win, we bet with all our balance, if it lose, we bet 1. Our balance with quickly increase to the limit in about 15-17 rounds. In the last round, we need to check our current balance and opponent balance to have a valid bet.

## Solution
Run `wow.py`. It will print the flag in the end.

We use `socket` python module to interact with the server. Some useful function are:
- open socket: `with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:`
- connect: `s.connect((host,port))`
- receive the message from server: `response = s.recv(1024).decode('utf-8')`
- parse the response by lines: `response.split('\n')`
- send `something` to the server: `s.sendall('something\n'.encode('utf-8'))`
- close connection: `s.close()`
  
## Reproduce the challenge
The organizer of the ctf provided the docker file in the zip file `../wow.zip`. Extract and go to that folder.

Build
```bash
docker compose up --build -d
```

Run
```bash
docker compose up -d
```

Interact with the server
```bash
nc localhost 20001
```

To get the flag with this server, run `wow-localhost.py` (this file modifies `wow.py` by changing`host` from `wow.knping.pl` to `localhost`).