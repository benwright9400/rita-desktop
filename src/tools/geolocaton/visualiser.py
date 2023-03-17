import threading
import time
import math
import tkinter as tk
from tkinter import font, ttk

from src.data.geolocation import Client
from src.interface.theme import Theme


# Returns n scaled to the specified range
def scale(n: int, start1: int, stop1: int, start2: int, stop2: int):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)


class Visualiser(tk.Tk):
    
    REFERSH_RATE = 1

    def __init__(self, client: Client) -> None:
        super().__init__()
        self.title("Digital Horizons LLC - Geolocation Visualiser")
        self.resizable(False, False)

        # Window Variables
        self._state = False
        self._client = client

        # Overwrite Default Tkinter Font
        font_ = font.nametofont("TkDefaultFont")
        font_.configure(family="Roboto", size=14)
        self.option_add("*Font", font_)

        # Overwrite Window Background Colour
        self.style = ttk.Style(self)
        self.configure(background=Theme.Colour.BACKGROUND)

        # Tk Display Variables
        self._toggle_button_text = tk.StringVar(value="Start")
        self._geolocation_status = tk.StringVar(value="Inactive")

        self.__construct()
        self.__stylize()
        self.__pack()

        threading.Thread(target=self.__update, daemon=True).start()

    def __construct(self) -> None:
        self._centre_frame = ttk.Frame(self, padding=5)

        self._widgets = [
            tk.Label(self, text="Geolocation Visualiser"),
            tk.Canvas(self, width=500, height=500),
            tk.Label(self, textvariable=self._geolocation_status),
            tk.Button(
                self, textvariable=self._toggle_button_text, command=self.__toggle_state
            ),
        ]

    def __stylize(self) -> None:
        # Titlebar
        self._widgets[0].configure(
            background=Theme.Colour.BACKGROUND,
            foreground=Theme.Colour.TEXT,
            font=("Roboto Strong", 22),
        )

        # Canvas
        self._widgets[1].configure(
            background=Theme.Colour.FOREGROUND,
            highlightbackground="#000000",
        )

        # Geolocation Status
        self._widgets[2].configure(
            background=Theme.Colour.BACKGROUND,
            foreground=Theme.Colour.TEXT,
            font=("Roboto Strong", 20),
        )

        # Toggle Button
        self._widgets[3].configure(
            relief="solid",
            background=Theme.Colour.FOREGROUND,
            activebackground=Theme.Colour.ACTIVE,
            foreground=Theme.Colour.TEXT,
            activeforeground=Theme.Colour.TEXT,
            width=10,
        )

    def __pack(self) -> None:
        self._widgets[0].grid(row=0, column=0, columnspan=2, padx=200, pady=10)
        self._widgets[1].grid(row=1, column=0, columnspan=2, padx=5, pady=20),
        self._widgets[2].grid(row=2, column=1, sticky="E", padx=10, pady=10)
        self._widgets[3].grid(row=2, column=0, sticky="W", padx=10, pady=10)

    def __update(self) -> None:
        while True:
            if self._state:

                time.sleep(1)

                self._client.refresh_devices()
                connections = self._client.connections.copy()

                if len(connections) == 0:
                    self._geolocation_status.set("No Available Connections")
                    continue

                else:
                    self._geolocation_status.set(f"Connections: {len(connections)}")


                self._widgets[1].delete("all")

                for coordinates in [(0, 0), (500, 0), (0, 500), (500, 500)]:

                    distance = connections[0].get_distance()

                    size = math.sqrt(
                        (self._client.environment.WIDTH**2)
                        + (self._client.environment.HEIGHT**2)
                    )
                    radius = scale(distance, 0, size, 0, 500)

                    self._widgets[1].create_oval(
                        coordinates[0] - radius,
                        coordinates[1] - radius,
                        coordinates[0] + radius,
                        coordinates[1] + radius,
                        outline=Theme.Colour.ACCENT,
                        width=3,
                    )

                    connections.pop(0)
                    
                    if len(connections) == 0:
                        break

    def __toggle_state(self) -> None:
        self._state = not self._state
        self._toggle_button_text.set("Stop" if self._state else "Start")
        self._geolocation_status.set("Inactive" if not self._state else "")

    def show(self) -> None:
        self.mainloop()
