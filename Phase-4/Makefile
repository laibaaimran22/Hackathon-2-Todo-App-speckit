# Phase 4: Local Kubernetes Deployment Makefile

.PHONY: help build-images deploy-minikube undeploy-minikube test-deployment logs-frontend logs-backend

help: ## Display this help message
	@echo "Phase 4: Local Kubernetes Deployment Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make <target>"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build-images: ## Build Docker images for frontend and backend
	@echo "Building Docker images..."
	docker build -t frontend:latest ./frontend
	docker build -t backend:latest ./backend
	@echo "Docker images built successfully!"

deploy-minikube: ## Deploy application to Minikube using Helm
	@echo "Deploying to Minikube..."
	@echo "Setting Docker environment to Minikube..."
	eval $$(minikube docker-env) && \
	docker build -t frontend:latest ./frontend && \
	docker build -t backend:latest ./backend
	helm install todo-app ./helm-charts/todo-app/
	@echo "Application deployed to Minikube!"

undeploy-minikube: ## Remove application from Minikube
	@echo "Removing application from Minikube..."
	helm uninstall todo-app || true
	@echo "Application removed from Minikube!"

test-deployment: ## Test the deployment
	@echo "Testing deployment..."
	@echo "Checking pods..."
	kubectl get pods
	@echo "Checking services..."
	kubectl get services
	@echo "Checking deployments..."
	kubectl get deployments
	@echo "Deployment test completed!"

logs-frontend: ## View frontend logs
	@echo "Viewing frontend logs..."
	kubectl logs -l app=frontend -f

logs-backend: ## View backend logs
	@echo "Viewing backend logs..."
	kubectl logs -l app=backend -f

minikube-start: ## Start Minikube with recommended settings
	@echo "Starting Minikube..."
	minikube start --memory=4096 --cpus=2
	@echo "Minikube started!"

minikube-stop: ## Stop Minikube
	@echo "Stopping Minikube..."
	minikube stop
	@echo "Minikube stopped!"

minikube-dashboard: ## Open Minikube dashboard
	@echo "Opening Minikube dashboard..."
	minikube dashboard
	@echo "Dashboard opened in browser!"

port-forward-frontend: ## Port forward frontend service
	@echo "Port forwarding frontend service..."
	kubectl port-forward svc/todo-app-frontend 3000:3000

port-forward-backend: ## Port forward backend service
	@echo "Port forwarding backend service..."
	kubectl port-forward svc/todo-app-backend 8000:8000

scale-frontend: ## Scale frontend deployment
	@echo "Scaling frontend deployment..."
	kubectl scale deployment todo-app-frontend --replicas=3
	@echo "Frontend scaled to 3 replicas!"

scale-backend: ## Scale backend deployment
	@echo "Scaling backend deployment..."
	kubectl scale deployment todo-app-backend --replicas=3
	@echo "Backend scaled to 3 replicas!"

reset: ## Reset the environment (undeploy and clean)
	@echo "Resetting environment..."
	make undeploy-minikube
	@echo "Environment reset!"