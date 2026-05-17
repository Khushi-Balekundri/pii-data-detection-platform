import mysql.connector

def get_connection(db_config):
    if isinstance(db_config, dict):
        return mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["db_name"]
        )
    else:  # DBConfig (BaseModel)
        return mysql.connector.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password,
            database=db_config.db_name
        )
