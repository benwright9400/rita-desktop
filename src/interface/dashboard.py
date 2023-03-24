import time
import threading

from PyQt6.QtCharts import (
    QChart,
    QChartView,
    QPieSeries,
)
from PyQt6.QtCore import (
    QMargins,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QPainter,
    QPixmap,
    QPen,
)
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QListWidget,
)

from PyQt6.uic import loadUi as QLoader


from src.data.session import Session


class Main(QMainWindow):

    def __init__(self, session: Session) -> None:
        super().__init__()

        self._session = session

        with open("./src/interface/resource/theme.qss", "r") as stylesheet:
            self.setStyleSheet(stylesheet.read())
        QLoader("./src/interface/dashboard.ui", self)

        self.setWindowTitle("Digital Horizons LLC - Presenter Dashboard")
        self.setWindowIcon(QIcon("./src/interface/resource/" + "group-logo.svg"))

        self._chart = PieChart()
        frame = self.findChild(QFrame, "chart_frame").layout()
        frame.addWidget(self._chart, 0, 0)

        title = self.findChild(QLabel, "title")
        title.setText(self._session.title)

        label = self.findChild(QLabel, "slide")
        label.setPixmap(QPixmap("./src/interface/resource/example-slide.png"))

        threading.Thread(target=self.__update, daemon=True).start()

    def __update(self) -> None:
        questions = []

        while True:
            understanding = self._session.get_understanding()

            self._chart.series.slices()[0].setValue(understanding)
            self._chart.series.slices()[1].setValue(100 - understanding)

            self.findChild(QLabel, "legend_label_primary").setText(
                f"{understanding}% Understanding"
            )
            self.findChild(QLabel, "legend_label_secondary").setText(
                f"{100 - understanding}% Not Understanding"
            )

            if self._session.get_questions() != questions:
                questions = self._session.get_questions()

                listwidget = self.findChild(QListWidget, "questions_box")
                listwidget.clear()

                for n in range(min(3, len(questions))):
                    listwidget.addItem(questions[n])

                if len(questions) > 3:
                    self.findChild(QLabel, "questions_footer").setText(f"{len(questions) - 3} others...")
                else:
                    self.findChild(QLabel, "questions_footer").clear()

            time.sleep(1)


class PieChart(QChartView):

    def __init__(self) -> None:
        self._chart = QChart()
        self.series = QPieSeries()

        self._chart.addSeries(self.series)
        self._chart.legend().hide()

        self.series.append("Primary", 50)
        self.series.append("Secondary", 50)

        super().__init__(self._chart)
        self.__stylise()

    def __stylise(self) -> None:
        self._chart.setAnimationOptions(QChart.AnimationOption.AllAnimations)
        self._chart.setBackgroundBrush(QBrush(QColor("transparent")))
        self._chart.setMargins(QMargins(0, 0, 0, 0))

        self.series.slices()[0].setPen(QPen(QColor("#D94C65")))
        self.series.slices()[1].setPen(QPen(QColor("#4C84D9")))

        self.series.slices()[0].setBrush(QColor("#D94C65"))
        self.series.slices()[1].setBrush(QColor("#4C84D9"))

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setContentsMargins(0, 0, 0, 0)
