import threading
import time
import tkinter as tk
from tkinter import font, ttk

from src.data.geolocation import Client
from src.interface.theme import Theme


class Visualiser(tk.Tk):
    
    REFRESH_RATE = 1

    def __init__(self, client: Client) -> None:
        super().__init__()
        self.title("Digital Horizons LLC - RSSI Distance Visualiser")
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
        self._connection_distance = tk.StringVar(value="-")
        self._connection_details = tk.StringVar(value="N/A    - dBm")
        self._toggle_button_text = tk.StringVar(value="Start")

        self.__construct()
        self.__stylize()
        self.__pack()

        threading.Thread(target=self.__update, daemon=True).start()

    def __construct(self) -> None:
        self._centre_frame = ttk.Frame(self, padding=5)

        self._widgets = [
            tk.Label(self, text="Distance to Beacon"),
            tk.Label(self, textvariable=self._connection_distance),
            tk.Label(self, textvariable=self._connection_details),
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

        # Distance
        self._widgets[1].configure(
            background=Theme.Colour.BACKGROUND,
            foreground=Theme.Colour.TEXT,
            font=("Roboto Strong", 100),
        )

        # Signal Strength
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
        self._widgets[0].grid(row=0, column=0, columnspan=2, padx=300, pady=10)
        self._widgets[1].grid(row=1, column=0, columnspan=2, padx=5, pady=140)
        self._widgets[2].grid(row=2, column=1, sticky="E", padx=10, pady=10)
        self._widgets[3].grid(row=2, column=0, sticky="W", padx=10, pady=10)

    def __update(self) -> None:
        while True:
            if self._state:

                self._client.refresh_devices()
                
                try:
                    connection = self._client.connections[0]
                except IndexError:
                    self._connection_details.set("N/A    - dBm")

                    time.sleep(Visualiser.REFRESH_RATE)
                    continue

                self._connection_distance.set(
                    f"{round(connection.get_distance(), 1)} M"
                )
                self._connection_details.set(
                    f"{connection.BEACON.ID}    {connection.RSSI} dBm"
                )

            time.sleep(Visualiser.REFRESH_RATE)

    def __toggle_state(self) -> None:
        self._state = not self._state
        self._toggle_button_text.set("Stop" if self._state else "Start")

    def show(self) -> None:
        self.mainloop()
