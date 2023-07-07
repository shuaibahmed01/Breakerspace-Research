import json
from adblockparser import AdblockRules

def extract_ad_data(url):
    # Read EasyList rules from the file
    with open('easylist.txt', 'r') as f:
        easylist_rules = f.read().splitlines()

    # Create AdblockRules instance with EasyList rules
    adblock_rules = AdblockRules(easylist_rules)

    # Set the desired matching options
    options = {'script': True, 'image': True, 'stylesheet': True, 'xmlhttprequest': True, 'third-party': True}

    print("here")
    # Match ads on the website using the AdblockRules instance
    if adblock_rules.should_block(url, options):
        # Extract ad data from the matched URL
        print("Matched!")
        ad_data = {
            'url': url,
            'ad_type': 'banner',
            'placement': 'header',
            'text': 'Buy Now!',
            'image': 'https://example.com/ad-image.png',
            # Include any other relevant ad data you want to extract
        }

        return ad_data

    return None

def save_to_json(ad_data_list, filename):
    with open(filename, 'w') as f:
        json.dump(ad_data_list, f, indent=4)

# Example usage
website_url = "https://www.tmz.com/"
ad_data = extract_ad_data(website_url)

if ad_data:
    print("Ad data extracted:")
    print(ad_data)

    ad_data_list = [ad_data]  # If you have multiple ad data, add them to the list
    save_to_json(ad_data_list, 'output.json')
    print("Ad data saved to 'output.json' file.")
else:
    print("No ads found on the website.")
