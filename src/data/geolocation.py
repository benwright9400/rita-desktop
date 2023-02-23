import json
import uuid
import requests

from src.data import trigonometry


def round_tuple(tuple: tuple) -> tuple:
    return (round(tuple[0]), round(tuple[1]))


class Beacon:
    def __init__(self, UUID: str, factor: int, x: int, y: int) -> None:
        self.UUID = uuid.UUID(UUID)
        self.MEASURED_POWER = factor

        self.x, self.y = x, y

    @staticmethod
    def sort(element: object) -> str:
        return str(element.x) + str(element.y)


class Environment:
    def __init__(self, filepath: str) -> None:
        with open(filepath, "r") as file:
            config = json.load(file)

        self.UUID = config["UUID"]
        self.NAME = config["name"]

        if len(config["beacons"]) > 4:
            raise ValueError("Beacon Limit Exceeded (Max 4)")

        self.BEACONS = [Beacon(*beacon.values()) for beacon in config["beacons"]]
        self.BEACONS.sort(key=Beacon.sort)

        self.WIDTH = max([beacon.x for beacon in self.BEACONS])
        self.HEIGHT = max([beacon.y for beacon in self.BEACONS])


class Connection:
    RSSI_MIN = -120
    RSSI_MAX = 10

    def __init__(self, beacon: Beacon, RSSI: float) -> None:
        self.BEACON = beacon

        if Connection.RSSI_MIN < RSSI < Connection.RSSI_MAX:
            self.RSSI = RSSI
        else:
            raise ValueError("Invalid RSSI Range")

    # Returns connection distance in Metres
    def get_distance(self) -> float:
        distance = 10 ** ((self.BEACON.MEASURED_POWER - self.RSSI) / (10 * 2))
        return round(distance, 1)

    @staticmethod
    def sort(element: object) -> str:
        return Beacon.sort(element.BEACON)


class Client:

    SERVER_URL = "https://rita-server.herokuapp.com/student?="

    def __init__(self, UUID: str, environment: Environment) -> None:
        self.UUID = uuid.UUID(UUID)
        self.environment = environment

        self.connections = []

    # Collects and processes the list of a available devices
    def get_devices(self) -> None:
        request = requests.get(
            f"https://rita-server.herokuapp.com/student?={str(self.UUID)}"
        )
        devices = json.loads(request.text)

        self.connections.clear()

        for device in devices:
            for beacon in self.environment.BEACONS:
                if device["UUID"] == str(beacon.UUID):
                    self.connections.append(Connection(beacon, device["RSSI"]))

        self.connections.sort(key=Connection.sort)

    # Returns a list of client connections
    def get_status(self) -> str:
        string = ""
        for connection in self.connections:
            string += "Beacon {} ({}, {}) -> {} M".format(
                connection.BEACON.UUID,
                connection.BEACON.x,
                connection.BEACON.y,
                connection.get_distance(),
            )
            string += "\n"
        return string[:-1]

    # Returns the client location based on available beacons
    def get_location(self) -> tuple:
        if len(self.connections) < 2:
            raise ConnectionError("Insufficant Beacon Connection")

        scanned_beacons = []
        coordinates = []

        for a in self.connections:
            for b in self.connections:
                if a.BEACON.UUID == b.BEACON.UUID:
                    continue

                elif b.BEACON.UUID in scanned_beacons:
                    continue

                if a.BEACON.y == b.BEACON.y:
                    result = trigonometry.get_reference(
                        abs(a.BEACON.x - b.BEACON.x),
                        a.get_distance(),
                        b.get_distance(),
                    )

                    if a.BEACON.y == self.environment.HEIGHT:
                        result = (result[0], self.environment.HEIGHT - result[1])

                elif a.BEACON.x == b.BEACON.x:
                    result = trigonometry.get_reference(
                        abs(a.BEACON.y - b.BEACON.y),
                        a.get_distance(),
                        b.get_distance(),
                    )

                    result = (result[1], result[0])

                    if a.BEACON.x == self.environment.WIDTH:
                        result = (self.environment.WIDTH - result[0], result[1])

                else:
                    continue

                # print(
                #     f"Op: {(a.BEACON.x, a.BEACON.y)}, {(b.BEACON.x, b.BEACON.y)} -> {round_tuple(result)}"
                # )

                coordinates.append(result)
                scanned_beacons.append(a.BEACON.UUID)

        x, y = 0, 0
        for item in coordinates:
            x += item[0]
            y += item[1]

        return round_tuple((x / len(coordinates), y / len(coordinates)))
