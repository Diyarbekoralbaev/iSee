github:
	git add .
	git commit -m "update"
	git pull origin main
	git push

build:
	docker build -t isee:v1 .

run:
	docker run -d -p 7005:80 --name isee isee:v1

stop:
	docker container stop isee

start:
	docker container start isee

delete:
	docker container rm isee

delimage:
	docker image rm isee:v1

logs:
	docker container logs -f isee

connect:
	docker exec -it isee /bin/bash