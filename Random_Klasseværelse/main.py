import sys
import random
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QGraphicsView, QGraphicsScene, QFrame, QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QFont, QBrush, QPen
import math


class Seat(QtWidgets.QGraphicsWidget):
    def __init__(self, x, y, size=50):
        super().__init__()

        self.setPos(x, y)
        self.size = size

        self.rect_item = QtWidgets.QGraphicsRectItem(0, 0, size, size, self)
        self.rect_item.setBrush(QtGui.QBrush(QtGui.QColor("#FFC107")))
        self.rect_item.setPen(QtGui.QPen(QtGui.QColor("#8D6E63"), 2))

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.offset = QtCore.QPointF()

        self.label = QtWidgets.QGraphicsSimpleTextItem("", self)
        self.label.setBrush(QBrush(QColor("black")))
        self.label.setFont(QFont("Arial", 10, QFont.Bold))
        self.label.setPos(size / 2 - self.label.boundingRect().width() / 2, size / 2 - self.label.boundingRect().height() / 2)

    def set_label(self, text):
        self.label.setText(text)
        self.label.setPos(self.size / 2 - self.label.boundingRect().width() / 2, self.size / 2 - self.label.boundingRect().height() / 2)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if not self.isSelected():
            return
        move_to = self.mapToParent(event.pos() - self.offset)
        self.setPos(move_to)
        self.scene().update()




class RandomSeatGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window settings
        self.setWindowTitle("Random Classroom Seat Generator")
        self.setGeometry(100, 100, 800, 600)

        # Set the main window background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(245, 245, 245))
        self.setPalette(palette)

        # Main layout
        main_layout = QHBoxLayout()

        # Names input and list layout
        names_layout = QVBoxLayout()
        names_layout.setSpacing(10)

        # Name input
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter name")
        self.name_input.setStyleSheet("border: 1px solid #BDBDBD; padding: 5px;")
        names_layout.addWidget(self.name_input)

        # Add name button
        self.add_name_button = QPushButton("Add Name", self)
        self.add_name_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px;")
        names_layout.addWidget(self.add_name_button)


        self.names_list = QListWidget(self)
        self.names_list.setStyleSheet("border: 1px solid #BDBDBD;")
        names_layout.addWidget(self.names_list)
        self.names_list.itemClicked.connect(self.remove_name_from_list)

    # Random name button
        self.random_name_button = QPushButton("Random Name", self)
        self.random_name_button.setStyleSheet("background-color: #607D8B; color: white; padding: 5px;")
        names_layout.addWidget(self.random_name_button)

        main_layout.addLayout(names_layout)

    # Seating layout
        seating_layout = QVBoxLayout()
        seating_layout.setSpacing(10)

    # Add and remove seat buttons
        seat_buttons_layout = QHBoxLayout()
        self.add_seat_button = QPushButton("Add Seat", self)
        self.add_seat_button.setStyleSheet("background-color: #2196F3; color: white; padding: 5px;")
        seat_buttons_layout.addWidget(self.add_seat_button)
        self.remove_seat_button = QPushButton("Remove Seat", self)
        self.remove_seat_button.setStyleSheet("background-color: #F44336; color: white; padding: 5px;")
        seat_buttons_layout.addWidget(self.remove_seat_button)
        seating_layout.addLayout(seat_buttons_layout)

    # Seating view
        self.seating_view = QGraphicsView(self)
        self.seating_view.setScene(QGraphicsScene(self))
        self.seating_view.setRenderHint(QPainter.Antialiasing)
        self.seating_view.setRenderHint(QPainter.TextAntialiasing)
        self.seating_view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.seating_view.setRenderHint(QPainter.HighQualityAntialiasing)
        self.seating_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.seating_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  
        self.seating_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.seating_view.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.seating_view.setOptimizationFlag(QGraphicsView.DontSavePainterState, True)
        self.seating_view.setFrameShape(QFrame.NoFrame)
        self.seating_view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.seating_view.setInteractive(True)  # added line
        seating_layout.addWidget(self.seating_view)
 
        main_layout.addLayout(seating_layout)

    # Set the main window layout
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Connect signals to slots
        self.add_name_button.clicked.connect(self.add_name)
        self.add_seat_button.clicked.connect(self.add_seat)
        self.remove_seat_button.clicked.connect(self.remove_seat)
        self.random_name_button.clicked.connect(self.select_random_name)

    def add_name(self):
       name = self.name_input.text().strip()
       if name:
        self.names_list.addItem(name)
        self.name_input.clear()

    def add_seat(self):
       size = 50
       x = (self.seating_view.width() - size) / 2
       y = (self.seating_view.height() - size) / 2
       seat = Seat(x, y, size)
       self.seating_view.scene().addItem(seat)

    def remove_seat(self):
       selected_items = self.seating_view.scene().selectedItems()
       if selected_items:
        for item in selected_items:
            self.seating_view.scene().removeItem(item)

    
    def select_random_name(self):
     items = [self.names_list.item(i).text() for i in range(self.names_list.count())]
     seats = [i for i in self.seating_view.scene().items() if isinstance(i, Seat)]
     available_seats = [seat for seat in seats if seat.label.text() == ""]

     if items and available_seats:
        while True:
            selected_name = random.choice(items)
            selected_seat = random.choice(available_seats)

            # Check if the selected name is already on a seat
            name_on_seat = False
            for seat in seats:
                if seat.label.text() == selected_name:
                    name_on_seat = True
                    break

            if not name_on_seat:
                selected_seat.set_label(selected_name)  # Update the label on the seat with the selected name
                break
     else:
        QMessageBox.warning(self, "Random Name", "No names or seats in the list to select from.")


    def remove_name_from_list(self, item):
        self.names_list.takeItem(self.names_list.row(item))





      
if __name__ == "__main__":
    app = QApplication(sys.argv)
    generator = RandomSeatGenerator()
    generator.show()
    sys.exit(app.exec_())


        

            






        




       