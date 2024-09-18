import requests
from bs4 import BeautifulSoup

def fetch_data_from_table(url):
    # Fetch the content of the page
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the document. Status code: {response.status_code}")
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table
    table = soup.find('table')
    if not table:
        raise Exception("Table not found in the document.")
    
    parsed_data = []
    
    # Extract rows and columns from the table, skipping the header row
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 3:
            try:
                x = int(cols[0].text.strip())  # Extract x-coordinate
                char = cols[1].text.strip()    # Extract character
                y = int(cols[2].text.strip())  # Extract y-coordinate
                parsed_data.append((char, x, y))
            except ValueError:
                # Handle any rows where conversion to int fails
                print(f"Skipping invalid row: {cols}")
    
    return parsed_data

def print_grid(data):
    # Find the maximum x and y coordinates to determine the size of the grid
    max_x = max(item[1] for item in data) if data else 0
    max_y = max(item[2] for item in data) if data else 0
    max_x_y = max(max_x, max_y)

    # Create a grid filled with spaces
    grid = [[' ' for _ in range(max_x_y + 1)] for _ in range(max_x_y + 1)]
    
    # print(data)
    empty_row = max_x_y
    # Place each character at its corresponding (x, y) coordinate
    for char, x, y in data:
        # print(max_x_y - x, max_x_y - y, x, y, char)
        empty_row = min(max_x_y - y, empty_row) 
        grid[max_x_y - y][max_x_y - x] = char  # y represents the row, x represents the column
    
    # Print the grid row by row (from top to bottom, y increasing)
    # print("Secret message grid:")
    i = 0
    for row in grid:
        if i < empty_row:
            i += 1
            continue        
        print(''.join(row[::-1])) # Use slicing to reverse the row

def decode_secret_message_from_url(url):
    # Step 1: Fetch and parse the table data
    data = fetch_data_from_table(url)
    
    # Step 2: Print the grid to reveal the secret message
    print_grid(data)

# Example usage
# url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub"
decode_secret_message_from_url(url)
