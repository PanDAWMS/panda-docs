# Extract the PanDA server API specs
git clone https://github.com/PanDAWMS/panda-server.git
python openapi_generator.py

npm install -g @redocly/cli
npx @redocly/cli build-docs panda_api.yaml --output panda_api.html