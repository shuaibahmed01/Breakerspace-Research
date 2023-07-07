import requests
from bs4 import BeautifulSoup

def extract_ads_from_url(url):
    # Fetch the HTML content of the web page
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find ad elements based on the <aside> tag
    ad_elements = soup.find_all('script')

    # Extract ad information from the ad elements
    ads = []
    for element in ad_elements:
        ad = {
            'url': url,
            'element': element,
            'text_content': element.get_text(strip=True),
            'class': element.get('class', ''),
            'id': element.get('id', ''),
            'src': element.get('src', ''),
            'parent_tag': element.parent.name,
            'parent_attributes': element.parent.attrs,
            'position': {
                'top': element.get('top', ''),
                'left': element.get('left', ''),
                'width': element.get('width', ''),
                'height': element.get('height', '')
            }
        }
        ads.append(ad)

    return ads

def extract_ads_from_urls_file(file_path):
    ads_data = []
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()
            ads = extract_ads_from_url(url)
            ads_data.extend(ads)
    return ads_data

# Example usage
urls_file = '/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/urls.txt'  # Replace with the path to your URLs text file
output_file = '/Users/shuaibahmed/Gunrock Breakerspace/URL:FL Matching/output.txt'  # Replace with the desired output file path

ads_data = extract_ads_from_urls_file(urls_file)

with open(output_file, 'w') as file:
    for ad in ads_data:
        file.write("URL: {}\n".format(ad['url']))
        file.write("Text Content: {}\n".format(ad['text_content']))
        file.write("Class: {}\n".format(ad['class']))
        file.write("ID: {}\n".format(ad['id']))
        file.write("Src: {}\n".format(ad['src']))
        file.write("Parent Tag: {}\n".format(ad['parent_tag']))
        file.write("Parent Attributes: {}\n".format(ad['parent_attributes']))
        file.write("Position: {}\n".format(ad['position']))
        file.write("--------------------------------------------------\n")

print("Extraction complete. Ad data written to:", output_file)
