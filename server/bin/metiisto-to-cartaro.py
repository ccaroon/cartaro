#!/usr/bin/env python
################################################################################
import arrow
import mysql.connector
from tinydb import TinyDB
################################################################################
class DataConverter:
    # m_fields and c_fields are lists; **must** be of equal length
    # m fields map into c fields
    def __init__(self, table_name, m_fields, c_fields, options):
        self.table_name = table_name.lower()
        self.opts = options
        
        if len(m_fields) != len(c_fields):
            raise ValueError()
        
        # Metiisto Field Names
        self.m_fields = m_fields
        
        # Cartar Field Names
        self.c_fields = c_fields

        if self.opts.get('has_datestamps', True):
            self.m_fields.extend(['created_date', 'updated_date', 'deleted_date'])
            self.c_fields.extend(['created_at',   'updated_at',   'deleted_at'])

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
        print(F"--- Begin Data Conversion for '{self.table_name}' ---")
        obj_cursor = self.metiisto.cursor()

        # Fetch Metiisto data
        fld_str = ",".join(self.m_fields)
        obj_sql = F"select id,{fld_str} from {self.table_name} order by id"
        print(F"     => {obj_sql}")
        
        tags = {}
        if self.opts.get("has_tags", False):
            tag_class = self.opts['tag_class']
            tag_sql = F"select tagged_object.obj_id, tags.name from tags, tagged_object where obj_class='{tag_class}' and tags.id = tagged_object.tag_id order by obj_id"
            print(F"     => {tag_sql}")

            tag_cursor = self.metiisto.cursor()
            tag_cursor.execute(tag_sql)
            for row in tag_cursor:
                note_id = row[0]
                if note_id not in tags:
                    tags[note_id] = []

                tags[note_id].append(row[1])

        count = 0
        obj_cursor.execute(obj_sql)
        for row in obj_cursor:
            record = {}
            obj_id = row[0]
            # row[0] == DB `id`, skip for mapping
            mapping = zip(self.c_fields, row[1:])
            for (name, raw_value) in mapping:
                value = raw_value
                if raw_value and name.endswith('_at'):
                    date = arrow.get(raw_value, 'US/Eastern')
                    value = date.timestamp
                elif name.startswith('is_'):
                    value = True if raw_value else False
                
                record[name] = value
                # print(record)

            if self.opts.get("has_tags", False):
                record['tags'] = tags.get(obj_id, [])
            
            self.cartaro.insert(record)
            count += 1
            print(F"{self.table_name.capitalize()} - {count}", end="\r")

        print(F"     => Converted {count} records.")

################################################################################
CONVERSION_MAP = {
    "notes": {
        'metiisto': ['title', 'body',    'is_favorite', 'is_encrypted'],
        'cartaro':  ['title', 'content', 'is_favorite', 'is_encrypted'],
        'options': {
            'has_tags': True,
            'tag_class': "Metiisto::Note"
        }
    },
    "tags": {
        'metiisto': ['name'],
        'cartaro':  ['name'],
        'options': {
            'has_datestamps': False
        }
    },
}
################################################################################
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert Data from Metiisto to Cartaro')
    parser.add_argument('table', type=str, help='Name of the data table')
    args = parser.parse_args()

    data = CONVERSION_MAP.get(args.table, None)

    if data:
        converter = DataConverter(args.table, data['metiisto'], data['cartaro'], data.get("options", {}))
        converter.convert()
    else:
        print(F"No data conversion implemeted for data table '{args.table}'.")
################################################################################
