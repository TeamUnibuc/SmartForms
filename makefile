.PHONY: default backend frontend frontend-packages conda-env

default:
	@echo "available commands:"

	@echo "backend"
	@echo "  -- Starts the backend server locally"

	@echo "frontend"
	@echo "  -- Starts frontend in interactive mode"

	@echo "conda-env"
	@echo "  -- Rebuilds conda environment 'SmartForms'"

backend:
	(cd backend/sources && python main.py)

frontend-packages:
	(cd frontend && yarn)

frontend: frontend-packages
	(cd frontend && yarn start)

conda-env:
	conda env update -f conda_environment.yaml
