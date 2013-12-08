#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
wget -O "$DIR/../cache/gdp.csv" 'http://databank.worldbank.org/data/views/reports/FileDownloadHandler.ashx?filename=3d7520fe-4eb8-4dc6-b683-9e14e9f905b3.csv&filetype=BULKCSV&language=en'