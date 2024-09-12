import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import datetime
from tasks_controller import handle_add_task, handle_get_tasks, handle_delete_task, handle_update_task, handle_get_statistics
from notifications import schedule_reminders
from export_handler import export_to_csv, export_to_pdf, export_to_excel, export_to_json
from themes import apply_theme
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class TaskPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Planner Pro - Planificator de Sarcini")
        self.root.geometry("1400x800")
        self.root.configure(bg="#f0f4f5")  # Fundal modern, luminos

        # Aplicați tema personalizată
        apply_theme(self.root, "light")

        self.create_sidebar()  # Creăm sidebar-ul pentru navigare
        self.create_widgets()  # Creăm restul interfeței

        # Inițializăm secțiunea de sarcini
        self.load_tasks()
        self.load_statistics()

    def create_sidebar(self):
        # Sidebar pentru navigare
        self.sidebar = tk.Frame(self.root, bg="#333333", width=200, height=800)
        self.sidebar.pack(side="left", fill="y")

        button_font = ("Helvetica", 12)

        # Butoane din sidebar
        dashboard_button = tk.Button(self.sidebar, text="Dashboard", font=button_font, bg="#61dafb", fg="black", command=self.show_dashboard)
        dashboard_button.pack(fill="x", pady=10)

        tasks_button = tk.Button(self.sidebar, text="Sarcini", font=button_font, bg="#61dafb", fg="black", command=self.show_tasks)
        tasks_button.pack(fill="x", pady=10)

        stats_button = tk.Button(self.sidebar, text="Statistici", font=button_font, bg="#61dafb", fg="black", command=self.show_stats)
        stats_button.pack(fill="x", pady=10)

        settings_button = tk.Button(self.sidebar, text="Setări", font=button_font, bg="#61dafb", fg="black", command=self.show_settings)
        settings_button.pack(fill="x", pady=10)

    def show_dashboard(self):
        self.clear_main_area()

        dashboard_label = tk.Label(self.main_area, text="Toate Sarcinile (Ordine Cronologică)", font=("Helvetica", 24, "bold"))
        dashboard_label.pack(pady=20)

        # Obținem sarcinile din baza de date
        tasks = handle_get_tasks()
        
        # Sortăm sarcinile în ordine cronologică în funcție de `due_date`
        tasks_sorted = sorted(tasks, key=lambda x: x[5])  # x[5] este `due_date`

        # Afișăm fiecare sarcină cu butoane pentru completare și ștergere
        for task in tasks_sorted:
            self.display_task_in_dashboard(task)

    def display_task_in_dashboard(self, task):
        task_frame = tk.Frame(self.main_area, bg="#f0f4f5", bd=1, relief="solid")
        task_frame.pack(fill="x", padx=10, pady=5)

        # Informații despre sarcină
        task_title = tk.Label(task_frame, text=f"{task[1]} - Data limită: {task[5]}", font=("Arial", 14), bg="#f0f4f5")
        task_title.pack(side="left", padx=10)

        # Buton pentru marcarea sarcinii ca "completată"
        complete_button = tk.Button(task_frame, text="Completează", font=("Arial", 12), bg="#28a745", fg="white", command=lambda t=task: self.mark_task_complete(t))
        complete_button.pack(side="right", padx=10)

        # Buton pentru ștergerea sarcinii
        delete_button = tk.Button(task_frame, text="Șterge", font=("Arial", 12), bg="#dc3545", fg="white", command=lambda t=task: self.delete_task(t))
        delete_button.pack(side="right", padx=10)

    def mark_task_complete(self, task):
        # Actualizăm sarcina ca fiind completată
        task_id = task[0]  # ID-ul sarcinii
        handle_update_task(task_id, task[1], task[2], task[3], task[4], task[5], task[6], "Finalizat")
        messagebox.showinfo("Sarcină Completată", f"Sarcina '{task[1]}' a fost completată.")
        self.show_dashboard()  # Reîncărcăm dashboard-ul

    def delete_task(self, task):
        task_id = task[0]  # ID-ul sarcinii
        handle_delete_task(task_id)
        messagebox.showinfo("Ștergere Sarcină", f"Sarcina '{task[1]}' a fost ștearsă.")
        self.show_dashboard()  # Reîncărcăm dashboard-ul

    def show_tasks(self):
        self.clear_main_area()
        task_label = tk.Label(self.main_area, text="Lista Sarcinilor", font=("Helvetica", 24, "bold"))
        task_label.pack(pady=20)

        # Sarcinile vor fi afișate aici cu posibilitatea de a le vizualiza sau modifica
        tasks = handle_get_tasks()
        for task in tasks:
            self.display_task_in_dashboard(task)

    def show_stats(self):
        self.clear_main_area()

        stats_label = tk.Label(self.main_area, text="Statistici", font=("Helvetica", 24, "bold"))
        stats_label.pack(pady=20)

        # Grafic cu starea sarcinilor (finalizate vs. în curs)
        stats = handle_get_statistics()
        labels = ['Finalizate', 'În curs']
        sizes = [stats["completed_tasks"], stats["pending_tasks"]]
        colors = ['#28a745', '#ffc107']
        explode = (0.1, 0)  # Se evidențiază sarcinile finalizate

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')  # Asigurăm că cercul este rotund

        canvas = FigureCanvasTkAgg(fig, master=self.main_area)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def show_settings(self):
        self.clear_main_area()

        settings_label = tk.Label(self.main_area, text="Setări Aplicație", font=("Helvetica", 24, "bold"))
        settings_label.pack(pady=20)

        # Adăugăm opțiuni pentru modificarea temei aplicației
        theme_label = tk.Label(self.main_area, text="Schimbă Tema", font=("Helvetica", 18))
        theme_label.pack(pady=10)

        # Dropdown pentru selectarea temei
        self.theme_combo = ttk.Combobox(self.main_area, values=["light", "dark", "colorful"], font=("Arial", 14))
        self.theme_combo.pack(pady=10)
        self.theme_combo.current(0)

        # Buton pentru aplicarea temei
        apply_theme_button = tk.Button(self.main_area, text="Aplică Tema", font=("Helvetica", 12, "bold"), bg="#28a745", fg="white", command=self.apply_theme_change)
        apply_theme_button.pack(pady=10)

    def apply_theme_change(self):
        selected_theme = self.theme_combo.get()
        apply_theme(self.root, selected_theme)

    def clear_main_area(self):
        # Ștergem toate elementele din zona principală pentru a afișa secțiunea dorită
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def create_widgets(self):
        # Zonă principală pentru conținut (se actualizează în funcție de secțiunea selectată)
        self.main_area = tk.Frame(self.root, bg="#ffffff")
        self.main_area.pack(side="right", expand=True, fill="both")

        # Inițial afișăm secțiunea sarcini
        self.create_task_area()

    def create_task_area(self):
        label_font = ("Helvetica", 14)
        button_font = ("Helvetica", 12, "bold")

        # Panou de control pentru adăugare sarcini
        control_frame = tk.Frame(self.main_area, bg="#f0f4f5")
        control_frame.pack(pady=20)

        tk.Label(control_frame, text="Titlu:", font=label_font, bg="#f0f4f5").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(control_frame, font=("Arial", 14))
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Categorie:", font=label_font, bg="#f0f4f5").grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = tk.Entry(control_frame, font=("Arial", 14))
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Subcategorie:", font=label_font, bg="#f0f4f5").grid(row=2, column=0, padx=5, pady=5)
        self.subcategory_entry = tk.Entry(control_frame, font=("Arial", 14))
        self.subcategory_entry.grid(row=2, column=1, padx=5, pady=5)

        # Calendar pentru selecția datei
        tk.Label(control_frame, text="Data limită:", font=label_font, bg="#f0f4f5").grid(row=3, column=0, padx=5, pady=5)
        self.calendar = Calendar(control_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.grid(row=3, column=1, padx=5, pady=5)

        # Selectarea orei
        tk.Label(control_frame, text="Ora (HH:MM):", font=label_font, bg="#f0f4f5").grid(row=4, column=0, padx=5, pady=5)
        self.hour_combo = ttk.Combobox(control_frame, values=[f"{i:02d}" for i in range(24)], font=("Arial", 14), width=3)
        self.hour_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.minute_combo = ttk.Combobox(control_frame, values=[f"{i:02d}" for i in range(60)], font=("Arial", 14), width=3)
        self.minute_combo.grid(row=4, column=1, padx=5, pady=5, sticky="e")

        tk.Label(control_frame, text="Prioritate:", font=label_font, bg="#f0f4f5").grid(row=5, column=0, padx=5, pady=5)
        self.priority_combo = ttk.Combobox(control_frame, values=["Scăzută", "Medie", "Ridicată"], font=("Arial", 14))
        self.priority_combo.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Stare:", font=label_font, bg="#f0f4f5").grid(row=6, column=0, padx=5, pady=5)
        self.status_combo = ttk.Combobox(control_frame, values=["În curs", "Finalizat"], font=("Arial", 14))
        self.status_combo.grid(row=6, column=1, padx=5, pady=5)

        add_button = tk.Button(control_frame, text="Adaugă Sarcină", font=button_font, bg="#28a745", fg="white", command=self.add_task)
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

    def load_tasks(self):
        # Aici vom încarca și afișa sarcinile
        pass

    def load_statistics(self):
        # Afișăm statisticile sarcinilor
        pass

    def add_task(self):
        title = self.title_entry.get()
        category = self.category_entry.get()
        subcategory = self.subcategory_entry.get()
        due_date = self.calendar.get_date()  # Se selectează data din calendar
        hour = self.hour_combo.get()  # Se selectează ora din combobox
        minute = self.minute_combo.get()  # Se selectează minutele din combobox

        # Construim data limită (due_date_time) folosind data și ora selectate
        due_date_time = f"{due_date} {hour}:{minute}:00"

        # Validăm formatul datei
        try:
            datetime.datetime.strptime(due_date_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            messagebox.showerror("Eroare", "Formatul datei sau orei este incorect!")
            return

        priority = self.priority_combo.get()  # Obținem prioritatea din combobox
        status = self.status_combo.get()  # Obținem starea din combobox

        if not title or not category:
            messagebox.showwarning("Eroare", "Titlul și categoria sunt obligatorii!")
            return

        # Adăugăm sarcina în baza de date
        handle_add_task(title, None, category, subcategory, due_date_time, priority, status, None)
        self.load_tasks()
        self.load_statistics()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskPlannerApp(root)
    root.mainloop()
