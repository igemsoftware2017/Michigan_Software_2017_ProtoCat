import json

class converter():
    def __init__(self):
        pass
    
    def convert_cat_to_io(self, cat_json):
        pass

    def convert_io_to_cat(self, io_json):
        #http://protocat.org/api/protocol/
        cat_json = {}
        if 'protocol_name' in io_json:
            cat_json['title'] = io_json['protocol_name']
        else:
            cat_json['title'] = "Untitled"

        if 'description' in io_json:
            cat_json['description'] = io_json['description']
        else:
            cat_json['description'] = "No Description provided"       
        protocol_url = 'https://www.protocols.io/view/' + io_json['uri']
        cat_json['description'] += '\n\nTaken from <a href=' + protocol_url + '>' + protocol_url + '</a>'

        if 'materials' in io_json and len(io_json['materials']) > 0:
            cat_json['materials'] = "<br/>".join(io_json['materials'])
        else:
            cat_json['materials'] = "No Materials Provided"

        cat_json['protocol_steps'] = []
        step_number = 1
        if 'steps' in io_json:
            for step in io_json['steps']:
                cat_step = {}
                cat_step['step_number'] = step_number
                step_number += 1
                #print(step['components'],'\n####################')
                descr = ""
                for comp in step['components']:
                    if 'name' in comp and comp['name'] == "Description":
                        cat_step['action'] = comp['data']
                        descr = ""
                    elif 'name' in comp and comp['name'] == 'Duration / Timer':
                        cat_step['time'] = comp['data']
                        descr = ""
                    else:
                        try:
                            if step['components'][comp]['name'] == "Description":
                                descr += step['components'][comp]['data']
                            elif step['components'][comp]['name'] == "Protocol":
                                #print(step['components'][comp])
                                descr += " https://www.protocols.io/view/" + step['components'][comp]['source_data']['uri']
                            else:
                                raise Exception
                        except:
                            print("Unknown how to handle this",comp)
                            descr = "Error ocurred while parsing"
                        cat_step['action'] = descr
                if "title" not in cat_step:
                    cat_step['title'] = ""
                if "time" not in cat_step:
                    cat_step['time'] = -1
                if "warning" not in cat_step:
                    cat_step['warning'] = ""
                if "time_scaling" not in cat_step:
                    cat_step['time_scaling'] = 2
                if "reagents" not in cat_step:
                    cat_step['reagents'] = []
                if "action" not in cat_step:
                    cat_step['action'] = ""
                if cat_step['action'][0:2] != "<p>":
                    cat_step['action'] = "<p>" + cat_step['action'] + "</p>"
                cat_json['protocol_steps'].append(cat_step)
            
        cat_json['category'] = None 
        cat_json['change-log'] = ""
        cat_json['previous_revision']: "-1"
        return cat_json
