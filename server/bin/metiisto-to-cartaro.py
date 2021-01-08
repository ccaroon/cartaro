#!/usr/bin/env python
################################################################################
import arrow
import mysql.connector
import sys
from tinydb import TinyDB

# In case some Cartaro Code is *needed*
sys.path.append(".")
from cartaro.model.tag import Tag
from cartaro.model.work_day import WorkDay
################################################################################
class DataConverter:
    def __init__(self, m_cfg, c_cfg, options):
        self.m_cfg = m_cfg
        self.c_cfg = c_cfg
        self.opts = options
        
        if len(m_cfg['fields']) != len(c_cfg['fields']):
            raise ValueError()

        if self.opts.get('has_datestamps', True):
            self.m_cfg['fields'].extend(['created_date', 'updated_date', 'deleted_date'])
            self.c_cfg['fields'].extend(['created_at',   'updated_at',   'deleted_at'])

        # Connect to MySQL DB
        self.metiisto = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            # database="metiisto_devel"
            database="metiisto_prod"
        )

        # Connect to / Create TinyDB
        self.cartaro = TinyDB(F"./{self.c_cfg['name']}-dev.json")
        self.cartaro.purge()

    def convert(self):
        print(F"--- Converting Metiisto/{self.m_cfg['name']} to Cartaro/{self.c_cfg['name']} ---")
        obj_cursor = self.metiisto.cursor()

        # Fetch Metiisto data
        fld_str = ",".join(self.m_cfg['fields'])
        obj_sql = F"select id,{fld_str} from {self.m_cfg['name']} order by id"
        if self.opts.get('limit', None):
            obj_sql += F" limit {self.opts['limit']}"
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

                tags[note_id].append(Tag.normalize(row[1]))

        count = 0
        obj_cursor.execute(obj_sql)
        for row in obj_cursor:
            record = {}
            obj_id = row[0]
            # row[0] == DB `id`, skip for mapping
            mapping = zip(self.c_cfg['fields'], row[1:])
            for (name, raw_value) in mapping:
                value = raw_value
                if raw_value and name.endswith('_at'):
                    date = arrow.get(raw_value, 'US/Eastern')
                    value = date.timestamp
                elif name.startswith('is_'):
                    value = True if raw_value else False
                
                transformer = self.opts.get(F"{name}_transformer", None)
                if transformer:
                    value = transformer(value)
                
                # print(F"{name} == {value} - {type(value)}")
                record[name] = value

            if self.opts.get("has_tags", False):
                record['tags'] = tags.get(obj_id, [])

            # Metiisto side does not have TS, Added `created_at` to Cartaro data
            if not self.opts.get('has_datestamps', True):
                record['created_at'] = record['created_at'] if 'created_at' in record else arrow.now().timestamp 
                record['updated_at'] = None
                record['deleted_at'] = None

            self.cartaro.insert(record)
            count += 1
            print(F"{self.m_cfg['name']} - {count}", end="\r")

        print(F"     => Converted {count} records.")

################################################################################
# options
#   * has_tags: Does the object in Metiisto have associated tags?
#   * tag_class: If YES to above, what's the object Metiisto class name (Metiisto::XYZZY)
#   * has_datestampes: Does the object in Metiisto have date/time stamps?
#       - If False, Cartaro object WILL have datestamps & 'created_at' will be NOW.
#   * XYZZY_transformer: For field 'XYZZY', run this function to transform it to Cartaro
################################################################################
# --- TRANSFORMERS ---
#     that are more that 1 liners
# entries.ticket_link
def xform_entries_ticket_link(t_num):
    link = None
    if t_num:
        jira = "https://jira.office.webassign.net"
        if t_num.startswith('DO-') or t_num.startswith('CJ'):
            jira = "https://jira.cengage.com"
        
        link = F"{jira}/browse/{t_num}"
        
    return link

# 0 - normal
# 1 - sick day
# 10 - holiday
# 100 - vacation/pto
def xform_work_day_type(value):
    type = WorkDay.TYPE_NORMAL

    if value == 1:
        type = WorkDay.TYPE_SICK
    elif value == 10:
        type = WorkDay.TYPE_HOLIDAY
    elif value == 100:
        type = WorkDay.TYPE_PTO

    return type

