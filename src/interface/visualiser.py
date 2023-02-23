import threading
import time
import tkinter as tk
from tkinter import font, ttk

from src.data import geolocation
from src.interface.theme import Theme


# Returns n scaled to the specified range
def scale(n: int, start1: int, stop1: int, start2: int, stop2: int):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)


class Visualiser(tk.Tk):
    REFRESH_RATE = 1

    def __init__(self, client: geolocation.Client) -> None:
        super().__init__()
        self.title("Digital Horizons LLC - Geolocation Visualiser")
        self.resizable(False, False)

        # Window Variables
        self._state = False
        self._client = client

        # Overwrite Default Tkinter Font
        font_ = font.nametofont("TkDefaultFont")
        font_.configure(family="Roboto", size=12)
        self.option_add("*Font", font_)

        # Overwrite Window Background Colour
        self.style = ttk.Style(self)
        self.configure(background=Theme.BACKGROUND)

        # Tk Display Variables
        self._toggle_button_text = tk.StringVar(value="Start")
        self._client_coordinates = tk.StringVar(value="( - - )  M")

        self._construct()
        self._stylize()
        self._pack()

        # Start Refresh Thread
        threading.Thread(target=self._refresh, daemon=True).start()

    def _construct(self) -> None:
        self._centre_frame = ttk.Frame(self, padding=15)

        self._widgets = [
            tk.Label(self, text="Digital Horizons - Geolocation Visualiser"),
            tk.Canvas(self, width=500, height=500),
            tk.Button(
                self,
                textvariable=self._toggle_button_text,
                width=10,
                command=self._toggle_state,
            ),
            tk.Label(self, textvariable=self._client_coordinates),
        ]

    def _stylize(self) -> None:
        self._widgets[0].configure(
            background=Theme.BACKGROUND,
            foreground=Theme.TEXT,
            font=("Roboto Strong", 14),
        )

        self._widgets[1].configure(
            background=Theme.FOREGROUND,
            highlightbackground="#000000",
        )

        self._widgets[2].configure(
            relief="solid",
            background=Theme.FOREGROUND,
            activebackground=Theme.ACTIVE,
            activeforeground=Theme.TEXT,
            foreground=Theme.TEXT,
        )

        self._widgets[3].configure(background=Theme.BACKGROUND, foreground=Theme.TEXT)

    def _pack(self) -> None:
        self._widgets[0].grid(
            row=0, column=0, columnspan=2, sticky="NESW", padx=5, pady=10
        )
        self._widgets[1].grid(row=1, column=0, columnspan=2, sticky="NESW", padx=5)
        self._widgets[2].grid(row=2, column=0, sticky="W", padx=7, pady=7)
        self._widgets[3].grid(row=2, column=1, sticky="E", padx=7, pady=7)

    def _refresh(self):
        while True:
            if self._state:
                location = self._client.get_location()

                self._client_coordinates.set(f"( {location[0]}, {location[1]} )  M")

                x = scale(location[0], 0, self._client.environment.WIDTH, 0, 500)
                y = scale(location[1], 0, self._client.environment.HEIGHT, 0, 500)

                self._widgets[1].create_oval(
                    x - 6, y - 6, x + 6, y + 6, fill=Theme.ACCENT, outline=Theme.ACCENT
                )

                time.sleep(Visualiser.REFRESH_RATE)

    def _toggle_state(self):
        self._state = not self._state
        self._toggle_button_text.set("Stop" if self._state else "Start")

    def show(self) -> None:
        self.mainloop()
