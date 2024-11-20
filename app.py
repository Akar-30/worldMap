from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def get_country_info(lat, lng, api_key):
    # Get country code from OpenCage API
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            country_code = data['results'][0]['components'].get('country_code')
            if country_code:
                # Get detailed country info from REST Countries API
                country_url = f"https://restcountries.com/v3.1/alpha/{country_code}"
                country_response = requests.get(country_url)
                if country_response.status_code == 200:
                    country_data = country_response.json()[0]
                    country_info = {
                        'name': country_data.get('name', {}).get('official', 'N/A'),
                        'capital': country_data.get('capital', ['N/A'])[0],
                        'population': country_data.get('population', 'N/A'),
                        'area': country_data.get('area', 'N/A'),
                        'region': country_data.get('region', 'N/A'),
                        'languages': ', '.join(country_data.get('languages', {}).values()),
                        'currency': ', '.join([f"{v['name']} ({v['symbol']})" for v in country_data.get('currencies', {}).values()]),
                        'timezones': ', '.join(country_data.get('timezones', []))
                    }
                    return country_info
                else:
                    return "Error retrieving country details"
            else:
                return "Country code not found"
        else:
            return "No results found"
    else:
        return f"Error: {response.status_code}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_country', methods=['GET'])
def get_country():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    api_key = '2b726e98af3e4140b9d67c70c9818a88'
    country_info = get_country_info(lat, lng, api_key)
    return jsonify(country_info)

if __name__ == '__main__':
    app.run(debug=True)