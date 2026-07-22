pwd
DEST=$1

PILOT_DOCS_DIR=pilot_docs

# start clean so re-runs don't fail on an existing clone / targets
rm -rf pilot2 ${DEST}/architecture/${PILOT_DOCS_DIR} ${DEST}/pilot

# Add the pilot docs
git clone --depth 1 https://github.com/PanDAWMS/pilot2.git
mkdir -p ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/getting_started ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/components ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/pilot ${DEST}/

# drop the leftover clone so it doesn't linger in the tree
rm -rf pilot2

cp source/api_specs/panda_api.html _static/panda_api.html
