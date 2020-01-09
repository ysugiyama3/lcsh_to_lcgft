#! python3
""" replace LCSH in 655 fields with LCGFT equivalent if available """

from pymarc import *
import csv
import re

def create_replace_list():
    with open(in_csv_name, 'r', newline='', encoding='utf-8-sig') as f:
        replace_list_reader = csv.reader(f)
        replace_list = dict()
        for row in replace_list_reader:
            lcsh = row[0].strip().rstrip('\.')  
            lcgft = row[1].strip()
            lcgft_uri = row[2].strip()
            if (lcsh) not in replace_list:
                replace_list.update({lcsh : [lcgft, lcgft_uri]})                        
    f.close()
    return replace_list

def lcsh_genre(field):
    ind1 = str(field)[6]
    ind2 = str(field)[7]
    if re.match(r"\\", str(ind1))and re.match('0', str(ind2)): # if 1st ind is '\' and 2nd ind is '0'
        return True

def lcgft_genre(field):
    ind1 = str(field)[6]
    ind2 = str(field)[7]
    if re.match(r"\\", str(ind1))and re.match('7', str(ind2)): # if 1st ind is '\' and 2nd ind is '7' 
        return True

def create_dup_list():
    dup_list = []
    if record['655'] is not None:
        for each_field in record.get_fields('655'):    
            subfield_a = each_field.get_subfields('a')[0].strip().rstrip('\.')
            try:
                subfield_2 = each_field.get_subfields('2')[0].strip().rstrip('\.')
                if lcgft_genre(each_field) and subfield_2 == 'lcgft':
                    dup_list.append(subfield_a)                
            except:
                pass
    return dup_list
   
def add_lcgft(subfield):
    field = Field(
        tag = '655',
        indicators = [' ','7'],
        subfields = [
        'a', r_list[subfield][0] + '.',
        '2', 'lcgft',
        '0', r_list[subfield][1],
        ])
    record.add_field(field)   
   
def replace_genre():
    if record['655'] is not None:
        for field_655 in record.get_fields('655'):
            note = ''
            sub_655a = field_655.get_subfields('a')[0].strip().rstrip('\.')          
            if lcsh_genre(field_655) and (sub_655a in existing_lcgft_list):
                record.remove_field(field_655)
                note = 'Removed'
            elif lcsh_genre(field_655) and (sub_655a in r_list):
                record.remove_field(field_655)
                add_lcgft(sub_655a)
                note = 'Converted to LCGFT'
                existing_lcgft_list.append(sub_655a)
            if len(note) > 0:
                csv_writer.writerow([bib, field_655, note])
        writer.write(record)

in_csv_name = input('Enter input csv name: ')
in_mrc_name = input('Enter input mrc name: ')
out_csv_name = in_mrc_name[:-4] + "_output.csv"	
out_mrc_name = in_mrc_name[:-4] + "_output.mrc"
writer = MARCWriter(open(out_mrc_name, mode="wb"))
csv_writer = csv.writer(open(out_csv_name, 'w', newline='', encoding='utf-8-sig'), delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
count = 0

r_list = create_replace_list()

with open(in_mrc_name, mode="rb") as fh:

    reader = MARCReader(fh, to_unicode = True)

	# read each record
    for record in reader:
        # See https://groups.google.com/d/msg/pymarc/Q444j3vY8LE/GxvWLQabheAJ
        # Leader position 9 = 'a' for UTF-8
        record.leader = record.leader[0:9] + 'a' + record.leader[10:] 
        bib = record['001'].value()
        existing_lcgft_list = create_dup_list()
        replace_genre()
fh.close()       


