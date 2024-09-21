import os
import json

dir = 'Song Histories'
out_dir = "out"
headers = "roomName,startTime,songs,songNumber"
separator = '|'
list_separator = '+'

debug_list = False

def csv_format(data,type = None, fm_separator = ','):
    if(type == str):
        return '"{0}"'.format(data) + fm_separator
    else:
        return '{0}'.format(data) + fm_separator

def key_dive(obj):
    if(dict != type(obj)): return ''
    keys_str = ''
    for key in obj.keys():
        sub_obj = obj[key]
        sub_type = type(sub_obj)
        #print(key, sub_type)
        if(list == sub_type and len(sub_obj) > 0):
            if(dict == type(sub_obj[0])):
                longest_key = 0
                longest_key_idx = 0
                for i in range(len(sub_obj)):
                    key_length = len(sub_obj[i].keys())
                    if longest_key != max(longest_key,key_length):
                        longest_key = key_length
                        longest_key_idx = i
                keys_str += key_dive(sub_obj[longest_key_idx])
            else:
                keys_str += csv_format(key,str,separator)
        elif(dict == sub_type): 
            keys_str += key_dive(sub_obj)
        else: 
            keys_str += csv_format(key,str,separator)
    return keys_str

def value_dive(obj,list_sep = '+'):
    value_str = ''
    obj_type = type(obj)
    if dict == obj_type:
        for item in obj:
            if debug_list: #-- for debugging list creation
                if(item == 'songNumber'): print("Song Num:{0}".format(obj[item]))
            value_str += value_dive(obj[item], list_sep)
    elif list == obj_type:
        if debug_list: #-- for debugging list creation
            print('----list merge----') 
        for i in range(len(obj)):
            if(type(obj[i]) == dict):
                value_str += value_dive(obj[i], list_sep)
            else:
                value_str += csv_format(obj[i],str, list_sep) 
        value_str = csv_format(value_str[:-1], fm_separator = separator) 
        if debug_list: #-- for debugging list creation
            print(value_str)
            print("----list merge end----")
    elif str == obj_type:
        value_str += csv_format(obj,str,separator)
    else:
        value_str += csv_format(obj,int,separator)
    return value_str

try:
    os.lstat(out_dir)
except FileNotFoundError:
    os.mkdir(out_dir)

header_text = ''
values_text = ''
dir_list = os.listdir(dir)
for dir_idx in range(len(dir_list)):
    with open(os.path.join(dir,dir_list[dir_idx]), encoding='utf-8') as f:
        print(dir_list[dir_idx])
        history = json.loads(f.read())

    # save csv for each file, so need new headers for every files
    header = key_dive(history)
    header = header[:-1]
    if(len(header_text) == 0):
        header_text = csv_format("round",str,separator) + header

    values = ''
    for song in history['songs']:
        values += separator.join([str(dir_idx+1), history['roomName'], history['startTime']]) + separator
        values += value_dive(song, list_separator)[:-1]
        values += '\n'
    # print(values)
    values_text += values
    

# accumulate outputs in the same file    
with open(os.path.join(out_dir,'amq_history.csv'),"w+",encoding='utf-8') as f:
    f.write(header_text+"\n")
    f.write(values_text+"\n")