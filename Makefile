run:
	uvicorn gpt_server:app --host "0.0.0.0" --port 8000 --reload

new: redis
	docker build -t gpt-server .
	docker run -p 8000:8000 --name gpt_server -d gpt-server

rebuild:
	docker stop gpt_server
	docker rm gpt_server
	docker image rm gpt_server
	$(MAKE) new

redis:
	docker pull redis:latest
	docker run --name redis -p 6011:6379 -e REDIS_PASSWORD=123456 -d redis /bin/sh -c 'redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}'
