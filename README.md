# SmartForms

![Deployment](https://github.com/TeamUnibuc/SmartForms/actions/workflows/RPI-Deploy.yaml//badge.svg)

## About

This project aims to help managing simple forms, allowing:
 * Easily creating pdf forms.
 * Filling the forms online.
 * Extracting the data from scanned forms, which were filled on paper.

## Usage

The main prerequisite for this project is to have [conda](https://docs.conda.io/en/latest/) installed.

In order to build & run the project, the `SmartForms` environment needs to be activated..

1. Load the conda environment

    `bash
        conda env update -f conda_environment.yaml
    `

2. Activate the environment

    `bash
        conda activate SmartForms
    `

### Backend

1. Copy `.env.sample` to `.env` - `cp backend/.env.sample backend/.env`.
2. Fill the required data in the env file - `vim backend/.env`. Our own authentication details are stored:
    * As Github secrets.
    * In [this](https://docs.google.com/spreadsheets/d/1BbUoCAjKaVtnTKgnLbWITGRJRHcD6892OqjgR-abZBk/edit#gid=0) document (restricted).
3. Make sure a working `Python 3` interpreter is installed.
4. Install the required `pip` packages - `pip3 install -r backend/requirements.txt`.
5. Start the backend - `make backend` or `cd backend/sources; python3 main.py`.

### Frontend

1. The following `Make` command will install the frontend packages and run the development build:

    `
        make frontend
    `

* Runs `yarn install` inside the `frontend` folder.
* Runs `yarn dev` which in turn calls [Vite](https://vitejs.dev/) for creating & running the dev build.


### Documentation

Check the [wiki](./wiki/wiki.md).
