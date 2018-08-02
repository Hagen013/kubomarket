#!/bin/bash

# FRONTEND
cd ./web/frontend/;
rm -rf /static /static_production;
npm i;
npm  run build;
gulp build;
cd ../../;
# BACKEND
source ../venv/bin/activate;
cd ./web/;
cd ./backend/;
echo 'yes' | python3 manage.py collectstatic --settings=config.settings.production;
deactivate;
cd ../../;
# STATIC_PRODUCTION TO NGINX STATIC
rm -rf ./compose/nginx_cube/static_production;
cp -r ./web/frontend/static_production ./compose/nginx_cube/;
# ADD HASH TO STATIC FILE NAMES IN 
# STATIC FILES AND IN TEMPLATES
hash_suffix="$(date | md5sum | cut -c1-7)"
echo "HASH_SUFFIX=${hash_suffix}"

TEMPLATES_PATH="$(cd ./web/frontend/templates && pwd && cd ../..)"
echo "TEMPLATES_PATH=${TEMPLATES_PATH}"
# STATIC FILES
cd ./compose/nginx_cube/static_production
STATIC_FILE_PATHS=(
    "css/styles.css"
    "js/cartPage.js"
    "js/categoryPage.js"
    "js/common.js"
    "js/indexPage.js"
    "js/productPage.js"
    "js/deliveryPage.js"
    "js/faqPage.js"
    "js/loginPage.js"
    "js/registerPage.js"
    "js/admin.js"
)

# REPLACE STATIC FILES AND TEMPLATES
for file_name in ${STATIC_FILE_PATHS[@]}
do
    new_file_name="${file_name%%.*}_${hash_suffix}.${file_name#*.}"
    cp $file_name $new_file_name
    find $TEMPLATES_PATH -name '*.html' -exec sed -i "s/$(sed 's/\//\\\//g' <<< $file_name)/$(sed 's/\//\\\//g' <<< $new_file_name)/g" '{}' \;
    echo "${file_name} hashed"
done

cd ../..
