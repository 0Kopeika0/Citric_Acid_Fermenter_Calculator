import tkinter as tk
from tkinter import ttk, messagebox

class BioreactorCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Расчет ферментера для лимонной кислоты")
        self.root.geometry("1300x800")
        
        # Основные переменные
        self.default_values = {
            'r_max': '0.000139', 'C_0': '37.0', 'C_k': '5.0', 'C_us': '1.0',
            'C_pm': '10.0', 'alpha': '1.2', 'omega': '0.9', 'G_0': '0.0231',
            'phi_g': '0.7', 'g_k': '2.0', 'rho_air': '1.14', 'y_n': '0.21',
            'v_air': '0.04', 'K_p': '35.0', 'dH_r': '16800.0', 'rho_nutrient': '1062.0',
            'c_p_nutrient': '4684.0', 'dT_nutrient': '4.0', 'dT_water': '7.0',
            'K_heat': '930.0', 'T_reaction': '309.0', 'T_water_in': '293.0'
        }
        
        self.results = {}
        self.create_widgets()
        self.load_example()
    
    def create_widgets(self):
        # Заголовок
        title_frame = ttk.Frame(self.root, padding=10)
        title_frame.pack(fill='x')
        ttk.Label(title_frame, text="РАСЧЕТ ФЕРМЕНТЕРА ДЛЯ ПРОИЗВОДСТВА ЛИМОННОЙ КИСЛОТЫ", 
                 font=('Arial', 14, 'bold')).pack()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # ВЕРХНЯЯ ЧАСТЬ - ИСХОДНЫЕ ДАННЫЕ
        input_frame = ttk.LabelFrame(main_frame, text="ИСХОДНЫЕ ДАННЫЕ", padding=15)
        input_frame.pack(fill='x', pady=(0, 10))
        
        # Создаем сетку исходных данных
        self.create_input_grid(input_frame)
        
        # СРЕДНЯЯ ЧАСТЬ - ТЕПЛОВЫЕ ПАРАМЕТРЫ
        thermal_frame = ttk.LabelFrame(main_frame, text="ТЕПЛОВЫЕ ПАРАМЕТРЫ", padding=15)
        thermal_frame.pack(fill='x', pady=(0, 10))
        
        # Создаем сетку тепловых параметров
        self.create_thermal_grid(thermal_frame)
        
        # НИЖНЯЯ ЧАСТЬ - РЕЗУЛЬТАТЫ
        results_frame = ttk.LabelFrame(main_frame, text="РЕЗУЛЬТАТЫ РАСЧЕТА", padding=15)
        results_frame.pack(fill='both', expand=True)
        
        # Создаем Treeview для отображения результатов
        self.create_results_tree(results_frame)
        
        # Панель управления
        self.create_control_panel()
    
    def create_input_grid(self, parent):
        """Создает сетку исходных данных"""
        
        # Разделяем параметры на группы
        param_groups = [
            ("КИНЕТИЧЕСКИЕ ПАРАМЕТРЫ", [
                ('r_max', 'Макс. скорость роста r_max', 'с⁻¹'),
                ('C_0', 'Начальная концентрация C₀', 'кг/м³'),
                ('C_k', 'Конечная концентрация Cₖ', 'кг/м³'),
                ('C_us', 'Концентрация C_ус', 'кг/м³'),
                ('C_pm', 'Концентрация C_пм', 'кг/м³'),
            ]),
            ("ПАРАМЕТРЫ ПРОИЗВОДИТЕЛЬНОСТИ", [
                ('alpha', 'Коэффициент α', 'кг/кг'),
                ('omega', 'Влажность ω', ''),
                ('G_0', 'Производительность G₀', 'кг/с'),
                ('phi_g', 'Коэффициент газосодержания φ_г', ''),
            ]),
            ("ПАРАМЕТРЫ МАССООБМЕНА", [
                ('g_k', 'Удельный расход O₂ g_к', 'кг/кг'),
                ('rho_air', 'Плотность воздуха', 'кг/м³'),
                ('y_n', 'Доля O₂ в воздухе y_н', ''),
                ('v_air', 'Скорость воздуха v_в', 'с⁻¹'),
                ('K_p', 'Коэффициент фазового равновесия K_p', ''),
            ])
        ]
        
        self.entries = {}
        
        # Создаем основной фрейм для групп
        groups_container = ttk.Frame(parent)
        groups_container.pack(fill='x')
        
        for i, (group_title, params) in enumerate(param_groups):
            group_frame = ttk.LabelFrame(groups_container, text=group_title)
            group_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            
            for j, (key, label, unit) in enumerate(params):
                # Создаем фрейм для каждой строки параметра
                param_frame = ttk.Frame(group_frame)
                param_frame.pack(fill='x', padx=8, pady=4)
                
                # Метка параметра
                label_widget = ttk.Label(param_frame, text=label, anchor='w')
                label_widget.pack(side='left', fill='x', expand=True)
                
                # Поле ввода
                entry = ttk.Entry(param_frame, width=12, font=('Arial', 10))
                entry.pack(side='left', padx=(10, 5))
                self.entries[key] = entry
                
                # Единица измерения
                unit_label = ttk.Label(param_frame, text=unit, width=8, anchor='w')
                unit_label.pack(side='left')
    
    def create_thermal_grid(self, parent):
        """Создает сетку тепловых параметров"""
        
        thermal_params = [
            ("ОСНОВНЫЕ ТЕПЛОВЫЕ ПАРАМЕТРЫ", [
                ('dH_r', 'Теплота образования ΔH_r', 'кДж/кг'),
                ('rho_nutrient', 'Плотность среды', 'кг/м³'),
                ('c_p_nutrient', 'Теплоемкость среды', 'Дж/(кг·К)'),
                ('K_heat', 'Коэффициент теплопередачи K', 'Вт/(м²·К)'),
            ]),
            ("ТЕМПЕРАТУРНЫЕ ПАРАМЕТРЫ", [
                ('dT_nutrient', 'ΔТ охлаждения среды', 'К'),
                ('dT_water', 'ΔТ нагрева воды', 'К'),
                ('T_reaction', 'Температура процесса', 'К'),
                ('T_water_in', 'Температура воды на входе', 'К'),
            ])
        ]
        
        # Создаем основной фрейм для групп
        groups_container = ttk.Frame(parent)
        groups_container.pack(fill='x')
        
        for i, (group_title, params) in enumerate(thermal_params):
            group_frame = ttk.LabelFrame(groups_container, text=group_title)
            group_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)
            
            for j, (key, label, unit) in enumerate(params):
                # Создаем фрейм для каждой строки параметра
                param_frame = ttk.Frame(group_frame)
                param_frame.pack(fill='x', padx=8, pady=4)
                
                # Метка параметра
                label_widget = ttk.Label(param_frame, text=label, anchor='w')
                label_widget.pack(side='left', fill='x', expand=True)
                
                # Поле ввода
                entry = ttk.Entry(param_frame, width=12, font=('Arial', 10))
                entry.pack(side='left', padx=(10, 5))
                self.entries[key] = entry
                
                # Единица измерения
                unit_label = ttk.Label(param_frame, text=unit, width=8, anchor='w')
                unit_label.pack(side='left')
    
    def create_results_tree(self, parent):
        # Создаем Treeview с увеличенными интервалами
        style = ttk.Style()
        style.configure("Treeview", 
                       rowheight=30,
                       font=('Arial', 10))
        style.configure("Treeview.Heading", 
                       font=('Arial', 11, 'bold'),
                       padding=5)
        
        columns = ('Параметр', 'Значение', 'Единица измерения', 'Формула/Описание')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)
        
        # Настраиваем заголовки с отступами
        self.tree.heading('Параметр', text='ПАРАМЕТР', anchor='w')
        self.tree.heading('Значение', text='ЗНАЧЕНИЕ', anchor='w')
        self.tree.heading('Единица измерения', text='ЕД. ИЗМ.', anchor='w')
        self.tree.heading('Формула/Описание', text='ОПИСАНИЕ', anchor='w')
        
        # Настраиваем ширину столбцов
        self.tree.column('Параметр', width=200, anchor='w')
        self.tree.column('Значение', width=140, anchor='w')
        self.tree.column('Единица измерения', width=100, anchor='w')
        self.tree.column('Формула/Описание', width=350, anchor='w')
        
        # Добавляем прокрутку
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=(0, 5))
        scrollbar.pack(side='right', fill='y')
        
        # Заполняем примером данных
        self.fill_example_data()
    
    def create_control_panel(self):
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(fill='x', side='bottom')
        
        # Кнопки с увеличенными отступами
        button_style = {'width': 18, 'padding': 8}
        
        ttk.Button(control_frame, text="▶ ВЫПОЛНИТЬ РАСЧЕТ", 
                  command=self.calculate_all, **button_style).pack(side='left', padx=10)
        
        ttk.Button(control_frame, text="📋 ЗАГРУЗИТЬ ПРИМЕР", 
                  command=self.load_example, **button_style).pack(side='left', padx=10)
        
        ttk.Button(control_frame, text="🗑️ ОЧИСТИТЬ ВСЕ", 
                  command=self.clear_all, **button_style).pack(side='left', padx=10)
        
        ttk.Button(control_frame, text="❌ ВЫХОД", 
                  command=self.root.quit, **button_style).pack(side='right', padx=10)
    
    def fill_example_data(self):
        """Заполняем Treeview примером результатов"""
        example_data = [
            ('Скорость роста биомассы', '2.23 × 10⁻⁵', 'с⁻¹', 'r = r_max × [Cₖ/(C_ус + Cₖ)] × [C_пм/(C_пм + C₀ + Cₖ)]'),
            ('Концентрация сухой биомассы', '26.67', 'кг/м³', 'C_сух = (C₀ - Cₖ) / α'),
            ('Рабочий объем аппарата', '35.1', 'м³', 'V_p = G₀ × ω / g'),
            ('Полный объем с аэрацией', '50.1', 'м³', "V_p' = V_p / φ_г"),
            ('Удельный расход кислорода', '1.19 × 10⁻³', 'кг/(м³·с)', 'v_O₂ = g × g_к'),
            ('Расход воздуха', '1.40', 'м³/с', 'V_в = v_в × V_p'),
            ('Теплота роста', '388.89', 'кВт', 'Q_р = ΔH_r × G₀'),
            ('Площадь теплообмена', '4.21', 'м²', 'F = Q_т / (K × ΔT_ср)'),
            ('Рекомендуемый объем', '50', 'м³', 'Стандартный объем по ГОСТ'),
        ]
        
        # Очищаем и заполняем с чередованием цветов
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for i, data in enumerate(example_data):
            item = self.tree.insert('', 'end', values=data)
            # Чередование цветов фона для лучшей читаемости
            if i % 2 == 0:
                self.tree.tag_configure('evenrow', background='#f0f0f0')
                self.tree.item(item, tags=('evenrow',))
    
    def get_float(self, key):
        try:
            value = self.entries[key].get().strip()
            return float(value) if value else float(self.default_values[key])
        except:
            return float(self.default_values[key])
    
    def calculate_all(self):
        try:
            # Получаем значения
            r_max = self.get_float('r_max')
            C_0 = self.get_float('C_0')
            C_k = self.get_float('C_k')
            C_us = self.get_float('C_us')
            C_pm = self.get_float('C_pm')
            alpha = self.get_float('alpha')
            omega = self.get_float('omega')
            G_0 = self.get_float('G_0')
            phi_g = self.get_float('phi_g')
            g_k = self.get_float('g_k')
            dH_r = self.get_float('dH_r')
            rho_air = self.get_float('rho_air')
            y_n = self.get_float('y_n')
            v_air = self.get_float('v_air')
            K_p = self.get_float('K_p')
            K_heat = self.get_float('K_heat')
            
            # Расчеты
            r = r_max * (C_k / (C_us + C_k)) * (C_pm / (C_pm + C_0 + C_k))
            C_dry = (C_0 - C_k) / alpha
            g = r * C_dry
            V_p = (G_0 * omega) / g
            V_p_prime = V_p / phi_g
            v_oxygen = g * g_k
            V_air_total = v_air * V_p
            
            # Тепловые расчеты
            Q_growth = dH_r * G_0 / 1000
            dT_avg = 10.5
            F_heat = Q_growth * 1000 / (K_heat * dT_avg)
            
            # Обновляем Treeview с результатами
            results_data = [
                ('Скорость роста биомассы', f'{r:.2e}', 'с⁻¹', 'r = r_max × [Cₖ/(C_ус + Cₖ)] × [C_пм/(C_пм + C₀ + Cₖ)]'),
                ('Концентрация сухой биомассы', f'{C_dry:.2f}', 'кг/м³', 'C_сух = (C₀ - Cₖ) / α'),
                ('Удельная производительность', f'{g:.2e}', 'кг/(м³·с)', 'g = r × C_сух'),
                ('Производительность с влажностью', f'{g/omega:.2e}', 'кг/(м³·с)', "g' = g / ω"),
                ('Рабочий объем аппарата', f'{V_p:.1f}', 'м³', 'V_p = (G₀ × ω) / g'),
                ('Полный объем с аэрацией', f'{V_p_prime:.1f}', 'м³', "V_p' = V_p / φ_г"),
                ('Расход питательной среды', f'{r*V_p:.2e}', 'м³/с', 'v_п = r × V_p'),
                ('Удельный расход кислорода', f'{v_oxygen:.2e}', 'кг/(м³·с)', 'v_O₂ = g × g_к'),
                ('Расход воздуха', f'{V_air_total:.2f}', 'м³/с', 'V_в = v_в × V_p'),
                ('Удельный расход воздуха', f'{V_air_total/V_p*3600:.0f}', 'м³/(м³·ч)', 'На единицу объема'),
                ('Теплота роста биомассы', f'{Q_growth:.1f}', 'кВт', 'Q_р = ΔH_r × G₀'),
                ('Площадь теплообмена', f'{F_heat:.2f}', 'м²', 'F = Q_т / (K × ΔT_ср)'),
                ('Рекомендуемый стандартный объем', f'{round(V_p_prime):.0f}', 'м³', 'По ГОСТ 20680-2002'),
            ]
            
            # Очищаем и заполняем таблицу
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            for i, data in enumerate(results_data):
                item = self.tree.insert('', 'end', values=data)
                # Чередование цветов фона
                if i % 2 == 0:
                    self.tree.item(item, tags=('evenrow',))
            
            # Показываем информацию о расчете
            messagebox.showinfo("✅ Расчет завершен", 
                              f"Основные параметры ферментера:\n\n"
                              f"• Рабочий объем: {V_p:.1f} м³\n"
                              f"• Рекомендуемый объем: {round(V_p_prime):.0f} м³\n"
                              f"• Расход воздуха: {V_air_total*3600:.0f} м³/ч\n"
                              f"• Тепловая мощность: {Q_growth:.1f} кВт\n"
                              f"• Площадь теплообмена: {F_heat:.2f} м²")
            
        except ZeroDivisionError as e:
            messagebox.showerror("Ошибка расчета", f"Деление на ноль в расчетах:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Проверьте корректность введенных данных:\n{str(e)}")
    
    def load_example(self):
        """Загружает пример данных из курсовой"""
        for key, value in self.default_values.items():
            if key in self.entries:
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, value)
        
        # Обновляем Treeview с примером
        self.fill_example_data()
        
        messagebox.showinfo("📋 Пример загружен", 
                          "Загружены исходные данные из курсовой работы.\n"
                          "Для выполнения расчета нажмите 'ВЫПОЛНИТЬ РАСЧЕТ'.")
    
    def clear_all(self):
        """Очищает все поля"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        # Очищаем Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        messagebox.showinfo("🗑️ Очистка", "Все поля ввода и результаты очищены.")

def main():
    root = tk.Tk()
    app = BioreactorCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()