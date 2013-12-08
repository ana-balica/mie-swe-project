#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
wget -O "$DIR/../cache/airports.csv" https://sourceforge.net/p/openflights/code/HEAD/tree/openflights/data/airports.dat\?format\=raw