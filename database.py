import os

import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
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

def add_application_to_db(job_id, application_data):
    try:
        with engine.connect() as conn:
            statement = text('INSERT INTO applications (job_id, full_name, email, linkedin_url) VALUES (:job_id, :full_name, :email, :linkedin_url)')
            conn.execute(
                statement,
                {
                    'job_id': job_id,
                    'full_name': application_data['full_name'],
                    'email': application_data['email'],
                    'linkedin_url': application_data['linkedin_url']
                }
            )
            conn.commit()  # Commit the transaction if required
    except SQLAlchemyError as e:
        print(f"An error occurred: {str(e)}")