def xform_todos_repeat_duration(value):
    repeat = 0

    if value:
        (count, unit) = value.split()
        count = int(count)
        if unit == 'day':
            repeat = count * 1
        elif unit == 'week':
            repeat = count * 7
        elif unit == 'month':
            repeat = count * 30
        elif unit == 'year':
            repeat = count * 365

    return repeat
################################################################################
CONVERSION_MAP = {
    "countdowns": {
        'metiisto': {
            'name': "countdowns",
            'fields': ['title', 'start_date', 'end_date'],
        },
        'cartaro':  {
            'name': 'CountDowns',
            'fields': ['name', 'start_at', 'end_at'],
        },
        'options': {
            'has_datestamps': False,
            'has_tags': False
        }
    },
    "entries": {
        'metiisto': {
            'name': "entries",
            'fields': ['task_date', 'ticket_num',  'subject', 'description', 'category', 'entry_date'],
        },
        'cartaro':  {
            'name': 'LogEntries',
            'fields': ['logged_at', 'ticket_link', 'subject', 'content',     'category', 'created_at'],
        },
        'options': {
            'has_datestamps': False,
            'has_tags': True,
            'tag_class': "Metiisto::Entry",
            'ticket_link_transformer': xform_entries_ticket_link
        }
    },
    "notes": {
        'metiisto': {
            'name': 'notes',
            'fields': ['title', 'body',    'is_favorite', 'is_encrypted']
        },
        'cartaro':  {
            'name': 'Notes',
            'fields': ['title', 'content', 'is_favorite', 'is_encrypted']
        },
        'options': {
            'has_tags': True,
            'tag_class': "Metiisto::Note"
        }
    },
    "tags": {
        'metiisto': {
            'name': 'tags',
            'fields': ['name']
        },
        'cartaro': {
            'name': 'Tags',
            'fields': ['name']
        },
        'options': {
            'has_datestamps': False,
            'name_transformer': lambda name: Tag.normalize(name)
        }
    },
    "work_days": {
        'metiisto': {
            'name': 'work_days',
            'fields': ['work_date', 'time_in', 'time_out', 'note', 'is_vacation*100+is_holiday*10+is_sick_day as type'],
        },
        'cartaro':  {
            'name': 'WorkDays',
            'fields': ['date',      'time_in', 'time_out', 'note', 'type'],
        },
        'options': {
            'has_datestamps': False,
            'date_transformer': lambda date_str: arrow.get(date_str, 'US/Eastern').timestamp,
            'time_in_transformer': lambda delta:  str(delta)[:4] if len(str(delta)) == 7 else str(delta)[:5],
            'time_out_transformer': lambda delta: str(delta)[:4] if len(str(delta)) == 7 else str(delta)[:5],
            'type_transformer': xform_work_day_type
        }
    },
    'todos': {
        'metiisto': {
            'name': "todos",
            'fields': ['title', 'description', 'priority', 'completed', 'completed_date', 'due_date', 'repeat_duration'],
        },
        'cartaro':  {
            'name': 'Todos',
            'fields': ['title', 'description', 'priority', 'is_complete', 'completed_at', 'due_at', 'repeat'],
        },
        'options': {
            'has_datestamps': False,
            'has_tags': True,
            'tag_class': "Metiisto::Todo",
            'repeat_transformer': xform_todos_repeat_duration
        }
    }
}
################################################################################
def do_conversion(data, args):
    if data:
        options = data.get("options", {})
        if args.limit:
            options['limit'] = args.limit
        
        converter = DataConverter(data['metiisto'], data['cartaro'], options)
        converter.convert()
    else:
        print(F"No data conversion implemeted for '{args.what}' data.")
################################################################################
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Convert Data from Metiisto to Cartaro')
    parser.add_argument('what', type=str, help='What data to convert')
    parser.add_argument('--limit', type=int, help='Only convert `limit` records.')
    args = parser.parse_args()

    if args.what == "all":
        for what, data in CONVERSION_MAP.items():
            do_conversion(data, args)
    else:
        data = CONVERSION_MAP.get(args.what, None)
        do_conversion(data, args)
################################################################################
