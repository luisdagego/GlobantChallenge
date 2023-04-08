# GlobantChallenge

This PoC gonna show how to handle CSV files for make a History copy of inforamation and daily transaccions, follow some requirements like:

1. Move historic data from files in CSV format to the new database.

2. Create a Rest API service to receive new data. This service must have:
  2.1. Each new transaction must fit the data dictionary rules.
  2.2. Be able to insert batch transactions (1 up to 1000 rows) with one request.
  2.3. Receive the data for each table in the same service.
  2.4. Keep in mind the data rules for each table.
  
3. Create a feature to backup for each table and save it in the file system in AVRO format.

4. Create a feature to restore a certain table with its backup.

## Enviroment Info

The enviroment where gonna be placed the solution gonna be Azure Cloud so there is some conciderations for have into account:

1. The CSV files gonna be located into Storage Account from Azule cloud (Low Costs)

2. The Database for sink in this Poc gonna be Azure SQL Database (Low Costs / Basic 4.99 Usd / month)

3. The features needed for the solution gonna be implemented in Azure Functions like a Rest API (Low Costs / Serverless)

4. The main languaje from codes gonna by Python mainly.

## Important Notes

* This escenario not gonna have enviroments like Dev, QA, and Prod, all gonna be handle like a prod endviroment (The correct practices define we need to have the 3 enviroments and also configurations for CI / CD for correct implementation but for this PoC not gonna handle it for times and costs of the proyect)

* Add aditional notes...

