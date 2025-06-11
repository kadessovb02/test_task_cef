run:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

build:
	docker compose build --no-cache

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart:
	docker compose down && docker compose up --build

clean:
	docker system prune -af
