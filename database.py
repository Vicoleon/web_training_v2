import os

import sqlalchemy
from sqlalchemy import create_engine, text

my_secret=os.environ['DB_CONNECTION_STRING'] #name of the secret in dev environment
##db connection string

db_connection_string=my_secret

##engine required to connect SSL
engine = create_engine(db_connection_string,connect_args={
"ssl": {
            "ssl_ca": "/etc/ssl/cert.pem"
        }
  
})


##returns jobs from the DB
def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text('select * from jobs'))
        jobs = []
        for row in result:
            jobs.append(row._asdict())   
    return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            statement=text('SELECT * FROM jobs WHERE id= :val'),
            parameters={'val': id} ##pass the param as list
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return rows[0]._asdict()

