import tkinter as tk
from tkinter import ttk, messagebox
import time
import matplotlib.pyplot as plt

# Backend Algorithms
def knapsack_dp(weights, values, capacity):
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    
    res = dp[n][capacity]
    w = capacity
    items_selected = []
    
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == dp[i - 1][w]:
            continue
        else:
            items_selected.append(i)
            res -= values[i - 1]
            w -= weights[i - 1]
    
    items_selected.reverse()
    return dp[n][capacity], items_selected


def knapsack_greedy(weights, values, capacity):
    ratio = [(values[i] / weights[i], i) for i in range(len(values))]
    ratio.sort(reverse=True)
    
    total_value = 0
    total_weight = 0
    items_selected = []
    
    for r, i in ratio:
        if total_weight + weights[i] <= capacity:
            total_value += values[i]
            total_weight += weights[i]
            items_selected.append((i + 1, 1))
        else:
            remain = capacity - total_weight
            total_value += values[i] * (remain / weights[i])
            items_selected.append((i + 1, round(remain / weights[i], 2)))
            break
    
    return total_value, items_selected

# GUI Application
class KnapsackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎒 Knapsack Problem Solver (DP + Greedy)")
        self.root.geometry("800x700")
        self.root.configure(bg="#f8ede3")

        # Title
        tk.Label(root, text="🧮 Knapsack Problem Solver",
                 font=("Helvetica", 22, "bold"),
                 bg="#6f4e37", fg="white", pady=10).pack(fill="x")

        # Input Section
        input_frame = tk.Frame(root, bg="#f8ede3")
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Number of Items:", font=("Arial", 12), bg="#f8ede3").grid(row=0, column=0, padx=5, pady=5)
        self.item_count = tk.Entry(input_frame, width=10)
        self.item_count.grid(row=0, column=1, padx=5)

        tk.Button(input_frame, text="Create Table", command=self.create_table,
                  bg="#8b5e3c", fg="white", width=14).grid(row=0, column=2, padx=10)

        # Table Frame
        self.table_frame = tk.Frame(root, bg="#f8ede3")
        self.table_frame.pack(pady=10)

        # Algorithm Frame
        algo_frame = tk.Frame(root, bg="#f8ede3")
        algo_frame.pack(pady=10)

        tk.Label(algo_frame, text="Choose Algorithm:", font=("Arial", 12), bg="#f8ede3").pack(side="left", padx=5)
        self.algo_choice = ttk.Combobox(algo_frame, values=["Dynamic Programming (0/1)", "Greedy Method (Fractional)"], width=30)
        self.algo_choice.pack(side="left")
        self.algo_choice.current(0)

        tk.Label(algo_frame, text="  Capacity:", font=("Arial", 12), bg="#f8ede3").pack(side="left", padx=5)
        self.capacity = tk.Entry(algo_frame, width=10)
        self.capacity.pack(side="left")

        # Buttons
        btn_frame = tk.Frame(root, bg="#f8ede3")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔹 Solve Knapsack", command=self.solve_knapsack,
                  bg="#4e342e", fg="white", font=("Arial", 12, "bold"), width=16).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="📊 Show Graph", command=self.show_graph,
                  bg="#3e2723", fg="white", font=("Arial", 12, "bold"), width=16).grid(row=0, column=1, padx=8)

        # Result Box
        tk.Label(root, text="Results:", font=("Arial", 14, "bold"), bg="#f8ede3").pack()
        self.result_box = tk.Text(root, width=90, height=10, wrap="word",
                                  bg="#fff8e1", fg="#3e2723", font=("Consolas", 11))
        self.result_box.pack(pady=5)

        # Storage
        self.value_entries = []
        self.weight_entries = []
        self.values = []
        self.weights = []
        self.selected_items = []
        self.max_value = 0

    # Create Dynamic Input Table
    def create_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        try:
            n = int(self.item_count.get())
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid number of items.")
            return

        tk.Label(self.table_frame, text="Item No", font=("Arial", 11, "bold"), bg="#d7ccc8", width=10).grid(row=0, column=0)
        tk.Label(self.table_frame, text="Value", font=("Arial", 11, "bold"), bg="#d7ccc8", width=10).grid(row=0, column=1)
        tk.Label(self.table_frame, text="Weight", font=("Arial", 11, "bold"), bg="#d7ccc8", width=10).grid(row=0, column=2)

        self.value_entries = []
        self.weight_entries = []

        for i in range(n):
            tk.Label(self.table_frame, text=f"Item {i+1}", bg="#f8ede3").grid(row=i+1, column=0)
            val = tk.Entry(self.table_frame, width=10)
            wt = tk.Entry(self.table_frame, width=10)
            val.grid(row=i+1, column=1)
            wt.grid(row=i+1, column=2)
            self.value_entries.append(val)
            self.weight_entries.append(wt)

    # Solve Knapsack
    def solve_knapsack(self):
        try:
            self.values = [int(v.get()) for v in self.value_entries]
            self.weights = [int(w.get()) for w in self.weight_entries]
            capacity = int(self.capacity.get())
        except:
            messagebox.showerror("Invalid Input", "Please check your input values.")
            return

        algo = self.algo_choice.get()
        start = time.time()

        if "Dynamic" in algo:
            self.max_value, items = knapsack_dp(self.weights, self.values, capacity)
            result_text = f"Algorithm: Dynamic Programming (0/1 Knapsack)\n"
            result_text += f"Selected Items: {items}\n"
            self.selected_items = items
        else:
            self.max_value, items = knapsack_greedy(self.weights, self.values, capacity)
            result_text = f"Algorithm: Greedy Method (Fractional Knapsack)\n"
            result_text += f"Items (Index, Fraction): {items}\n"
            self.selected_items = [i[0] for i in items]

        end = time.time()
        result_text += f"Maximum Value: {round(self.max_value, 2)}\n"
        result_text += f"Execution Time: {round(end - start, 6)} seconds\n"

        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, result_text)

    # Graph Visualization
    def show_graph(self):
        if not self.values or not self.weights:
            messagebox.showwarning("No Data", "Please solve the knapsack first.")
            return

        items = [f"Item {i+1}" for i in range(len(self.values))]
        colors = ['#6d4c41' if (i+1) in self.selected_items else '#bcaaa4' for i in range(len(self.values))]

        plt.figure(figsize=(8, 5))
        plt.bar(items, self.values, color=colors)
        plt.title("Knapsack Items (Selected vs Not Selected)", fontsize=14)
        plt.xlabel("Items")
        plt.ylabel("Values")
        plt.legend(["Selected Items", "Unselected Items"], loc="upper left")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.show()

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackApp(root)
    root.mainloop()
