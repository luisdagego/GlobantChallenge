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

## Architecture Design

For this PoC we propose the following modern architecture, perfectly flexible and scalable over time.

![Diagrama ArquitecturaGlobantChallenge drawio](https://user-images.githubusercontent.com/81250098/230745098-3cd96d3a-abe7-4c7e-8ef5-4d3df1d5b7f2.png)

We can find all the steps for finally get the informatios structured and migrated, so in this architecture we need to have some things in mind:

* The develop gonna star after the ingest stpe, with the data loaded into Storage Account
* The step from visualization dont gonna go in this Poc but the data gonna be ready for consumpsumtion in what ever reprt designer like Power Bi, Tablueau server etc.
* For this Challenge the step for serve the information across API gonna be directly for the DB but this is not the best practice as it is not right to hit the data warehouse systems to serve the data with API, this layer should be considered before in the processed data warehouse zone with a GOLD zone.
* We gonna have zonification from datalake with Bronze. Silver and Gold for have the data organized

## Important Notes

* This escenario not gonna have enviroments like Dev, QA, and Prod, all gonna be handle like a prod endviroment (The correct practices define we need to have the 3 enviroments and also configurations for CI / CD for correct implementation but for this PoC not gonna handle it for times and costs of the proyect)

* Add aditional notes...

