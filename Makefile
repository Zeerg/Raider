.PHONY: all up build

all: build up
	
build:
	docker build -t raider:latest .

up:
	docker-compose up

