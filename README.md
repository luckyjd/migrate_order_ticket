# Challenge
Given the following target schema, and the attached source CSV files,
please write a python script to transform the CSV file into an SQL file(s) capable of being imported against the target
schema.
The target database is MySQL.

- Event
  - id: UUID
  - name: CharField

- Order
  - id: UUID
  - event_id: UUID
  - created: CharField (DateTime YYYY-MM-DD HH:MM:SS+ZZZZ)
  - completed: CharField (DateTime YYYY-MM-DD HH:MM:SS+ZZZZ)
  - price: int (cents)
  - address1: CharField(100)
  - address2: CharField(100)
  - country_code Charfield (choices=[HK, MO, CN])

- Ticket
  - id: UUID
  - order_id: UUID
  - created: CharField (DateTime YYYY-MM-DD HH:MM:SS+ZZZZ)
  - barcode: CharField (16 char [0-9a-f] random)
  - price: int (cents)

1. Comment where there are data gaps from a previous import and how you would expect to cover these gaps, justify
assumptions about likely data transforms. 
2. Where can the target schema not accommodate the source data. Assuming the
application and schema will improve to cover these gaps, what strategy would you suggest to allow the data migration
development process to continue whilst the schema changes are pending, and what process would you recommend to fix
once the target schema has evolved to accept the outstanding data? 
3. What temporary or non-intrustive schema adjustments
would you deem necessary or helpful to this import task if any?

### source_orders.csv

OID,EID,cost,fee,address1,address2,address3,country

1,4,399.96,20,123 main st,shek kip mei,kowloon,hong kong
2,72,159.9,10,40 boundary rd,tsim sha tsui,kowloon,hong kong
3,72,159.9,10,1288 Lianhua Road,Futian District,"Shenzhen, Guangdong",china
4,11,85,5,42 Rua de Madrid,,Sé,macau
5,4,109.99,5,1505 Avenida de Amizade,,Taipa,macau

### source_tickets.csv

TID,OID,utc_timestamp,barcode,cost,fee
1,1,1706534990,A2010557834556546,99.99,5
2,1,1706534990,A2010557834556547,99.99,5
3,1,1706534990,A2010557834556548,99.99,5
4,1,1706534990,A2010557834556549,99.99,5
5,2,1706535006,A2010557834556550,79.5,5
6,2,1706535006,A2010557834556551,79.5,5
7,3,1706535023,A2010557834556552,79.5,5
8,3,1706535023,A2010557834556553,79.5,5
9,4,1706535031,A2010557834556554,85,5
10,5,1706535034,A2010557834556555,109.99,5


* Note: cost value in tickets and orders, there are a slight mismatch in value `79.5 + 79.5 != 159.9` ???? 

# Script in main.py
- put input source csv file in /input 
- `python main.py`
- output file at /output 

# Addressing the Specific Points 

### Data Gaps: 
- The source data might lack direct mappings for `created` and `completed` timestamps in the Order table, requiring assumptions or default values. 
At this script, it is assumed to use the current time `datetime.now().strftime('%Y-%m-%d %H:%M:%S+0000')`.
- Mapping `country` in source_order to `country_code` (choices=[HK, MO, CN])
- Do not have source_events, so generate new UUID for event. Need to ensure consistency in UUID assignment, especially for linking orders to events and tickets to orders.
- `utc_timestamp` convert to datetime format.

### Schema Limitations: 
- The presence of an `address3` field in the source which doesn't exist in the target schema, so suggests combining `address2` and `address3` or using one over the other.
At this script, combining `address2` and `address3` and save to `address2`. 
If `address2` and `address3` in some cases larger than 100 characters, consider having an extra data field outside to store the value of address3 if that field is too necessary.

### Temporary Adjustments: 
- Additional temporary fields or a JSON column to hold unmapped data could be useful, though this script will aim to transform data without schema changes.

### Prepare for update case
- Always prepare for the case when the data is already in the database (for example, in case of re-migrating), then update will be performed instead of insert.
In this script, function `df_to_sql_insert_on_duplicate_key` with boolean `update_flg` will generate sql script with update case.
Function `df_to_DB`, which directly insert data from dataframe to database, cover update case with keyword `if_exists='replace'`