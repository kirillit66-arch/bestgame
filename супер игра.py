import tkinter as tk
from tkinter import messagebox
import math
import random

class SuperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игровой Автомат: Крутилка и Рычаг")
        self.root.geometry("450x500")
        self.show_main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_screen()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        
        tk.Label(frame, text="ВЫБЕРИТЕ РЕЖИМ", font=("Arial", 18, "bold")).pack(pady=20)
        
        tk.Button(frame, text="🎡 РЕЖИМ 1: КРУТИЛКА", font=("Arial", 12), width=25, height=2,
                  bg="#f0f0f0", command=self.init_spinner).pack(pady=10)
        
        tk.Button(frame, text="🕹️ РЕЖИМ 2: РЫЧАГ", font=("Arial", 12), width=25, height=2,
                  bg="#f0f0f0", command=self.init_lever).pack(pady=10)

    # --- ЛОГИКА КРУТИЛКИ (С АНИМАЦИЕЙ) ---
    def init_spinner(self):
        self.clear_screen()
        tk.Button(self.root, text="⬅ Меню", command=self.show_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Рисуем колесо с секторами для красоты
        colors = ["#FF5733", "#33FF57", "#3357FF", "#F3FF33", "#FF33F6", "#33FFF6"]
        for i in range(6):
            self.canvas.create_arc(50, 50, 250, 250, start=i*60, extent=60, fill=colors[i], outline="white")
        
        # Центр и стрелка
        self.line = self.canvas.create_line(150, 150, 150, 60, fill="black", width=5, arrow=tk.LAST)
        self.canvas.create_oval(145, 145, 155, 155, fill="black") # Оська
        
        self.angle = 0
        self.speed = 0
        self.is_spinning = False
        
        self.spin_btn = tk.Button(self.root, text="КРУТИТЬ!", font=("Arial", 14, "bold"), 
                                 bg="orange", command=self.start_spin)
        self.spin_btn.pack(pady=20)

    def start_spin(self):
        if not self.is_spinning:
            self.speed = random.uniform(15, 35) # Случайная начальная сила
            self.is_spinning = True
            self.animate_spin()

    def animate_spin(self):
        if self.speed > 0.1:
            self.angle += self.speed
            self.speed *= 0.97 # Коэффициент трения (замедление)
            
            # Считаем координаты кончика стрелки
            rad = math.radians(self.angle)
            x = 150 + 90 * math.sin(rad)
            y = 150 - 90 * math.cos(rad)
            
            self.canvas.coords(self.line, 150, 150, x, y)
            self.root.after(20, self.animate_spin)
        else:
            self.is_spinning = False
            self.speed = 0
            messagebox.showinfo("Стоп!", "Крутилка остановилась!")

    # --- ЛОГИКА РЫЧАГА (ТОТ САМЫЙ) ---
    def init_lever(self):
        self.clear_screen()
        tk.Button(self.root, text="⬅ Меню", command=self.show_main_menu).pack(anchor="nw", padx=10, pady=10)
        
        self.lever_state = "up"
        tk.Label(self.root, text="ТЯНИ РЫЧАГ!", font=("Arial", 16, "bold")).pack(pady=20)
        
        self.lever_btn = tk.Button(self.root, text="  [O]  \n   |   \n   |   ", 
                                   font=("Courier", 24, "bold"), bg="#808080", 
                                   fg="white", command=self.pull_lever)
        self.lever_btn.pack(pady=20)
        
        self.lever_label = tk.Label(self.root, text="Статус: Ожидание", font=("Arial", 12))
        self.lever_label.pack()

    def pull_lever(self):
        if self.lever_state == "up":
            # Анимация нажатия
            self.lever_btn.config(text="   |   \n   |   \n  [O]  ", bg="#2ECC71")
            self.lever_state = "down"
            self.lever_label.config(text="СТАТУС: АКТИВИРОВАНО!", fg="green")
            # Автоматический возврат через 600 мс
            self.root.after(600, self.pull_lever)
        else:
            # Возврат в исходное
            self.lever_btn.config(text="  [O]  \n   |   \n   |   ", bg="#808080")
            self.lever_state = "up"
            self.lever_label.config(text="Статус: Готов", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperGame(root)
    root.mainloop()
