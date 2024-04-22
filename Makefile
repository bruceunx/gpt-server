run:
	uvicorn gpt_server:app --host "0.0.0.0" --port 8000 --reload

new:
	docker build -t gpt-server .
	docker run -p 8000:8000 --name gpt_server -d gpt-server

rebuild:
	docker stop gpt_server
	docker rm gpt_server
	docker image rm gpt_server
	$(MAKE) new
