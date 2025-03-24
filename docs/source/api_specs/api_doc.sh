# cd to the directory of this file and run it to extract the PanDA server API specs
rm -rf panda-server
git clone https://github.com/PanDAWMS/panda-server.git
python openapi_generator.py

npm install -g @redocly/cli
npx @redocly/cli build-docs panda_api.yaml --output ../_static/panda_api.html
rm -rf panda-server