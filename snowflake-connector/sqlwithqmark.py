from snowflake import connector
import os
import sf_connector

#Set connector
connector.paramstype = 'qmark' #qmark and numeric both use binding logic
conn = sf_connector('myaccountname','myusername','mypassword')

#build relative file path
current_dir = os.path.dirname(os.path.realpath(__file__))
sql_file_path = os.path.join(current_dir, "testsql.txt")


#build and execute query
with open(sql_file_path) as f:
    sql_scripts = f.read()


values = ("foo","bar")
cs_list = conn.cursor().execute(sql_scripts,[values])

#print out the query result, given the sql cmd returns a json formated response
for cs in cs_list:
    for row in cs:
        try:
            print(json.loads(row[0]))
        except:
            print(row)

conn.close()