import pandas as pd
import uuid
from datetime import datetime
import os
from sqlalchemy import create_engine

from log_handler import logger


current_dir = os.getcwd()

event_column = ['id', 'name']
order_column = ['id', 'event_id', 'created', 'completed', 'price', 'address1', 'address2', 'country_code']
ticket_column = ['id', 'order_id', 'created', 'barcode', 'price']


# Helper functions
def convert_country_to_code(country_name):
    mapping = {"hong kong": "HK", "china": "CN", "macau": "MO"}
    return mapping.get(country_name.lower(), "UNKNOWN")


def convert_unix_to_datetime(unix_time):
    return datetime.utcfromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M:%S+0000')


def price_to_cents(price):
    return int(float(price) * 100)


def generate_uuid():
    return str(uuid.uuid4())


def gen_df(orders_path, tickets_path):
    """Function to read csv, generate dataframe and transform data"""
    # Read source CSV files
    orders_df = pd.read_csv(orders_path)
    tickets_df = pd.read_csv(tickets_path)

    # Generate Events DataFrame
    events_df = pd.DataFrame(orders_df['EID'].unique(), columns=['EID'])
    events_df['id'] = events_df.apply(lambda _: generate_uuid(), axis=1)
    events_df['name'] = 'Event ' + events_df['EID'].astype(str)  # Just use format Event + EID

    # Map EID to event_id in orders
    eid_event_id_map = events_df.set_index('EID')['id'].to_dict()
    orders_df['event_id'] = orders_df['EID'].map(eid_event_id_map)

    # Orders transformations
    orders_df['id'] = orders_df.apply(lambda _: generate_uuid(), axis=1)
    orders_df['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S+0000')  # Placeholder
    orders_df['completed'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S+0000')  # Placeholder
    orders_df['price'] = (orders_df['cost'] + orders_df['fee']).apply(price_to_cents)
    orders_df['country_code'] = orders_df['country'].apply(convert_country_to_code)
    orders_df['address2'] = orders_df.apply(lambda row:
                                            (str(row['address2']) + ', ' if pd.notna(row['address2']) else '') +
                                            str(row['address3']),
                                            axis=1)

    # orders_df['address2'] = orders_df['address2'].fillna('') + ', ' + orders_df['address3'].fillna('')

    # Tickets transformations
    oid_order_id_map = orders_df.set_index('OID')['id'].to_dict()
    tickets_df['id'] = tickets_df.apply(lambda _: generate_uuid(), axis=1)
    tickets_df['order_id'] = tickets_df['OID'].map(oid_order_id_map)
    tickets_df['created'] = tickets_df['utc_timestamp'].apply(convert_unix_to_datetime)
    tickets_df['price'] = (tickets_df['cost'] + tickets_df['fee']).apply(price_to_cents)

    # Drop column after transform done
    tickets_df.drop(columns=['TID', 'OID', 'utc_timestamp', 'cost', 'fee'], inplace=True)
    orders_df.drop(columns=['OID', 'EID', 'cost', 'fee', 'address3', 'country'], inplace=True)
    events_df.drop(columns=['EID'], inplace=True)

    # order columns, that make columns in sql query in order.
    events_df = events_df[event_column]
    orders_df = orders_df[order_column]
    tickets_df = tickets_df[ticket_column]

    return events_df, orders_df, tickets_df


def df_to_sql_insert_on_duplicate_key(df, table_name, filepath, update_flg=False):
    """Function for create SQL insert query"""
    filepath = os.path.join(current_dir, 'output', filepath)
    with open(filepath, 'w+') as file:
        for _, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(
                ['\'' + str(item).replace("'", "''") + '\'' if isinstance(item, str) else str(item) for item in
                 row.values])
            if update_flg:
                updates = ', '.join([f"{col} = VALUES({col})" for col in row.index])
                sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON DUPLICATE KEY UPDATE {updates};\n"
            else:
                sql_statement = f"INSERT INTO {table_name} ({columns}) VALUES ({values});\n"
            file.write(sql_statement)


def df_to_DB(events_df, orders_df, tickets_df):
    """Function for direct insert data to Database"""
    # Create connection
    engine = create_engine('mysql+pymysql://root:12345@localhost/savy_mygrate')

    # Insert to database
    events_df.to_sql('event', con=engine, if_exists='replace', index=False)
    orders_df.to_sql('orders', con=engine, if_exists='replace', index=False)
    tickets_df.to_sql('tickets', con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    # Path to csv source
    orders_path = os.path.join(current_dir, 'input', 'source_orders.csv')
    tickets_path = os.path.join(current_dir, 'input', 'source_tickets.csv')

    events_df, orders_df, tickets_df = gen_df(orders_path, tickets_path)
    # Generate sql insert file or update if exist
    df_to_sql_insert_on_duplicate_key(orders_df, 'orders', 'orders_insert.sql', update_flg=False)
    df_to_sql_insert_on_duplicate_key(tickets_df, 'tickets', 'tickets_insert.sql', update_flg=False)
    df_to_sql_insert_on_duplicate_key(events_df, 'events', 'events_insert.sql', update_flg=False)

    ## Insert direct to DB
    # df_to_DB(events_df, orders_df, tickets_df)

