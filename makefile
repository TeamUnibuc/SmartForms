.PHONY: default conda-env deploy 
.PHONY: backend frontend frontend-packages build backend-tests
.PHONY: test-ci test-frontend-ci test-backend-ci

default:
	@echo "available commands:"

	@echo "backend"
	@echo "  -- Starts the backend server locally"

	@echo "backend-tests"
	@echo "  -- Starts the backend unit tests"

	@echo "frontend"
	@echo "  -- Starts frontend in interactive mode"

	@echo "build"
	@echo "  -- Builds the project"

	@echo "conda-env"
	@echo "  -- Rebuilds conda environment 'SmartForms'"

backend:
	(cd backend/sources && python main.py)

backend-train:
	(cd backend/sources && python main.py --train=True)

backend-tests:
	(cd backend/sources/tests && python -m unittest)

frontend-packages:
	(cd frontend && yarn)

frontend: frontend-packages
	(cd frontend && yarn dev)

build: frontend-packages

test-backend-ci:
	@echo "TODO: No backend tests to run :/"

test-frontend-ci:
	(cd frontend && CI=true yarn test)

test-ci: 
	$(MAKE) test-backend-ci
	$(MAKE) test-frontend-ci

# Delete the line 'tensorflow' from pip requirements for arm
# Run the deploy script
# Restore the requirements.txt file
deploy:
	cp ./backend/requirements.txt ./backend/requirements.txt.bak
	sed -i '/tensorflow/d' ./backend/requirements.txt

	chmod +x deploy_script.sh
	./deploy_script.sh

	rm ./backend/requirements.txt
	mv ./backend/requirements.txt.bak ./backend/requirements.txt

	@echo " ---- Deploy Finished ---- "

conda-env:
	conda env update -f conda_environment.yaml
