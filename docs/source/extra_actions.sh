pwd
DEST=$1

PILOT_DOCS_DIR=pilot_docs

git clone https://github.com/PanDAWMS/pilot2.git
mkdir -p ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/getting_started ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/doc/components ${DEST}/architecture/${PILOT_DOCS_DIR}
mv pilot2/pilot ${DEST}/

git clone https://github.com/tmaeno/test-actions.git
python source/api_specs/extract_specs.py test-actions/apy.py >> source/api_specs/test.yaml
