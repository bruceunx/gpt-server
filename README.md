# Use Gemini and Groq(Llama3, Mixtral) and OpenAI for Unary Interface

## Easy Self Host setup for any usage, like CopilotChat.nvim

> Make sure `make` is installed in your system, or your should run command in `Makefile` manually.

## Add Support for Auto Switch between Gemini Pro 1.5 and Gemini Pro 1.0

## Pre-Requirements

> Make sure you have `docker`.

### Change password in your Makefile for redis server

```makefile
# change password
    docker run --name redis -p 6379:6379 -e REDIS_PASSWORD=123456 -d redis /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'
```

### personal information file .person in root

```sh
groq=<YOUR API KEY>
gemini=<YOUR API KEY>
proxy=<YOUR PROXY>
redis=<REDIS URL>
redis_port=<REDIS Port>
redis_password=<REDIS PASSWORD>
```

## Install Dependencies and Run Server

```sh
make run
```

## Run in docker

```sh
make new
```

## Rebuild docker

```sh
make rebuild
```

## If you want to add new Llm servers.

- copy and past file in routers
- adjust some logic and add
- add routers to `__main__.py`
