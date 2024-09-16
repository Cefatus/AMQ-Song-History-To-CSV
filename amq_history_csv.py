import os
import json

dir = 'Song Histories'
out_dir = "out"
headers = "roomName,startTime,songs,songNumber"
separator = '|'

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
                keys_str += '"{0}"{1}'.format(key,separator)
        elif(dict == sub_type): 
            keys_str += key_dive(sub_obj)
        else: 
            keys_str += '"{0}"{1}'.format(key, separator)
    return keys_str

def value_dive(obj):
    value_str = ''
    obj_type = type(obj)
    if dict == obj_type:
        for item in obj:
            # if(item == 'songNumber'): print("Song Num:{0}".format(obj[item])) #-- for debugging list creation
            value_str += value_dive(obj[item])
    elif list == obj_type:
        # print('----list merge----') #-- for debugging list creation
        for i in range(len(obj)):
            if(type(obj[i]) == dict):
                value_str += value_dive(obj[i])
            else:
                value_str += '"{0}"+'.format(obj[i])
        value_str = '{0}'.format(value_str[:-1])+ separator
        # print(value_str) #-- for debugging list creation
        # print("----list merge end----") #-- for debugging list creation
    elif str == obj_type:
        value_str += '"{0}"{1}'.format(obj,separator)
    else:
        value_str += '{0}{1}'.format(obj,separator)
    return value_str

if(os.lstat(out_dir) is None):
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
        header_text = "round"+separator+header

    values = ''
    for song in history['songs']:
        values += '{3}{2}"{0}"{2}"{1}"'.format(history['roomName'],history['startTime'],separator,dir_idx+1)+separator
        values += value_dive(song)[:-1]
        values += '\n'
    # print(values)
    values_text += values
    

# accumulate outputs in the same file    
with open(os.path.join(out_dir,'amq_history.csv'),"w+",encoding='utf-8') as f:
    f.write(header_text+"\n")
    f.write(values_text+"\n")