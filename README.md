# Use Gemini and Groq(Llama3, Mixtral) and OpenAI for Unary Interface

## Easy Self Host setup for any usage, like CopilotChat.nvim

> Make sure `make` is installed in your system, or your should run command in `Makefile` manually.

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
