import requests
import json
from adblockparser import AdblockRules

def extract_ads_from_url(url, adblock_rules):
    # Fetch the HTML content of the web page
    response = requests.get(url)
    html_content = response.text

    # Extract ad information for different resource types
    ads = []
    ads.extend(extract_ads_for_resource(url, html_content, adblock_rules, 'script'))
    ads.extend(extract_ads_for_resource(url, html_content, adblock_rules, 'image'))
    ads.extend(extract_ads_for_resource(url, html_content, adblock_rules, 'stylesheet'))
    ads.extend(extract_ads_for_resource(url, html_content, adblock_rules, 'object'))

    return ads

def extract_ads_for_resource(url, html_content, adblock_rules, resource_type):
    # Apply the adblock_rules to the parsed HTML content for a specific resource type
    options = {resource_type: True}
    matched_elements = adblock_rules._matches(html_content, options, None, None, None)

    # Extract ad information from the matched elements
    ads = []
    for element in matched_elements:
        ad = {
            'url': url,
            'element': '',
            'location': '',
            'text_content': '',
            'class': '',
            'id': '',
            'src': '',
            'parent_tag': '',
            'parent_attributes': {},
            'position': {
                'top': '',
                'left': '',
                'width': '',
                'height': ''
            }
        }
        ads.append(ad)

    return ads

def extract_ads_from_urls_file(file_path, adblock_rules):
    ads_data = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            ads = extract_ads_from_url(url, adblock_rules)
            ads_data.extend(ads)
    return ads_data

# Read the EasyList filter list file into a variable
with open('/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/easylist.txt', 'r') as file:
    el_rules = file.read().splitlines()

# Create an instance of AdblockRules with the EasyList filter rules
adblock_rules = AdblockRules(el_rules)

# Example usage
urls_file = '/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/urls.txt'
ads_data = extract_ads_from_urls_file(urls_file, adblock_rules)

# Write the ad data to a JSON file
output_file = '/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/output.json'
with open(output_file, 'w') as file:
    json.dump(ads_data, file, indent=4)

print("Extraction complete. Ad data written to:", output_file)
