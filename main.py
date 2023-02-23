import json

from src.data import geolocation
from src.interface.visualiser import Visualiser

if __name__ == "__main__":
    environment = geolocation.Environment("./src/data/samples/environment/10-10.json")
    client = geolocation.Client("51c7759d-6a2a-4c63-a20c-37b59cbdab98", environment)

    with open("./src/data/samples/server/7-2.json", "r") as file:
        client.process_scan(json.load(file))

    visualiser = Visualiser(client)
    visualiser.show()
