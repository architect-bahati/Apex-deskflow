import tkinter as tk
from tkinter import ttk, messagebox
from invoice_generator import create_invoice  # Custom PDF Invoice Generator
import database

class ApexDeskFlow:
    def __init__(self, root):
        self.root = root
        self.root.title("Apex DeskFlow — Productivity Hub")
        self.root.geometry("720x580")
        self.root.resizable(False, False)
        
        self.db = database.load_data()
        self.setup_ui()

    def setup_ui(self):
        # Header Banner
        header = tk.Frame(self.root, bg="#1e1e2e", height=60)
        header.pack(fill="x")
        title_label = tk.Label(
            header, text="⚡ APEX DESKFLOW HUB", 
            font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1e1e2e"
        )
        title_label.pack(pady=15)

        # Tab Control Navigation
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Tab 1: Dashboard Overview
        self.dash_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dash_tab, text=" 📊 Overview ")
        self.build_dashboard_ui()

        # Tab 2: Ledger / Cash Tracker
        self.ledger_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ledger_tab, text=" 💰 Cash Ledger ")
        self.build_ledger_ui()

        # Tab 3: Task Manager
        self.task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text=" 📝 Task Manager ")
        self.build_task_ui()

        # Refresh all dynamic data displays
        self.refresh_all()

    def build_dashboard_ui(self):
        # Summary Statistics Frame
        stats_frame = ttk.LabelFrame(self.dash_tab, text="Live Operations Metrics")
        stats_frame.pack(fill="x", padx=15, pady=15)

        self.lbl_total_trans = ttk.Label(stats_frame, text="Total Ledger Entries: 0", font=("Segoe UI", 11))
        self.lbl_total_trans.pack(anchor="w", padx=15, pady=5)

        self.lbl_total_val = ttk.Label(stats_frame, text="Total Recorded Volume: KES 0.00", font=("Segoe UI", 11, "bold"))
        self.lbl_total_val.pack(anchor="w", padx=15, pady=5)

        self.lbl_pending_tasks = ttk.Label(stats_frame, text="Pending Tasks: 0", font=("Segoe UI", 11))
        self.lbl_pending_tasks.pack(anchor="w", padx=15, pady=5)

        self.lbl_done_tasks = ttk.Label(stats_frame, text="Completed Tasks: 0", font=("Segoe UI", 11))
        self.lbl_done_tasks.pack(anchor="w", padx=15, pady=5)

        # Report Exporter Frame
        export_frame = ttk.LabelFrame(self.dash_tab, text="Export & Reporting Engine")
        export_frame.pack(fill="x", padx=15, pady=10)

        btn_export = ttk.Button(export_frame, text="⚡ Export DeskFlow_Summary.txt", command=self.export_report)
        btn_export.pack(padx=15, pady=5)

        # PDF Invoice Exporter Button
        btn_pdf_invoice = ttk.Button(export_frame, text="📄 Generate PDF Invoice from Ledger", command=self.generate_pdf_invoice)
        btn_pdf_invoice.pack(padx=15, pady=5)

    def build_ledger_ui(self):
        frame = ttk.LabelFrame(self.ledger_tab, text="Add Transaction (KES)")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Description:").grid(row=0, column=0, padx=5, pady=5)
        self.desc_entry = ttk.Entry(frame, width=20)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame, width=12)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(frame, text="Add Entry", command=self.add_transaction).grid(row=0, column=4, padx=5, pady=5)

        # Transaction List Display
        self.trans_list = tk.Listbox(self.ledger_tab, height=14)
        self.trans_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def build_task_ui(self):
        frame = ttk.LabelFrame(self.task_tab, text="New Task")
        frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = ttk.Entry(frame, width=35)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Task", command=self.add_task).grid(row=0, column=2, padx=5, pady=5)

        # Task Listbox
        self.task_list = tk.Listbox(self.task_tab, height=12)
        self.task_list.pack(fill="both", expand=True, padx=10, pady=5)

        # Action Buttons for Tasks
        btn_frame = ttk.Frame(self.task_tab)
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Button(btn_frame, text="✔ Mark Completed", command=self.complete_task).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="❌ Delete Selected Task", command=self.delete_task).pack(side="right", padx=5)

    def add_transaction(self):
        desc = self.desc_entry.get().strip()
        amt = self.amount_entry.get().strip()

        if not desc or not amt:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            amount_val = float(amt)
            self.db["transactions"].append({"desc": desc, "amount": amount_val})
            database.save_data(self.db)
            self.desc_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.refresh_all()
            messagebox.showinfo("Success", f"Recorded entry for '{desc}'!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")

    def add_task(self):
        task_name = self.task_entry.get().strip()
        if not task_name:
            messagebox.showwarning("Input Error", "Please enter a task description.")
            return

        self.db["tasks"].append({"task": task_name, "completed": False})
        database.save_data(self.db)
        self.task_entry.delete(0, tk.END)
        self.refresh_all()

    def complete_task(self):
        try:
            selected_idx = self.task_list.curselection()[0]
            self.db["tasks"][selected_idx]["completed"] = True
            database.save_data(self.db)
            self.refresh_all()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        try:
            selected_idx = self.task_list.curselection()[0]
            removed_task = self.db["tasks"].pop(selected_idx)
            database.save_data(self.db)
            self.refresh_all()
            messagebox.showinfo("Deleted", f"Removed task: '{removed_task['task']}'")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def refresh_all(self):
        # Refresh Ledger UI
        self.trans_list.delete(0, tk.END)
        total_val = 0.0
        for t in self.db["transactions"]:
            self.trans_list.insert(tk.END, f"• {t['desc']}: KES {t['amount']:,.2f}")
            total_val += t['amount']

        # Refresh Tasks UI
        self.task_list.delete(0, tk.END)
        pending_cnt = 0
        done_cnt = 0
        for tk_item in self.db["tasks"]:
            status = "[✔ Done]" if tk_item.get("completed", False) else "[ ] Pending"
            if tk_item.get("completed", False):
                done_cnt += 1
            else:
                pending_cnt += 1
            self.task_list.insert(tk.END, f"{status} - {tk_item['task']}")

        # Refresh Dashboard UI
        self.lbl_total_trans.config(text=f"Total Ledger Entries: {len(self.db['transactions'])}")
        self.lbl_total_val.config(text=f"Total Recorded Volume: KES {total_val:,.2f}")
        self.lbl_pending_tasks.config(text=f"Pending Tasks: {pending_cnt}")
        self.lbl_done_tasks.config(text=f"Completed Tasks: {done_cnt}")

    def generate_pdf_invoice(self):
        """Compiles active ledger entries into a PDF invoice."""
        if not self.db["transactions"]:
            messagebox.showwarning("No Data", "Please add at least one cash ledger entry to generate an invoice.")
            return

        try:
            # Converts ledger records to invoice item tuples: (description, quantity, amount)
            items = [(t["desc"], 1, t["amount"]) for t in self.db["transactions"]]
            create_invoice("Valued Client", items, "INV-2001")
            messagebox.showinfo("Invoice Created", "✅ PDF Invoice successfully compiled and saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate invoice PDF: {e}")

    def export_report(self):
        try:
            total_val = sum(t['amount'] for t in self.db['transactions'])
            pending_tasks = [t['task'] for t in self.db['tasks'] if not t.get('completed', False)]
            done_tasks = [t['task'] for t in self.db['tasks'] if t.get('completed', False)]

            with open("DeskFlow_Summary.txt", "w", encoding="utf-8") as f:
                f.write("=========================================\n")
                f.write("       APEX DESKFLOW SUMMARY REPORT      \n")
                f.write("=========================================\n\n")
                f.write(f"Total Transactions: {len(self.db['transactions'])}\n")
                f.write(f"Total Cash Volume: KES {total_val:,.2f}\n\n")
                f.write("--- LEDGER ENTRIES ---\n")
                for t in self.db['transactions']:
                    f.write(f" • {t['desc']}: KES {t['amount']:,.2f}\n")
                f.write("\n--- PENDING TASKS ---\n")
                for pt in pending_tasks:
                    f.write(f" [ ] {pt}\n")
                f.write("\n--- COMPLETED TASKS ---\n")
                for dt in done_tasks:
                    f.write(f" [✔] {dt}\n")

            messagebox.showinfo("Export Success", "Report generated in 'DeskFlow_Summary.txt'!")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export report: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ApexDeskFlow(root)
    root.mainloop()