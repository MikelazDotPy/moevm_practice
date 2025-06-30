import json
import random
import sys

from PyQt6 import QtWidgets
from PyQt6.QtCore import QCoreApplication, QLibraryInfo, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow, QProgressDialog

from darwin import Darwin, Creature
from ui import Ui_MainWindow


DEFAULT = {'radius': 10.0, 'square_count': 5, 'generations': 25, 'population_size': 100, 'tournament_size': 2, 'mutation_prob': 0.1, 'crossover_prob': 0.5, 'sigma_deviation': 2.0, 'deviation_coef': 0.5, 'n': 0.25, 'E': 10, 'eps': 0.0, 'c': 2}


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.resize(1400, 750)
        
        self.ui.pushButton_2.clicked.connect(self.on_random_clicked)
        self.ui.pushButton_3.clicked.connect(self.to_first_step)
        self.ui.pushButton_4.clicked.connect(self.to_last_step)
        self.ui.pushButton_5.clicked.connect(self.on_prev_step_clicked)
        self.ui.pushButton_6.clicked.connect(self.on_next_step_clicked)
        self.ui.pushButton_7.clicked.connect(self.on_reset_clicked)
        self.ui.pushButton_8.clicked.connect(self.save_parameters)
        self.ui.pushButton_9.clicked.connect(self.stop_darwin)
        self.ui.pushButton_10.clicked.connect(self.save_adaptation)
        self.ui.pushButton_11.clicked.connect(self.save_circle)
        self.ui.pushButton.clicked.connect(self.on_load_clicked)
        self.ui.spinBox_3.valueChanged.connect(self.change_creation_i)

        self.ui.pushButton_6.setText("Начать")

        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)
        self.ui.spinBox_3.setEnabled(False)


        self.history: list[list[Creature]] = []
        self.darwin = None
        self.darwin_it = None
        self.gen_i = -1
        self.creation_i = 0

    def change_creation_i(self, i):
        self.creation_i = i - 1
        if self.darwin is not None:
            self.set_circle_img(self.history[self.gen_i][self.creation_i])

    def to_first_step(self):
        self.gen_i = 1
        self.on_prev_step_clicked()

    def to_last_step(self):
        progress = QProgressDialog("Идет обработка...", "Отмена", 0, 100, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)  # Блокирует главное окно
        progress.setWindowTitle("Пожалуйста, подождите")
        progress.setAutoClose(True)

        self.gen_i = len(self.history) - 1

        progress.setValue(int(self.gen_i*100/self.darwin.D))

        while self.gen_i < self.darwin.D - 1:
            self.gen_i += 1
            self.history.append(next(self.darwin_it))

            progress.setValue(int(self.gen_i*100/self.darwin.D))
            if progress.wasCanceled():
                break

        progress.setValue(100)

        self.gen_i -= 1
        self.on_next_step_clicked()

    def on_load_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл с параметрами", "", 
            "JSON файлы (*.json);;Все файлы (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    data = json.load(file)
                    self.load_parameters(data)
                    QMessageBox.information(self, "Успех", "Параметры успешно загружены!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def load_parameters(self, params):
        #Параметры задачи
        self.ui.doubleSpinBox.setValue(float(params.get("radius", DEFAULT["radius"])))                     # R
        self.ui.spinBox.setValue(int(params.get("square_count", DEFAULT["square_count"])))                 # K
        
        # Параметры алгоритма
        self.ui.spinBox_2.setValue(int(params.get("generations", DEFAULT["generations"])))                 # N
        self.ui.spinBox_4.setValue(int(params.get("population_size", DEFAULT["population_size"])))         # m
        self.ui.spinBox_5.setValue(int(params.get("tournament_size", DEFAULT["tournament_size"])))         # D
        self.ui.doubleSpinBox_2.setValue(float(params.get("mutation_prob", DEFAULT["mutation_prob"])))     # P_m
        self.ui.doubleSpinBox_4.setValue(float(params.get("crossover_prob", DEFAULT["crossover_prob"])))   # P_c
        self.ui.doubleSpinBox_3.setValue(float(params.get("sigma_deviation", DEFAULT["sigma_deviation"]))) # σ
        self.ui.doubleSpinBox_5.setValue(float(params.get("deviation_coef", DEFAULT["deviation_coef"])))   # α
        self.ui.doubleSpinBox_6.setValue(float(params.get("n", DEFAULT["n"])))                             # n
        self.ui.spinBox_6.setValue(int(params.get("E", DEFAULT["E"])))                                     # E
        self.ui.doubleSpinBox_7.setValue(float(params.get("eps", DEFAULT["eps"])))                         # ε
        self.ui.spinBox_7.setValue(int(params.get("c", DEFAULT["c"])))                                     # c

    def save_adaptation(self):
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите сохранить график?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
    
        if reply == QMessageBox.StandardButton.Yes:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Сохранить график", "", 
                "PNG файлы (*.json);;Все файлы (*)"
            )
            
            if file_name:
                try:
                    if not file_name.endswith(".png"):
                        file_name += ".png"
                    self.ui.label_11.pixmap().save(file_name, "PNG")
                    QMessageBox.information(self, "Успех", "График успешно сохранен!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def save_circle(self):
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите сохранить визуализацию упаковки квадратов в круг?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
    
        if reply == QMessageBox.StandardButton.Yes:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Сохранить визуализацию", "", 
                "PNG файлы (*.json);;Все файлы (*)"
            )
            
            if file_name:
                try:
                    if not file_name.endswith(".png"):
                        file_name += ".png"
                    self.ui.label_10.pixmap().save(file_name, "PNG")
                    QMessageBox.information(self, "Успех", "Визуализация успешно сохранена!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def save_parameters(self):
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите сохранить текущие параметры?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
    
        if reply == QMessageBox.StandardButton.Yes:
            file_name, _ = QFileDialog.getSaveFileName(
                self, "Сохранить параметры", "", 
                "JSON файлы (*.json);;Все файлы (*)"
            )
            
            if file_name:
                params = {
                    "radius": self.ui.doubleSpinBox.value(),
                    "square_count": self.ui.spinBox.value(),
                    "generations": self.ui.spinBox_2.value(),
                    "population_size": self.ui.spinBox_4.value(),
                    "tournament_size": self.ui.spinBox_5.value(),
                    "mutation_prob": self.ui.doubleSpinBox_2.value(),
                    "crossover_prob": self.ui.doubleSpinBox_4.value(),
                    "sigma_deviation": self.ui.doubleSpinBox_3.value(),
                    "deviation_coef": self.ui.doubleSpinBox_5.value(),
                    "n": self.ui.doubleSpinBox_6.value(), 
                    "E": self.ui.spinBox_6.value(),              
                    "eps": self.ui.doubleSpinBox_7.value(),                 
                    "c":  self.ui.spinBox_7.value()

                }
        
                try:
                    if not file_name.endswith(".json"):
                        file_name += ".json"
                    with open(file_name, 'w') as file:
                        json.dump(params, file, indent=4)
                    QMessageBox.information(self, "Успех", "Параметры успешно сохранены!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def generate_random_parameters(self):
        params = {
            # Параметры задачи
            "radius": random.uniform(0.01, 100),  
            "square_count": random.randint(1, 25),      
            
            # Параметры алгоритма
            "generations": random.randint(1, 100),
            "population_size": random.randint(1, 100),
            "tournament_size": random.randint(2, 16), 
            "mutation_prob": random.uniform(0, 1),  
            "crossover_prob": random.uniform(0, 1),
            "sigma_deviation": random.uniform(0, 3),
            "deviation_coef": random.uniform(0, 2),
            "n": random.uniform(0.0, 1.0), 
            "E": random.randint(1, 100),              
            "eps": random.uniform(0, 100),                 
            "c":  random.randint(1, 8)
        }
        return params

    def on_random_clicked(self):
        self.load_parameters(self.generate_random_parameters())
        QMessageBox.information(
            self, 
            "Случайные параметры", 
            "Параметры задачи и алгоритма были сгенерированы случайным образом."
        )

    def on_reset_clicked(self):
        try:
            self.load_parameters(DEFAULT)
            QMessageBox.information(
                self,
                "Сброс параметров",
                "Все параметры были сброшены к значениям по умолчанию."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сбросить параметры: {str(e)}"
            )
            
    def on_prev_step_clicked(self):
        self.gen_i -= 1
        self.set_circle_img(self.history[self.gen_i][0])
        self.set_adaptation_img()
        if self.gen_i == 0:
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_6.setEnabled(True)
    
    def set_circle_img(self, creature: Creature):
        pixmap = QPixmap()
        pixmap.loadFromData(self.darwin.draw_squares_in_circle(creature.h, creature.r, self.gen_i + 1))
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * 0.7),
            int(pixmap.height() * 0.7),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.ui.label_10.setPixmap(scaled_pixmap)
        self.ui.label_10.setMinimumSize(scaled_pixmap.size())
        self.ui.label_10.adjustSize()
        self.ui.label_10.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    def set_adaptation_img(self):
        pixmap = QPixmap()
        pixmap.loadFromData(self.darwin.draw_adaptation(self.history[:self.gen_i + 1]))
        self.ui.label_11.setPixmap(pixmap)
        self.ui.label_11.setMinimumSize(pixmap.size())
        self.ui.label_11.adjustSize()
        self.ui.label_11.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

    def disable_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setEnabled(False)
    
    def enable_layout(self, layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setEnabled(True)

    def stop_darwin(self):
        self.history = []
        self.darwin = None
        self.gen_i = -1
        self.darwin_it = None

        self.ui.spinBox_3.setEnabled(False)

        self.enable_layout(self.ui.gridLayout)
        self.enable_layout(self.ui.gridLayout_2)
        self.enable_layout(self.ui.groupBox.layout())

        self.ui.pushButton_6.setText("Начать")

        self.ui.pushButton_3.setEnabled(False)
        self.ui.pushButton_4.setEnabled(False)
        self.ui.pushButton_5.setEnabled(False)
        self.ui.pushButton_6.setEnabled(True)
        self.ui.pushButton_7.setEnabled(True)
        self.ui.pushButton_9.setEnabled(False)
        self.ui.pushButton_10.setEnabled(False)
        self.ui.pushButton_11.setEnabled(False)
        self.ui.spinBox_3.setEnabled(False)

        self.ui.label_10.setPixmap(QPixmap())
        self.ui.label_11.setPixmap(QPixmap())

    def start_darwin(self):
        self.darwin = Darwin(
            R = self.ui.doubleSpinBox.value(),
            K = self.ui.spinBox.value(),
            N = self.ui.spinBox_4.value(),
            m = self.ui.spinBox_5.value(),
            D = self.ui.spinBox_2.value(),
            P_m = self.ui.doubleSpinBox_2.value(),
            P_c = self.ui.doubleSpinBox_4.value(),
            sigma = self.ui.doubleSpinBox_3.value(),
            alpha = self.ui.doubleSpinBox_5.value(),
            n = self.ui.doubleSpinBox_6.value(),
            E = self.ui.spinBox_6.value(),
            eps = self.ui.doubleSpinBox_7.value(),
            c = self.ui.spinBox_7.value()
        )
        self.gen_i = -1
        self.darwin_it = self.darwin.solve_generator()

        self.ui.spinBox_3.setMaximum(self.darwin.N)
        self.ui.spinBox_3.setEnabled(True)

        self.disable_layout(self.ui.gridLayout)
        self.disable_layout(self.ui.gridLayout_2)
        self.disable_layout(self.ui.groupBox.layout())

        self.ui.pushButton_6.setText("Вперед")

        self.ui.pushButton_4.setEnabled(True)
        self.ui.pushButton_7.setEnabled(False)
        self.ui.pushButton_9.setEnabled(True)
        self.ui.pushButton_10.setEnabled(True)
        self.ui.pushButton_11.setEnabled(True)

    def on_next_step_clicked(self):
        if self.darwin is None:
            self.start_darwin()

        if self.gen_i + 1 == len(self.history):
            self.history.append(next(self.darwin_it))

        self.gen_i += 1
        self.set_circle_img(self.history[self.gen_i][self.creation_i])
        self.set_adaptation_img()

        if self.gen_i + 1 >= self.darwin.D:
            self.ui.pushButton_6.setEnabled(False)
            self.ui.pushButton_4.setEnabled(False)
        if self.gen_i > 0:
            self.ui.pushButton_5.setEnabled(True)
            self.ui.pushButton_3.setEnabled(True)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Упаковка квадратов в круг")
    window.show()
    sys.exit(app.exec())