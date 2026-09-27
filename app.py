from flask import Flask, render_template, request
import oracledb

# Enable thick mode using Oracle Instant Client
oracledb.init_oracle_client(lib_dir=r"C:\instantclient_19_26")  # Make sure this path is correct

app = Flask(__name__)

# Connect to Oracle 10g
connection = oracledb.connect(
    user="system",
    password="system",
    dsn="localhost/XE"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    query = request.form['sql'].strip().rstrip(';')  # Strip any trailing semicolon
    result = None
    error = None

    try:
        cursor = connection.cursor()
        cursor.execute(query)

        if query.lower().startswith("select"):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            result = {'columns': columns, 'rows': rows}
        else:
            connection.commit()
            result = {'message': 'Query executed successfully.'}

    except Exception as e:
        error = str(e)
    finally:
        cursor.close()

    return render_template('result.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)
