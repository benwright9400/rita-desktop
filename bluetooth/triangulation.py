import json
import math
import uuid as unique


class Beacon:

    def __init__(self, UUID: str, factor: int, x: int, y: int) -> None:
        self.UUID = unique.UUID(UUID)

        self.MEASURED_POWER = factor
        self.x, self.y = x, y

    def get_position(self) -> tuple:
        return (self.x, self.y)


class Stage:

    FACTOR = 2

    def __init__(self, filepath: str) -> None:
        with open(filepath, "r") as file:
            config = json.load(file)

        self.UUID = config["UUID"]
        self.NAME = config["name"]

        self.BEACONS = [Beacon(*beacon.values())
                        for beacon in config["beacons"]]


class Connection:

    RSSI_MIN = -120
    RSSI_MAX = 10

    def __init__(self, beacon: Beacon, RSSI: int) -> None:
        self.beacon = beacon
        self.RSSI = RSSI

    # Returns the distance between the client and beacon in M
    def get_distance(self, factor: int) -> float:
        if Connection.RSSI_MIN < self.RSSI < Connection.RSSI_MAX:
            return 10 ** ((self.beacon.MEASURED_POWER - self.RSSI) / (10 * factor))
        else:
            raise ValueError("Invalid RSSI Range")


class Client:

    def __init__(self, UUID: str) -> None:
        self.UUID = unique.UUID(UUID)

        self._connections = []
        self._stage = None

    # Assign a stage to the client
    def assign(self, stage: Stage) -> None:
        self._stage = stage

    # Process the results of a BLE scan
    def process_scan(self, devices: list) -> None:
        if self.stage is None:
            raise ConnectionError("No Assigned Stage")

        self._connections.clear()

        for device in devices:
            for beacon in self.stage.BEACONS:
                if device["UUID"] == str(beacon.UUID):
                    self._connections.append(
                        Connection(beacon, device["RSSI"]))

    # Returns the users coordinates
    def get_location(self) -> tuple:
        if len(self._connections) < 2:
            raise ConnectionError(f"Insufficiant Beacon Connections")

        coordinates = []
        for a in self._connections:
            for b in self._connections:
                if a.beacon.UUID == b.beacon.UUID:
                    continue
                elif a.beacon.x == b.beacon.x:
                    result = Client.triangulate(
                        a.beacon.y, b.beacon.y, a.get_distance(Stage.FACTOR), b.get_distance(Stage.FACTOR))
                    coordinates.append(result)

                elif a.beacon.y == b.beacon.y:
                    result = Client.triangulate(
                        a.beacon.x, b.beacon.x, a.get_distance(Stage.FACTOR), b.get_distance(Stage.FACTOR))
                    coordinates.append(result)

        return Client.average_coordinates(coordinates)
    
    @staticmethod
    def average_coordinates(coords: list):
        return tuple(map(lambda x: sum(x) / len(x), zip(*coords)))

    @classmethod
    def triangulate(cls, a: int, b: int, l1: int, l2: int) -> tuple:
        x = ((l1 ** 2) - (l2 ** 2) + (b ** 2) - (a ** 2)) / (2 * (b - a))
        y = math.sqrt((l1 ** 2) - ((x - a) ** 2))
        return (x, y)


if __name__ == "__main__":
    stage = Stage("./bluetooth/stage.json")

    client = Client("becbd811-938d-4c22-ad1b-e154a10f4539")
    client.stage = stage

    import time

    while True:
        with open("./bluetooth/scan.json") as file:
            client.process_scan(json.load(file))

        for i, connection in enumerate(client._connections):
            print("Beacon", i, "->",
                  round(connection.get_distance(Stage.FACTOR), 2), "M")

        print("-" * 50)

        print(client.get_location())

        print("#" * 50)
        time.sleep(1)
