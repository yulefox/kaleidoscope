#!/bin/sh

dir=$1

find gitbook/$dir -name '*.md' | xargs sed -i '' 's/, /，/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/,/，/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/\. /。/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/\./。/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/\: /：/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/\:/：/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/(/（/g'
find gitbook/$dir -name '*.md' | xargs sed -i '' 's/)/）/g'
