import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "f1c00681-0542-4d1d-987c-3a8de6aecc63"

def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        return json_status, lat, lng, name
    else:
        if json_status != 200:
            print(f"Geocode API status: {json_status}\nError message: {json_data['message']}")
        return json_status, "null", "null", location

while True:
    loc1 = input("Ciudad de Origen (o 'q' para salir): ")
    if loc1.lower() == "q":
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ciudad de Destino (o 'q' para salir): ")
    if loc2.lower() == "q":
        break
    dest = geocoding(loc2, key)

    if orig[0] == 200 and dest[0] == 200:
        op = f"&point={orig[1]}%2C{orig[2]}"
        dp = f"&point={dest[1]}%2C{dest[2]}"
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": "car"}) + op + dp
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json()

        if paths_status == 200:
            km = paths_data["paths"][0]["distance"] / 1000
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            rendimiento = float(input("Ingrese el rendimiento del vehículo (km/l): "))
            combustible = km / rendimiento

            print(f"Distancia: {km:.2f} km")
            print(f"Duración del viaje: {hr:02d} horas, {min:02d} minutos, {sec:02d} segundos")
            print(f"Combustible requerido: {combustible:.2f} litros")

            print("Narrativa del viaje:")
            for each in paths_data["paths"][0]["instructions"]:
                path = each["text"]
                distance = each["distance"]
                print(f"{path} ({distance / 1000:.2f} km)")

        else:
            print(f"Error message: {paths_data['message']}")
    else:
        print("Error al obtener datos de geocodificación para una de las ciudades.")
