# Databricks notebook source
import logging
import os
import pyodbc
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Connect to the Azure SQL database using PyODBC
    server = "sqlsv-base-prod.database.windows.net"
    database = "sqldb-base-prod"
    username = "adminChallenge"
    password = "passwordChallenge01"
    driver = "{ODBC Driver 17 for SQL Server}"
    cnxn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}")

    # Connect to the Azure Storage account using the BlobServiceClient
    connection_string = "DefaultEndpointsProtocol=https;AccountName=adlsbaseprod;AccountKey=xRPmvPEnueIHz5ecL5o7DqCeCeSmdBaqquXOBC5T40z7aza35L9ohZRSoPdO2c6jmMPq7Yr/b4zH+ASt579jsQ==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get a reference to the container where the backup files will be stored
    container_name = "silver"
    container_client = blob_service_client.get_container_client(container_name)

    # Get a list of table names from the Azure SQL database
    cursor = cnxn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    table_names = cursor.fetchall()

    # Serialize the data from each table and save it in an AVRO file in Azure Storage
    for table_name in table_names:
        query = f"SELECT * FROM {table_name[0]}"
        cursor.execute(query)
        rows = cursor.fetchall()

        # Create an AVRO schema based on the columns in the table
        columns = [column[0] for column in cursor.description]
        fields = [{'name': column, 'type': 'string'} for column in columns]
        schema = avro.schema.SchemaFromJSONData({'type': 'record', 'name': table_name[0], 'fields': fields})

        # Serialize the data from the table using the AVRO schema
        filename = f"{table_name[0]}.avro"
        file_path = os.path.join(os.environ["TMP"], filename)
        with open(file_path, "wb") as avro_file:
            writer = DataFileWriter(avro_file, DatumWriter(), schema)
            for row in rows:
                writer.append(dict(zip(columns, row)))
            writer.close()

        # Upload the AVRO file to Azure Storage
        with open(file_path, "rb") as avro_file:
            blob_client = container_client.get_blob_client(filename)
            blob_client.upload_blob(avro_file, overwrite=True)

        # Delete the local AVRO file
        os.remove(file_path)

    # Close the PyODBC connection and return a success response
    cursor.close()
    cnxn.close()
    return func.HttpResponse("Backup successfully created for all tables in Azure SQL database.", status_code=200)

