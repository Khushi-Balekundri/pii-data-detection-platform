import sqlite3
from typing import List, Dict, Any


DEFAULT_SAMPLE_SIZE = 50


def get_connection(db_path: str):
    """
    Create database connection.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"DB connection error: {e}")
        return None



def get_tables(conn) -> List[str]:
    """
    Fetch all table names.
    """
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    tables = [row[0] for row in cursor.fetchall()]
    return tables



def get_columns(conn, table_name: str) -> List[Dict[str, Any]]:
    """
    Fetch column metadata.
    """
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")

    columns = []
    for col in cursor.fetchall():
        columns.append({
            "column_name": col[1],
            "data_type": col[2],
            "not_null": bool(col[3]),
            "primary_key": bool(col[5])
        })

    return columns



def sample_table(conn, table_name: str, sample_size: int = DEFAULT_SAMPLE_SIZE):
    """
    Sample limited rows from table.
    """
    cursor = conn.cursor()

    query = f"""
        SELECT * FROM {table_name}
        LIMIT {sample_size};
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        sampled_data = []
        for row in rows:
            sampled_data.append(dict(zip(column_names, row)))

        return sampled_data

    except Exception as e:
        print(f"Sampling error in table {table_name}: {e}")
        return []



def scan_database(db_path: str, sample_size: int = DEFAULT_SAMPLE_SIZE):
    """
    Scan database schema + sample data.
    Returns structured output for classification pipeline.
    """

    conn = get_connection(db_path)
    if not conn:
        return []

    scan_results = []

    tables = get_tables(conn)

    for table in tables:
        table_info = {
            "table_name": table,
            "columns": [],
        }

        columns = get_columns(conn, table)
        sampled_rows = sample_table(conn, table, sample_size)

        for col in columns:
            column_name = col["column_name"]

            # Extract sample values for this column
            sample_values = [
                str(row[column_name])
                for row in sampled_rows
                if row.get(column_name) is not None
            ]

            table_info["columns"].append({
                "column_name": column_name,
                "db_data_type": col["data_type"],
                "primary_key": col["primary_key"],
                "sample_values": sample_values[:20],  # limit further
            })

        scan_results.append(table_info)

    conn.close()
    return scan_results