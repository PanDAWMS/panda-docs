# cd to the directory of this file and run it to extract the PanDA server API specs
rm -rf panda-server
git clone https://github.com/PanDAWMS/panda-server.git
python openapi_generator.py

# Pinned so a Redocly release can't change the rendered docs unannounced (2.x
# renders with Redoc 2; a later release moves build-docs to Redoc 3). Bump on
# purpose and check the output.
REDOCLY_VERSION=2.62.0
npx -y @redocly/cli@${REDOCLY_VERSION} build-docs panda_api.yaml --output ../_static/panda_api.html
rm -rf panda-server