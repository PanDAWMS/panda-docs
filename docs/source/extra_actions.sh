pwd
DEST=$1

git clone https://github.com/PanDAWMS/pilot2.git
mv pilot2/doc/components ${DEST}/architecture/pilot_components
mv pilot2/pilot ${DEST}/