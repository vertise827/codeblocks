virtualenv sfconn
sfconn\Scripts\active


# Setting up virtual env
# Tested requirements can be found here: https://github.com/snowflakedb/snowflake-connector-python/tree/main/tested_requirements
curl https://github.com/snowflakedb/snowflake-connector-python/blob/main/tested_requirements/requirements_38.reqs >> requirements_38.reqs
pip3 install -r requirements_38.reqs
pip install snowflake-connector-python==v3.0.0
