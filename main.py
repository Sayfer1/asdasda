import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.records = []

        self.create_widgets()

    def create_widgets(self):
        # Ввод данных
        frame_input = ttk.Frame(self.root)
        frame_input.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame_input, text="Дата (ГГГГ-MM-ДД):").grid(row=0, column=0, sticky='w')
        self.entry_date = ttk.Entry(frame_input)
        self.entry_date.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Температура (°C):").grid(row=1, column=0, sticky='w')
        self.entry_temp = ttk.Entry(frame_input)
        self.entry_temp.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Описание погоды:").grid(row=2, column=0, sticky='w')
        self.entry_desc = ttk.Entry(frame_input)
        self.entry_desc.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Осадки (да/нет):").grid(row=3, column=0, sticky='w')
        self.var_rain = tk.StringVar()
        ttk.Radiobutton(frame_input, text='Да', variable=self.var_rain, value='да').grid(row=3, column=1, sticky='w')
        ttk.Radiobutton(frame_input, text='Нет', variable=self.var_rain, value='нет').grid(row=3, column=1, sticky='e')

        # Кнопки добавления и сохранения
        frame_buttons = ttk.Frame(self.root)
        frame_buttons.pack(padx=10, pady=10, fill='x')

        btn_add = ttk.Button(frame_buttons, text="Добавить запись", command=self.add_record)
        btn_add.pack(side='left', padx=5)

        btn_save = ttk.Button(frame_buttons, text="Сохранить в JSON", command=self.save_to_json)
        btn_save.pack(side='left', padx=5)

        btn_load = ttk.Button(frame_buttons, text="Загрузить из JSON", command=self.load_from_json)
        btn_load.pack(side='left', padx=5)

        # Таблица для отображения записей
        columns = ('date', 'temp', 'desc', 'rain')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Фильтры
        frame_filter = ttk.Frame(self.root)
        frame_filter.pack(padx=10, pady=10, fill='x')

        ttk.Label(frame_filter, text="Фильтр по дате (ГГГГ-MM-ДД):").grid(row=0, column=0, sticky='w')
        self.filter_date = ttk.Entry(frame_filter)
        self.filter_date.grid(row=0, column=1, padx=5)

        ttk.Label(frame_filter, text="Минимальная температура (°C):").grid(row=0, column=2, sticky='w')
        self.filter_temp = ttk.Entry(frame_filter)
        self.filter_temp.grid(row=0, column=3, padx=5)

        btn_filter = ttk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_clear_filter = ttk.Button(frame_filter, text="Очистить фильтр", command=self.clear_filter)
        btn_clear_filter.grid(row=0, column=5, padx=5)

    def add_record(self):
        date_str = self.entry_date.get()
        temp_str = self.entry_temp.get()
        desc = self.entry_desc.get()
        rain = self.var_rain.get()

        # Проверка данных
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        try:
            temp = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return
        if not desc:
            messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
            return
        if rain not in ('да', 'нет'):
            messagebox.showerror("Ошибка", "Выберите осадки: да или нет.")
            return

        record = {
            'date': date_str,
            'temp': temp,
            'desc': desc,
            'rain': rain
        }
        self.records.append(record)
        self.refresh_tree()
        self.clear_inputs()

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def refresh_tree(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        data = data if data is not None else self.records
        for rec in data:
            self.tree.insert('', 'end', values=(rec['date'], rec['temp'], rec['desc'], rec['rain']))

    def clear_inputs(self):
        self.entry_date.delete(0, tk.END)
        self.entry_temp.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.var_rain.set('')

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены.")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.records = json.load(f)
            self.refresh_tree()

    def apply_filter(self):
        filtered = self.records
        date_filter = self.filter_date.get()
        temp_filter = self.filter_temp.get()

        if date_filter:
            try:
                datetime.strptime(date_filter, '%Y-%m-%d')
                filtered = [rec for rec in filtered if rec['date'] == date_filter]
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат даты для фильтра.")
                return
        if temp_filter:
            try:
                temp_value = float(temp_filter)
                filtered = [rec for rec in filtered if rec['temp'] >= temp_value]
            except ValueError:
                messagebox.showerror("Ошибка", "Температура должна быть числом для фильтра.")
                return
        self.refresh_tree(filtered)

    def clear_filter(self):
        self.filter_date.delete(0, tk.END)
        self.filter_temp.delete(0, tk.END)
        self.refresh_tree()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
