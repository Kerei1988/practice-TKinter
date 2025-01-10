import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


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

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.previous_color = self.pen_color

        self.brush_size = 1
        self.sizes = [1, 2, 5, 10]
        self.size_var = tk.IntVar(value=self.brush_size)

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        """ Настройка пользовательского интерфейса приложения. """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)
        print(type(color_button))
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text='Ластик', command=self.mode_eraser)
        eraser_button.pack(side=tk.LEFT)

        drawing_button = tk.Button(control_frame, text="Рисование", command=self.mode_drawing)
        drawing_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.OptionMenu(control_frame, self.size_var, *self.sizes, command=self.update_brush_size)
        self.brush_size_scale.pack(side=tk.LEFT)

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

    def choose_color(self):
        """Устанавливает цвет пера."""
        color = colorchooser.askcolor(color=self.pen_color)
        current_color = None
        if color[1]:
            self.pen_color = color[1]
            current_color = color[1]

    def save_image(self):
        """Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
         Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении."""
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
