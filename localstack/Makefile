build:
	docker compose up --build --detach
	cd terraform && \
	terraform init && \
	terraform apply --auto-approve

down:
	docker compose down
