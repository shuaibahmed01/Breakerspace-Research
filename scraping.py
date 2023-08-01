import json
from adblockparser import AdblockRules
import os
import glob

def extract_ad_data_from_har(har_file_path, website_label):
    # Read EasyList rules from the file
    with open('/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/easylist.txt', 'r') as f:
        easylist_rules = f.read().splitlines()

    # Create AdblockRules instance with EasyList rules
    adblock_rules = AdblockRules(easylist_rules)
    

    # List to store extracted ad data
    ad_data_list = []
    header = f"FILE : {website_label}"
    ad_data_list.append(header)

    # Load the HAR file
    with open(har_file_path, 'r') as har_file:
        har_data = json.load(har_file)

    # Loop through all entries in the HAR file
    for entry in har_data['log']['entries']:
        request = entry['request']
        response = entry['response']
        url = request['url']

        resource_type = entry.get('_resourceType')

        # Set the desired matching options
        if resource_type == 'document':
            option = {'document': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'script':
            option = {'script': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'xhr':
            option = {'xmlhttprequest': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'image':
            option = {'image': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'object':
            option = {'object': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'stylesheet':
            option = {'stylesheet': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'elemhide':
            option = {'elemhide': True, 'subdocument': True, 'third-party':True}
        elif resource_type == 'background':
            option = {'background': True, 'subdocument': True, 'third-party':True}
        

        # Match ads on the URL using the AdblockRules instance
        if adblock_rules.should_block(url, option):

            ad_data = {
                'url': url,
                'dimensions': {
                    'width': request.get('width'),
                    'height': request.get('height')
                },
                'mime_type': response.get('content', {}).get('mimeType'),
                'status': response.get('status'),
                'status_text': response.get('statusText'),
                'headers': response.get('headers'),
                'request_headers': request.get('headers'),
            }

            ad_data_list.append(ad_data)

    seperator = '-------------------------------------------------------------------------------------------------------------'
    ad_data_list.append(seperator)

    return ad_data_list


def save_to_json(ad_data_list, filename):
    try:
        if os.path.isfile(filename):
            # Read the existing data from the file
            with open(filename, 'r') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        # Append the new data to the existing data
        existing_data.extend(ad_data_list)
        
        # Write the updated data back to the file
        with open(filename, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        print("Error occurred while saving to JSON:", str(e))

def get_har_file_paths(directory):
    har_files = glob.glob(os.path.join(directory, '*.har'))
    return har_files
    

har_directory = '/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/HAR_files'  
har_file_paths = get_har_file_paths(har_directory)


for har_file_path in har_file_paths:
    website_label = har_file_path
    ad_data_list = extract_ad_data_from_har(har_file_path, website_label)
    
    if ad_data_list:
        print("Ad data extracted from", har_file_path)
        save_to_json(ad_data_list, '100Realt.json')
        print("Ad data saved to 'ad_data.json' file.")
    else:
        print("No ads found in the HAR file", har_file_path)

