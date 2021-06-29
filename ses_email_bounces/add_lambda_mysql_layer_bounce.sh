#create module directory
mkdir -p temp/python
cd temp/python

#install pymysql module
pip install pymysql -t .
cd ..

#create a zip file using installed module
zip -r9 ../pymysql.zip .
cd ..
#create the lambda layer
aws lambda publish-layer-version --layer-name pymysql \
--description "pymysql" \
--zip-file fileb://pymysql.zip \
--compatible-runtimes python3.8 \
--region us-east-1
