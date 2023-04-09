# Databricks notebook source
import logging
import os
import pyodbc
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Parse the request body to get the table name
    req_body = req.get_json()
    if req_body and "table_name" in req_body:
        table_name = req_body["table_name"]
    else:
        return func.HttpResponse("Invalid request body.", status_code=400)

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

    # Get a reference to the container where the backup files are stored
    container_name = "silver"
    container_client = blob_service_client.get_container_client(container_name)

    # Download the AVRO backup file from Azure Storage and restore the data in the specified table
    filename = f"{table_name}.avro"
    file_path = os.path.join(os.environ["TMP"], filename)
    blob_client = container_client.get_blob_client(filename)
    with open(file_path, "wb") as avro_file:
        blob_data = blob_client.download_blob()
        blob_data.readinto(avro_file)

    cursor = cnxn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    cnxn.commit()

    with open(file_path, "rb") as avro_file:
        avro_reader = avro.datafile.DataFileReader(avro_file, avro.io.DatumReader())
        for row in avro_reader:
            columns = ", ".join(row.keys())
            values = ", ".join([f"'{value}'" for value in row.values()])
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
        avro_reader.close()

    # Close the PyODBC connection and return a success response
    cursor.close()
    cnxn.close()
    return func.HttpResponse(f"Table {table_name} successfully restored from backup.", status_code=200)

