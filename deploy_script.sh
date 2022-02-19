#!/usr/bin/bash

# Conda envinronment
source ~/miniconda3/bin/activate
conda activate SmartForms

echo "========  Installing npm/yarn dependencies"
cd frontend
yarn install --check-file

echo "========  Building for production"
# Build the frontend
cd ../frontend
rm -rf build
yarn build

# Serve the new backend
# Kill the old backend process
PORT=5000
echo "Port is: ${PORT}"
kill -9 $(lsof -t -i :${PORT})

# Save & Delete old logs
cp backend_err.log backend_err.log.bak
cp backend_out.log backend_out.log.bak
rm backend_err.log
rm backend_out.log

echo "========  Serving"
cd ../backend
nohup python sources/main.py 2> backend_err.log 1> backend_out.log & disown
