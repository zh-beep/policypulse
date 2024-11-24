from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse incoming JSON payload
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    # Example: Extract the specific ordinance section to fetch
    section = data.get('section')
    if not section:
        return jsonify({"error": "Section not specified"}), 400

    # Fetch and process the specified section of the Austin Code of Ordinances
    ordinance_text = fetch_ordinance_section(section)
    if not ordinance_text:
        return jsonify({"error": "Section not found"}), 404

    # Return the processed ordinance text
    return jsonify({"section": section, "text": ordinance_text}), 200

def fetch_ordinance_section(section):
    # Base URL of the Austin Code of Ordinances
    base_url = 'https://library.municode.com/tx/austin/codes/code_of_ordinances'

    # Construct the URL for the specific section
    section_url = f'{base_url}?nodeId={section}'

    # Fetch the page content
    response = requests.get(section_url)
    if response.status_code != 200:
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the ordinance text (this may need adjustment based on actual HTML structure)
    ordinance_text = soup.find('div', class_='muni_section').get_text(strip=True)

    return ordinance_text

if __name__ == '__main__':
    app.run(port=5000, debug=True)
