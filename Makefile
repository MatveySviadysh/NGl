IMAGE_NAME = ngl-app
CONTAINER_NAME = ngl-app-container
PORT = 8000

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -p $(PORT):8000 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

shell:
	docker exec -it $(CONTAINER_NAME) sh

logs:
	docker logs -f $(CONTAINER_NAME)

migrate:
	docker exec -it $(CONTAINER_NAME) python manage.py migrate

createsuperuser:
	docker exec -it $(CONTAINER_NAME) python manage.py createsuperuser

clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
	docker system prune -f

.PHONY: build run stop shell logs migrate createsuperuser clean
