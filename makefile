.PHONY: default conda-env deploy 
.PHONY: backend frontend frontend-packages build
.PHONY: test-ci test-frontend-ci test-backend-ci

default:
	@echo "available commands:"

	@echo "backend"
	@echo "  -- Starts the backend server locally"

	@echo "frontend"
	@echo "  -- Starts frontend in interactive mode"

	@echo "build"
	@echo "  -- Builds the project"

	@echo "conda-env"
	@echo "  -- Rebuilds conda environment 'SmartForms'"

backend:
	(cd backend/sources && python main.py)

frontend-packages:
	(cd frontend && yarn)

frontend: frontend-packages
	(cd frontend && yarn start)

build: frontend-packages

test-backend-ci:
	@echo "TODO: No backend tests to run :/"

test-frontend-ci:
	(cd frontend && CI=true yarn test)

test-ci: 
	$(MAKE) test-backend-ci
	$(MAKE) test-frontend-ci

deploy:
	chmod +x deploy_script.sh
	./deploy_script.sh
	@echo " ---- Deploy Finished ---- "

conda-env:
	conda env update -f conda_environment.yaml
