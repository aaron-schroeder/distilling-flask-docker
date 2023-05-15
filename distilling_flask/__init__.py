import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import mysql.connector


db = SQLAlchemy()


def create_app(config_name='dev'):
    app = Flask(__name__)

    # app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://root:password1@mysqldb/inventory'
    )

    db.init_app(app)

    with app.app_context():
        class UserSettings(db.Model):
            id = db.Column(db.Integer, primary_key=True)
            cp_ms = db.Column(db.Float)
            #     nullable=False,
            #     server_default=sa.text(str(units.pace_to_speed('6:30')))
            # )

            # @property
            # def ftp_ms(self):
            #     return self.cp_ms

    @app.route('/')
    def hello_world():
        return 'Hello, Docker!'
    
    @app.route('/settings')
    def get_settings():
        results = db.session.scalars(db.select(UserSettings)).all()
        json_data = [{'id': r.id, 'cp_ms': r.cp_ms} for r in results]
        return json.dumps(json_data)
    
    @app.route('/initdb')
    def db_init():
        mydb = mysql.connector.connect(
            host="mysqldb",
            user="root",
            password="password1"
        )
        cursor = mydb.cursor()

        cursor.execute("DROP DATABASE IF EXISTS inventory")
        cursor.execute("CREATE DATABASE inventory")
        cursor.close()

        db.drop_all()
        db.create_all()

        # mydb = mysql.connector.connect(
        #     host="mysqldb",
        #     user="root",
        #     password="password1",
        #     database="inventory"
        # )
        # cursor = mydb.cursor()

        # cursor.execute("DROP TABLE IF EXISTS widgets")
        # cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
        # cursor.close()

        return 'init_database'
    
    
    return app





if __name__ == "__main__":
    app = create_app()
    app.run(host ='0.0.0.0')