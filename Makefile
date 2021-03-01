
.PHONY: all run test stop clean

all: run

run:
	docker-compose -f docker-compose.yml up -d

test:
	docker-compose -f docker-compose.yml -f docker-compose-test.yml up
stop:
	docker-compose stop
clean:
	docker ps -a  | grep team_monitor_web | awk '{print $$1}' | xargs docker rm
