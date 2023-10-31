#!/bin/bash
set -e

pip () {
    command pip3 "$@"
}

FUNCTION=generate-product-desc
LAMBDA_SOURCE=generate_products_desc.py
PACKAGE_FILE=generate_products_desc.zip

echo "Cleaning up intermediate files"
[ -e ${PACKAGE_FILE} ] && rm ${PACKAGE_FILE}
[ -e "package" ] && rm -rf package

echo "Installing Lambda dependencies"
pip install -r requirements.txt --target ./package

echo "Building Lambda deployment package"
cd package
zip -q -r9 ${OLDPWD}/${PACKAGE_FILE} .
cd ${OLDPWD}

echo "Adding Lambda function source code to package"
zip -q -g ${PACKAGE_FILE} ${LAMBDA_SOURCE}

aws lambda update-function-code --function-name ${FUNCTION}   --zip-file fileb://./${PACKAGE_FILE}
rm $PACKAGE_FILE
echo "Done!"