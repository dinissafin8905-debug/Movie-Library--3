import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        
        self.movies = []          # Список фильмов
        self.load_data()          # Загрузка из JSON
        self.create_widgets()     # Создание интерфейса
        self.update_table()       # Обновление таблицы
    
    def create_widgets(self):
        # Заголовок
        Label(self.root, text="МОЯ КИНОТЕКА", 
              font=("Comic Sans MS", 16, "bold"), 
              bg="#2c3e50", fg="#f1c40f").place(x=320, y=10)
        
        # Рамка добавления
        add_frame = Frame(self.root, bg="#34495e", bd=3, relief=GROOVE)
        add_frame.place(x=20, y=50, width=760, height=130)
        
        # Поля ввода
        Label(add_frame, text="Название:", bg="#34495e", fg="white").place(x=20, y=15)
        self.entry_title = Entry(add_frame, width=20)
        self.entry_title.place(x=120, y=12, height=30)
        
        Label(add_frame, text="Жанр:", bg="#34495e", fg="white").place(x=300, y=15)
        self.entry_genre = Entry(add_frame, width=15)
        self.entry_genre.place(x=370, y=12, height=30)
        
        Label(add_frame, text="Год:", bg="#34495e", fg="white").place(x=530, y=15)
        self.entry_year = Entry(add_frame, width=8)
        self.entry_year.place(x=580, y=12, height=30)
        
        Label(add_frame, text="Рейтинг (0-10):", bg="#34495e", fg="white").place(x=20, y=60)
        self.entry_rating = Entry(add_frame, width=8)
        self.entry_rating.place(x=160, y=57, height=30)
        
        # Кнопка добавления
        Button(add_frame, text="ДОБАВИТЬ", command=self.add_movie, 
               bg="#27ae60", fg="white").place(x=600, y=70, width=130, height=40)
        
        # Рамка фильтров
        filter_frame = Frame(self.root, bg="#34495e", bd=3, relief=GROOVE)
        filter_frame.place(x=20, y=190, width=760, height=70)
        
        Label(filter_frame, text="ФИЛЬТРЫ", bg="#34495e", fg="#f1c40f").place(x=20, y=10)
        
        Label(filter_frame, text="По жанру:", bg="#34495e", fg="white").place(x=150, y=12)
        self.filter_genre = Entry(filter_frame, width=15)
        self.filter_genre.place(x=230, y=9, height=30)
        self.filter_genre.bind("<KeyRelease>", lambda e: self.update_table())
        
        Label(filter_frame, text="По году:", bg="#34495e", fg="white").place(x=400, y=12)
        self.filter_year = Entry(filter_frame, width=8)
        self.filter_year.place(x=470, y=9, height=30)
        self.filter_year.bind("<KeyRelease>", lambda e: self.update_table())
        
        Button(filter_frame, text="СБРОСИТЬ", command=self.clear_filters, 
               bg="#e67e22", fg="white").place(x=580, y=8, width=150, height=30)
        
        # Стиль таблицы
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, bg="white", fg="black")
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), bg="#3498db", fg="white")
        
        # Таблица с фильмами
        self.tree = ttk.Treeview(self.root, columns=("Название", "Жанр", "Год", "Рейтинг"), 
                                  show="headings", height=12)
        for col in ["Название", "Жанр", "Год", "Рейтинг"]:
            self.tree.heading(col, text=col)
        self.tree.column("Название", width=300)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=100)
        self.tree.column("Рейтинг", width=100)
        self.tree.place(x=20, y=280, width=760, height=240)
        
        # Кнопка удаления и счётчик
        Button(self.root, text="УДАЛИТЬ", command=self.delete_movie, 
               bg="#e74c3c", fg="white").place(x=350, y=540, width=100, height=40)
        self.counter_label = Label(self.root, text="", bg="#2c3e50", fg="gray")
        self.counter_label.place(x=20, y=540)
    
    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        
        if not title or not genre:
            messagebox.showerror("Ошибка", "Заполните название и жанр!")
            return
        
        # Проверка года
        try:
            year = int(self.entry_year.get())
            if year < 1888 or year > 2026:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Год должен быть числом от 1888 до 2026!")
            return
        
        # Проверка рейтинга
        try:
            rating = float(self.entry_rating.get())
            if rating < 0 or rating > 10:
                raise ValueError
        except:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10!")
            return
        
        # Добавление фильма
        self.movies.append({"title": title, "genre": genre, "year": year, "rating": rating})
        self.save_data()
        
        # Очистка полей
        for entry in [self.entry_title, self.entry_genre, self.entry_year, self.entry_rating]:
            entry.delete(0, END)
        
        self.update_table()
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
    
    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите фильм в таблице!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить этот фильм?"):
            title = self.tree.item(selected[0], "values")[0]
            self.movies = [m for m in self.movies if m["title"] != title]
            self.save_data()
            self.update_table()
            messagebox.showinfo("Успех", "Фильм удалён!")
    
    def update_table(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Получение фильтров
        genre_filter = self.filter_genre.get().strip().lower()
        year_filter = self.filter_year.get().strip()
        
        count = 0
        for movie in self.movies:
            # Фильтр по жанру
            if genre_filter and genre_filter not in movie["genre"].lower():
                continue
            # Фильтр по году
            if year_filter and str(movie["year"]) != year_filter:
                continue
            self.tree.insert("", END, values=(movie["title"], movie["genre"], 
                                              movie["year"], movie["rating"]))
            count += 1
        
        # Обновление счётчика
        self.counter_label.config(text=f"Всего: {len(self.movies)} | Показано: {count}")
    
    def clear_filters(self):
        self.filter_genre.delete(0, END)
        self.filter_year.delete(0, END)
        self.update_table()
    
    def load_data(self):
        if os.path.exists("movies.json"):
            try:
                with open("movies.json", "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "Файл movies.json повреждён! Создан новый файл.")
                self.movies = []
                self.save_data()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")
                self.movies = []
        else:
            self.movies = []
    
    def save_data(self):
        try:
            with open("movies.json", "w", encoding="utf-8") as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

if __name__ == "__main__":
    root = Tk()
    app = MovieLibrary(root)
    root.mainloop()
