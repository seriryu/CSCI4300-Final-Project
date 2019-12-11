import mysql.connector
from pprint import pprint
import json
import decimal

creds = { 'user' : 'FOO',
          'database' : 'jobs',
          'password' : 'FOOp4ss$',
          'auth_plugin' : 'mysql_native_password'}


def application (env, start_response):
    if (env['REQUEST_METHOD'] == 'GET' and env['QUERY_STRING'] != ''):
        start_response('200 OK', [('Content-Type', 'application/json')])
        body = env['QUERY_STRING']

        body = body.replace("%20", " ")
        id = body.split('=')[1]

        cnx = mysql.connector.connect(**creds)

        cursor = cnx.cursor(dictionary=True)

        sql = ("SELECT title, description FROM job WHERE title = %(value)s")
        params = {'value':id}
        cursor.execute(sql, params)

        values = cursor.fetchall()

        def decimal_default(obj):
            if isinstance(obj, decimal.Decimal):
                return float(obj)
            raise TypeError

        return(json.dumps(values, default=decimal_default))
