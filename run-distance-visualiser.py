from src.tools.distance.visualiser import Visualiser
from src.data import geolocation

if __name__ == "__main__":
    environment = geolocation.Environment("./src/data/samples/WDC 201.json")
    client = geolocation.Client(environment)

    visualiser = Visualiser(client)
    visualiser.show()
