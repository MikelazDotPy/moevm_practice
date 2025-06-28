import os
import sys
from PyQt6.QtCore import QCoreApplication, QLibraryInfo
from PyQt6 import QtWidgets
# Импортируем обновленный класс Ui_MainWindow
from ui_untitled import Ui_MainWindow 

# Эта строка может быть не нужна в более новых версиях PyQt6, но если возникают ошибки с плагинами, оставьте.
# os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(QLibraryInfo.PluginsPath)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Здесь можно добавить логику для кнопок и других элементо
        # Инициализация для графика (позже здесь будет код для PyQtGraph)
        self.init_plot()

    def init_plot(self):
        # Здесь будет инициализация PyQtGraph plot
        # Для начала просто заглушка
        print("Инициализация области для графика")
        pass

    def on_load_clicked(self):
        print("Кнопка 'Из файла' нажата")
        # Здесь будет логика для открытия диалога выбора файла и загрузки данных
    
    def on_manual_clicked(self):
        print("Кнопка 'Ручной ввод' нажата")
        # Здесь будет логика для открытия диалога/окна ручного ввода данных
    
    def on_random_clicked(self):
        print("Кнопка 'Случайная генерация' нажата")
        # Здесь будет логика для случайной генерации параметров задачи (радиус, количество квадратов)
    
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
        print("Кнопка 'Сбросить' нажата")
        # Здесь будет логика для сброса состояния ГА, очистки графика, визуализации
        self.ui.info_label.setText("Лучшее решение: -\nСтоимость: -\nСредняя стоимость поколения: -")
        self.ui.history_list_widget.clear()

    # Новые слоты для второй вкладки
    def on_crossover_type_changed(self, index):
        crossover_type = self.ui.crossover_combo.currentText()
        print(f"Тип кроссовера изменен на: {crossover_type}")
        # Здесь можно обновить параметр кроссовера для вашего ГА
        
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
    window.show()
    sys.exit(app.exec())