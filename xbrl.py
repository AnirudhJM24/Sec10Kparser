from bs4 import BeautifulSoup

# Load the HTML file
with open(r'sec-edgar-filings\ORCL\10-K\0000950170-23-028914\primary-document.html', 'r') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all XBRL elements
xbrl_elements = soup.find_all(name='ix')

# Extract XBRL data
xbrl_data = {}
for element in xbrl_elements:
    # Extract the tag name and text content
    tag_name = element.name
    text_content = element.get_text()
    
    # Store the data in a dictionary
    xbrl_data[tag_name] = text_content

# Print the extracted XBRL data
for tag, content in xbrl_data.items():
    print(f"Tag: {tag}, Content: {content}")