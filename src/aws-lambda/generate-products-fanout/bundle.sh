#!/bin/bash
set -e

pip () {
    command pip3 "$@"
}

FUNCTION=generate-products-fanout
LAMBDA_SOURCE=${FUNCTION}.py
PACKAGE_FILE=${FUNCTION}.zip

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


echo "Done!"
aws lambda update-function-code --function-name ${FUNCTION}   --zip-file fileb://./${PACKAGE_FILE}
rm $PACKAGE_FILE