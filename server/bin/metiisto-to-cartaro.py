#!/usr/bin/env python
################################################################################
import arrow
import mysql.connector
from tinydb import TinyDB
################################################################################
class DataConverter:
    # m_fields and c_fields are lists; **must** be of equal length
    # m fields map into c fields
    def __init__(self, table_name, m_fields, c_fields):
        self.table_name = table_name.lower()
        
        # Metiisto Field Names
        self.m_fields = m_fields
        
        # Cartar Field Names
        self.c_fields = c_fields

        # Connect to MySQL DB
        self.metiisto = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            # database="metiisto_devel"
            database="metiisto_prod"
        )

        # Connect to / Create TinyDB
        self.cartaro = TinyDB(F"./{self.table_name.capitalize()}.json")
        self.cartaro.purge()

    def convert(self):
        cursor = self.metiisto.cursor()

        # Fetch Metiisto data
        fld_str = ",".join(self.m_fields)
        cursor.execute(F"select {fld_str} from {self.table_name} order by created_date")

        record = {}
        count = 0
        for row in cursor:
            mapping = zip(self.c_fields, row)
            for (name, raw_value) in mapping:
                value = raw_value
                if raw_value and name.endswith('_at'):
                    date = arrow.get(raw_value, 'US/Eastern')
                    value = date.timestamp
                elif name.startswith('is_'):
                    value = True if raw_value else False
                
                record[name] = value
                # print(record)

            self.cartaro.insert(record)
            count += 1
            print(F"{self.table_name.capitalize()} - {count}", end="\r")

################################################################################
CONVERSION_MAP = {
    "notes": {
        'metiisto': ('title','body','is_favorite','is_encrypted','created_date','updated_date','deleted_date'),
        'cartaro':  ('title','content','is_favorite','is_encrypted','created_at','updated_at','deleted_at')
    }
}
################################################################################
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert Data from Metiisto to Cartaro')
    parser.add_argument('table', type=str, help='Name of the data table')
    args = parser.parse_args()

    data = CONVERSION_MAP.get(args.table, None)

    if data:
        converter = DataConverter(args.table, data['metiisto'], data['cartaro'])
        converter.convert()
    else:
        print(F"No data conversion implemeted for data table '{args.table}'.")
################################################################################
