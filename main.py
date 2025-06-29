import os
import sys
import json
import random
from PyQt6.QtCore import QCoreApplication, QLibraryInfo, Qt
from PyQt6 import QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication, QMainWindow
from ui_untitled import Ui_MainWindow 

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Подключаем кнопки
        self.ui.pushButton.clicked.connect(self.on_load_clicked)  # Кнопка "Из файла"
        self.ui.pushButton_2.clicked.connect(self.on_random_clicked) #Кнопка "Случайная генерация"
        self.ui.pushButton_7.clicked.connect(self.on_reset_clicked)  #Кнопка "Сбросить"
        self.ui.pushButton_4.clicked.connect(self.on_run_clicked)    #Кнопка "Выполнить до конца"
        self.ui.pushButton_5.clicked.connect(self.on_prev_step_clicked)  #Кнопка "Назад"
        self.ui.pushButton_6.clicked.connect(self.on_next_step_history_clicked)   #Кнопка "Вперед"
        #self.ui.pushButton_3.clicked.connect()                        #Кнопка "Начать сначала"
        self.ui.pushButton_8.clicked.connect(self.save_parameters)     #Кнопка "Сохранить в файл"
       

        # Инициализация для графика 
        self.init_plot()

    def init_plot(self):
        # Здесь будет инициализация PyQtGraph plot
        
        print("Инициализация области для графика")
        print(self.ui.groupBox_3.size().width(), self.ui.groupBox_3.size().height())
        #self.ui.label_10.setPixmap(QPixmap("test.jpg").scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio))

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
        # Параметры задачи
        self.ui.doubleSpinBox.setValue(float(params.get("radius", 10.0)))            # R
        self.ui.spinBox.setValue(int(params.get("square_count", 3)))                 # K
        
        # Параметры алгоритма
        self.ui.spinBox_2.setValue(int(params.get("generations", 1000)))             # N
        self.ui.spinBox_4.setValue(int(params.get("population_size", 100)))          # m
        self.ui.spinBox_5.setValue(int(params.get("tournament_size", 5)))            # D
        self.ui.doubleSpinBox_2.setValue(float(params.get("mutation_prob", 0.5)))    # P_m
        self.ui.doubleSpinBox_4.setValue(float(params.get("crossover_prob", 0.5)))   # P_c
        self.ui.doubleSpinBox_3.setValue(float(params.get("sigma_deviation", 3.0)))  # σ
        self.ui.doubleSpinBox_5.setValue(float(params.get("deviation_coef", 0.5)))   # α
        self.ui.doubleSpinBox_6.setValue(float(params.get("n", 2.0)))                # n
        self.ui.spinBox_6.setValue(int(params.get("E", 50)))                         # E
        self.ui.doubleSpinBox_7.setValue(float(params.get("eps", 0.01)))             # ε
        self.ui.spinBox_7.setValue(int(params.get("c", 10)))                         # c

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
                    "epsilon": self.ui.doubleSpinBox_7.value(),                 
                    "c":  self.ui.spinBox_7.value()

                }
        
                try:
                    with open(file_name, 'w') as file:
                        json.dump(params, file, indent=4)
                    QMessageBox.information(self, "Успех", "Параметры успешно сохранены!")
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def generate_random_parameters(self):
       #Генерирует случайные параметры задачи и алгоритма"""
        params = {
            # Параметры задачи
            "radius": random.uniform(0.01, 5000.0),  
            "square_count": random.randint(1, 5000),      
            
            # Параметры алгоритма
            "generations": random.randint(0, 1000),
            "population_size": random.randint(0, 1000),
            "tournament_size": random.randint(2, 20), 
            "mutation_prob": random.uniform(0.01, 1.00),  
            "crossover_prob": random.uniform(0.0, 1.0),
            "sigma_deviation": random.uniform(0.0, 1.0),
            "deviation_coef": random.uniform(0.0, 2.0),
            "n": random.uniform(0.0, 1.0), 
            "E": random.randint(1, 100),              
            "epsilon": random.uniform(0.0, 1.0),                 
            "c":  random.randint(1, 100)
        }
        return params

    def on_random_clicked(self):
        # Генерируем случайные параметры
        random_params = self.generate_random_parameters()
        
        # Загружаем их в интерфейс
        self.load_parameters(random_params)
        
        # Показываем сообщение
        QMessageBox.information(
            self, 
            "Случайные параметры", 
            "Параметры задачи и алгоритма были сгенерированы случайным образом."
        )
    
    def reset_parameters(self):
        default_params = {
            # Параметры задачи
            "radius": 10.0,
            "square_count": 3,
            
            # Параметры алгоритма
            "generations": 1000,
            "population_size": 100,
            "tournament_size": 5,
            "mutation_prob": 0.5,
            "crossover_prob": 0.5,
            "sigma_deviation": 3.0,
            "deviation_coef": 0.5,
            "n": 2, 
            "E": 0.5,              
            "epsilon": 0.5,                 
            "c": 10
        }
        self.load_parameters(default_params)

    def on_manual_clicked(self):
        print("Кнопка 'Ручной ввод' нажата")
        # Здесь будет логика для открытия диалога/окна ручного ввода данных
    
    def on_next_clicked(self):
        print("Кнопка 'Следующий шаг' нажата")
        # Здесь будет логика выполнения одного шага ГА
        # Обновление vis_label (отображение лучшего решения)
        # Обновление info_label (стоимость, средняя стоимость)
        # Обновление графика
        # Добавление элемента в history_list_widget
    
    def on_run_clicked(self):
        print("Кнопка 'Выполнить до конца' нажата")
        # Здесь будет логика выполнения ГА до завершения (или заданного числа поколений)
        # Обновление GUI по мере выполнения (или только в конце)
    
    def on_reset_clicked(self):
        try:
            self.reset_parameters()
            
            # Если у вас есть history_list_widget, очищаем его
            if hasattr(self.ui, 'history_list_widget'):
                self.ui.history_list_widget.clear()
            
            # Если есть другие элементы для очистки, добавьте здесь
            
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

    # Новые слоты для второй вкладки
    def on_crossover_type_changed(self, index):
        crossover_type = self.ui.crossover_combo.currentText()
        print(f"Тип кроссовера изменен на: {crossover_type}")
        # Здесь обновить параметр кроссовера для ГА
        
    def on_history_selection_changed(self):
        selected_items = self.ui.history_list_widget.selectedItems()
        if selected_items:
            selected_generation_text = selected_items[0].text()
            print(f"Выбрано поколение: {selected_generation_text}")
            # Здесь будет логика для загрузки и отображения выбранного решения из истории
            # Обновить vis_label и info_label на основе данных этого поколения
            
    def on_prev_step_clicked(self):
        print("Кнопка 'Назад' нажата (история)")
        # Логика для перехода к предыдущему состоянию в истории
        
    def on_next_step_history_clicked(self):
        print("Кнопка 'Вперед' нажата (история)")
        # Логика для перехода к следующему состоянию в истории


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Упаковка квадратов в круг")
    window.show()
    sys.exit(app.exec())