import tkinter as tk
from tkinter import ttk, messagebox
from scipy.optimize import linprog

class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Resolução de Problema de Programação Linear")
        self.root.geometry("500x750")
        self.root.config(bg="#f0f0f0")

        # Estilos
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        style.configure("TButton", font=("Arial", 10, "bold"), foreground="#000000", background="#007acc")
        style.map("TButton", background=[("active", "#005a99")])

        # Título
        title = ttk.Label(root, text="Método Simplex", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Entrada do número de variáveis
        frame = tk.Frame(root, bg="#f0f0f0")
        frame.pack(pady=5)
        
        ttk.Label(frame, text="Número de Variáveis de Decisão:").grid(row=0, column=0, sticky="w")
        self.num_vars_entry = ttk.Entry(frame, width=5)
        self.num_vars_entry.grid(row=0, column=1, padx=5)

        # Entrada do número de restrições
        ttk.Label(frame, text="Número de Restrições:").grid(row=1, column=0, sticky="w")
        self.num_constraints_entry = ttk.Entry(frame, width=5)
        self.num_constraints_entry.grid(row=1, column=1, padx=5)

        # Botão para definir variáveis e restrições
        ttk.Button(root, text="Definir Problema", command=self.create_problem_inputs).pack(pady=10)

    def create_problem_inputs(self):
        try:
            self.num_vars = int(self.num_vars_entry.get())
            self.num_constraints = int(self.num_constraints_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")
            return

        # Limpar entradas anteriores
        for widget in self.root.winfo_children():
            widget.destroy()

        # Entrada da função objetivo
        objective_frame = tk.Frame(self.root, bg="#f0f0f0")
        objective_frame.pack(pady=5)
        
        ttk.Label(objective_frame, text="Função Objetivo (Maximizar):").grid(row=0, column=0, columnspan=self.num_vars * 2, pady=5)
        
        ttk.Label(objective_frame, text="Max:").grid(row=1, column=0, padx=5)

        self.objective_entries = []
        for j in range(self.num_vars):
            entry = ttk.Entry(objective_frame, width=5)
            entry.grid(row=1, column=(j * 2) + 1, padx=5)
            self.objective_entries.append(entry)

            ttk.Label(objective_frame, text=f"x{j + 1}").grid(row=1, column=(j * 2) + 2, padx=5)

        # Entrada das restrições
        constraint_frame = tk.Frame(self.root, bg="#f0f0f0")
        constraint_frame.pack(pady=5)
        
        self.constraints_entries = []
        self.b_entries = []

        for i in range(self.num_constraints):
            row_entries = []
            ttk.Label(constraint_frame, text=f"Restrição {i + 1}:").grid(row=i, column=0, sticky="e", padx=5)
            
            for j in range(self.num_vars):
                entry = ttk.Entry(constraint_frame, width=5)
                entry.grid(row=i, column=(j * 2) + 1, padx=5)
                row_entries.append(entry)

                ttk.Label(constraint_frame, text=f"x{j + 1}").grid(row=i, column=(j * 2) + 2, padx=5)

            self.constraints_entries.append(row_entries)

            ttk.Label(constraint_frame, text="≤").grid(row=i, column=(self.num_vars * 2) + 1, padx=5)

            b_entry = ttk.Entry(constraint_frame, width=5)
            b_entry.grid(row=i, column=(self.num_vars * 2) + 2, padx=5)
            self.b_entries.append(b_entry)

        ttk.Button(self.root, text="Resolver", command=self.solve_simplex).pack(pady=20)

    def solve_simplex(self):
        try:
            c = [-float(entry.get()) for entry in self.objective_entries]
            A = []
            b = []
            for i in range(self.num_constraints):
                A.append([float(entry.get()) for entry in self.constraints_entries[i]])
                b.append(float(self.b_entries[i].get()))

            result = linprog(c, A_ub=A, b_ub=b, method='simplex')

            if result.success:
                self.solution = result.x
                self.objective_value = -result.fun
                self.A, self.b, self.c = A, b, c
                self.shadow_prices = result.slack  # Preços sombra
                messagebox.showinfo("Resultado", f"Solução: {self.solution}\nValor da Função Objetivo: {self.objective_value:.2f}")
                self.create_shadow_price_inputs()
            else:
                messagebox.showerror("Erro", "O problema não possui solução viável.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores válidos.")

    def create_shadow_price_inputs(self):
        shadow_price_frame = tk.Frame(self.root, bg="#f0f0f0")
        shadow_price_frame.pack(pady=10)

        ttk.Label(shadow_price_frame, text="Ajuste de Recursos:").pack(pady=5)

        self.delta_b_entries = []
        for i in range(len(self.b)):
            frame = tk.Frame(shadow_price_frame, bg="#f0f0f0")
            frame.pack(pady=5)
            ttk.Label(frame, text=f"Restrição {i + 1}:").grid(row=0, column=0, padx=5)
            delta_entry = ttk.Entry(frame, width=10)
            delta_entry.grid(row=0, column=1, padx=5)
            self.delta_b_entries.append(delta_entry)

        ttk.Button(shadow_price_frame, text="Aplicar Ajuste", command=self.apply_shadow_price_adjustments).pack(pady=10)

    def apply_shadow_price_adjustments(self):
        try:
            deltas = [float(entry.get()) if entry.get() else 0 for entry in self.delta_b_entries]
            adjusted_b = [self.b[i] + deltas[i] for i in range(len(self.b))]

            # Verificando a viabilidade do ajuste com base nos preços sombra
            for i, delta in enumerate(deltas):
                if delta > 0 and self.shadow_prices[i] < 0:
                    messagebox.showwarning("Aviso", f"O aumento da restrição {i + 1} pode não ser viável, pois o preço sombra é negativo.")
                    return

            result = linprog(self.c, A_ub=self.A, b_ub=adjusted_b, method='simplex')

            if result.success:
                new_objective_value = -result.fun
                messagebox.showinfo("Novo Resultado", f"Novo Valor da Função Objetivo: {new_objective_value:.2f}\n"
                                                      f"Ajuste Viável.")
            else:
                messagebox.showerror("Erro", "Ajuste inviável. Restrições violadas.")
        except ValueError:
            messagebox.showerror("Erro", "Insira valores válidos para o ajuste.")

# Inicializar a aplicação
root = tk.Tk()
app = SimplexApp(root)
root.mainloop()

