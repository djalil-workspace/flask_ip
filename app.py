from flask import Flask, request, jsonify
import geoip2.database

app = Flask(__name__)

# Загрузка базы данных GeoIP
geoip_reader = geoip2.database.Reader('./GeoLite2-City_20241213/GeoLite2-City.mmdb')

@app.route('/')
def get_extended_client_info():
    ip = request.remote_addr
    geo_data = geoip_reader.city(ip)
    
    client_info = {
        "IP Address": ip,
        "GeoIP": {
            "City": geo_data.city.name,
            "Country": geo_data.country.name,
            "Latitude": geo_data.location.latitude,
            "Longitude": geo_data.location.longitude,
        },
        "User-Agent": request.headers.get('User-Agent'),
        "Accept-Language": request.headers.get('Accept-Language'),
        "Headers": dict(request.headers),
    }
    return jsonify(client_info)

if __name__ == "__main__":
    app.run(debug=True)
