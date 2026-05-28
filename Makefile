

dev:
	docker compose -f docker-compose.dev.yml up --build


dev-down:
	docker compose -f docker-compose.dev.yml down


dev-logs:
	docker compose -f docker-compose.dev.yml logs -f



prod:
	docker compose -f docker-compose.prod.yml up -d --build


prod-down:
	docker compose -f docker-compose.prod.yml down


prod-logs:
	docker compose -f docker-compose.prod.yml logs -f




clean:
	docker system prune -f



build:
	docker build -t auth-service .


run:
	docker run -p 8000:8000 auth-service