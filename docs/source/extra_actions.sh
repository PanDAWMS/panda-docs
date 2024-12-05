pwd
DEST=$1

PILOT_DOCS_DIR=pilot_docs

# Add the pilot docs
git clone https://github.com/PanDAWMS/pilot2.git
mkdir -p ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/getting_started ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/components ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/pilot ${DEST}/

cp source/api_specs/panda_api.html build/html/panda_api.html