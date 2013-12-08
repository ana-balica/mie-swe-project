#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
wget -O "$DIR/../cache/tourism.csv" 'http://databank.worldbank.org/data/views/reports/FileDownloadHandler.ashx?filename=4a7ca97c-3217-4c08-953a-e23e37a8cd58.csv&filetype=BULKCSV&language=en'