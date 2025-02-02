import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
from tkinter import simpledialog

class DrawingApp:
    """Приложение для рисования с возможностью выбора цвета и сохранения изображения."""

    def __init__(self, root):
        """
        Инициализация приложения
        :param root: Корневое окно
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.canvas.image = self.photo

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.previous_color = self.pen_color

        self.brush_size = 1
        self.sizes = [1, 2, 5, 10]
        self.size_var = tk.IntVar(value=self.brush_size)

        self.text_entries = []

        self.setup_ui()

        self.root.bind("<Control-s>", self.save_image)
        self.root.bind("<Control-c>", self.choose_color)

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)

    def setup_ui(self):
        """ Настройка пользовательского интерфейса приложения. """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.Y)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        self.color_brush = tk.Label(control_frame, bg=self.pen_color, width=2)
        self.color_brush.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text='Ластик', command=self.mode_eraser)
        eraser_button.pack(side=tk.LEFT)

        drawing_button = tk.Button(control_frame, text="Рисование", command=self.mode_drawing)
        drawing_button.pack(side=tk.LEFT)

        background_color_canvas = tk.Button(control_frame, text="Цвет фона", command=self.change_background_color)
        background_color_canvas.pack(side=tk.LEFT)

        canvas_size = tk.Button(control_frame, text="Размер холста", command=self.resize_canvas)
        canvas_size.pack(side=tk.LEFT)

        self.brush_size_scale = tk.OptionMenu(control_frame, self.size_var, *self.sizes, command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

        self.text_button = tk.Button(control_frame, text="Текст", command=self.add_text)
        self.text_button.pack(side=tk.LEFT)

    def change_background_color(self):
        """
        Изменяет цвет фона, сохраняя все нарисованные объекты.
        """
        selected_color = colorchooser.askcolor(title="Выберите цвет фона")[1]
        if selected_color:
            new_image = Image.new("RGB", self.image.size, selected_color)
            self.draw = ImageDraw.Draw(new_image)
            for text, x, y, color_text in self.text_entries:
                self.draw.text((x, y), text, fill=color_text)
            self.image.paste(new_image, mask=new_image.convert("RGBA"))
            self.draw = ImageDraw.Draw(self.image)
            self.canvas.config(bg=selected_color)
            self.update_canvas()

    def add_text(self):
        """
         Открывает диалоговое окно для ввода текста пользователем. После ввода текста, привязываем обработчик события
         клика мышью для размещения текста на холсте.
        """
        text = tk.simpledialog.askstring("Текст", "Введите текст", parent=self.root)
        if text:
            self.canvas.bind("<Button-1>", lambda event: self.add_text_on_canvas(event, text))

    def add_text_on_canvas(self, event, text):
        """
         Размещает текст на холсте в указанную позицию.
        :param event:  Событие мыши, содержащее координаты X и Y.
        :param text: Текст, который должен быть размещён на холсте.
        :return: None
        """
        x = event.x
        y = event.y

        current_color = self.pen_color
        self.draw.text((x, y), text, fill=current_color)
        self.text_entries.append((text, x, y, current_color))
        self.update_canvas()
        self.canvas.unbind("<Button-1>")

    def update_canvas(self):
        """Обновляет холст с текущим изображением."""
        self.photo.paste(self.image)

    def resize_canvas(self):
        """
        Метод реализующий ввод и изменение размера холста,
        """
        height_canvas = simpledialog.askinteger("Изменение размера", "Введите высоту(положительное число):",
                                                parent=self.root)
        width_canvas = simpledialog.askinteger("Изменение размера", "Введите ширину(положительное число):",
                                               parent=self.root)
        if height_canvas is not None and width_canvas is not None:
            if height_canvas > 0 and width_canvas > 0:
                self.image = Image.new("RGB", (width_canvas, height_canvas), "white")
                self.draw = ImageDraw.Draw(self.image)
                self.canvas.config(width=width_canvas, height=height_canvas)
                self.canvas.pack()
            else:
                messagebox.showwarning("Ошибка", "Ширина и высота должны быть положительными числами")
        else:
            messagebox.showinfo("Информация", "Размер холста не изменен")


    def pick_color(self, event):
        """Получение цвета пикселя под курсором и установка его как текущий цвет пера."""
        x, y = event.x, event.y
        if 0 <= x < self.image.width and 0 <= y < self.image.height:
            color = self.image.getpixel((x, y))
            if isinstance(color, tuple) and len(color) == 3:
                self.pen_color = '#{:02x}{:02x}{:02x}'.format(*color)
            else:
                print("Unexpected pixel format:", color)
        else:
            print("Clicked outside the canvas.")

    def mode_drawing(self):
        """
        Режим рисования, восстанавливает предыдущий цвет пера.
        """
        if self.previous_color:
            self.pen_color = self.previous_color

    def mode_eraser(self):
        """
        Режим ластика, сохраняет текущий цвет, и устанавливает белый цвет(цвет фона)
        """
        self.previous_color = self.pen_color
        self.pen_color = 'white'


    def update_brush_size(self, size):
        """Обновляем текущий размер кисти при выборе нового значения из выпадающего списка.
        :param size: Размер кисти
        """
        self.brush_size = int(size)

    def paint(self, event):
        """
        Обрабатывает событие рисования на холсте.
        Этот метод вызывается при движении мыши с нажатой левой кнопкой.
        Он рисует линию на холсте и обновляет изображение с использованием
        текущего цвета пера и размера кисти
        :param event: Событие, содержащий координаты курсора мыши
        """

        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """Сбрасываем координаты последней точки.
        :param event:  Событие, содержащий координаты курсора мыши
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Очищаем холст и создаем новое изображение."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        """Устанавливает цвет пера.
        :param event: Str, событие, по умолчанию None, что бы функция была универсальной, для вызова в двух случаях:
         Кнопка и сочетания клавиш Ctrl + C.
        """
        color = colorchooser.askcolor(color=self.pen_color)
        current_color = None
        if color[1]:
            self.pen_color = color[1]
            current_color = color[1]
            self.color_brush.config(bg=self.pen_color)

    def save_image(self, event=None):
        """Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
         Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        :param event: Str, событие, по умолчанию None, что бы функция была универсальной, для вызова в двух случаях:
         Кнопка и сочетания клавиш Ctrl + S.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])

        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
