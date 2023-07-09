import json
from adblockparser import AdblockRules

def extract_ad_data_from_har(har_file_path):
    # Read EasyList rules from the file
    with open('/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/easylist.txt', 'r') as f:
        easylist_rules = f.read().splitlines()

    # Create AdblockRules instance with EasyList rules
    adblock_rules = AdblockRules(easylist_rules)
    

    # List to store extracted ad data
    ad_data_list = []

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
                'request_headers': request.get('headers')
            }

            ad_data_list.append(ad_data)

    return ad_data_list


def save_to_json(ad_data_list, filename):
    try:
        with open(filename, 'w') as f:
            json.dump(ad_data_list, f, indent=4)
    except Exception as e:
        print("Error occurred while saving to JSON:", str(e))

# Example usage
har_file_path = 'DentalTown.har'
ad_data_list = extract_ad_data_from_har(har_file_path)

if ad_data_list:
    print("Ad data extracted!")
    # print("Ad data list:", ad_data_list)
    save_to_json(ad_data_list, 'ad_data.json')
    print("Ad data saved to 'ad_data.json' file.")
else:
    print("No ads found in the HAR file.")

