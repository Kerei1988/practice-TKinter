###  Задача №1. Реализовать функционал: Выбор размера кисти из списка

     # В конструкторе класса добавили:
        self.brush_size = 1  # Инициализация размера кисти
        self.sizes = [1, 2, 5, 10]  # Предопределенные размеры кисти
        self.size_var = tk.IntVar(value=self.brush_size)  # Переменная для хранения выбранного размера
        
        И обновили атрибут self.brush_size_scale в методе setup_ui, добавив создание выпадающего списка для 
        выбора размера кисти:
        self.brush_size_scale = tk.OptionMenu(control_frame, self.size_var, *self.sizes, command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

     # Добавлен метод update_brush_size, который обновляет значение self.brush_size, 
       когда пользователь выбирает новый размер из выпадающего списка.

     # В методе paint, атрибута self.canvas.create_line обновили параметр width=self.brush_size
       Теперь при рисовании на холсте используется актуальный размер кисти.