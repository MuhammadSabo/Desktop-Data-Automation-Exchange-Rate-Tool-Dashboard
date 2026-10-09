import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import pandas as pd
import matplotlib.pyplot as plt

class ProfessionalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Data Automation & Exchange Rate Tool Dashboard")
        self.root.geometry("700x420")
        self.root.configure(bg="#1e1e2e")
        
        # Title Label
        self.title_label = tk.Label(
            root, text="Enterprise Sales Automator & Live Exchange Portal", 
            font=("Helvetica", 16, "bold"), fg="#cdd6f4", bg="#1e1e2e"
        )
        self.title_label.pack(pady=20)
        
        self.info_label = tk.Label(
            root, text="Select an operation mode below:",
            font=("Helvetica", 10), fg="#a6adc8", bg="#1e1e2e"
        )
        self.info_label.pack(pady=5)

        # Button 1: Local CSV Processing
        self.upload_btn = tk.Button(
            root, text="📁 Import & Process Local CSV", font=("Helvetica", 11, "bold"),
            fg="#11111b", bg="#89b4fa", activebackground="#b4befe",
            width=32, pady=8, borderwidth=0, command=self.process_csv
        )
        self.upload_btn.pack(pady=10)
        
        # Button 2: Live API Integration
        self.api_btn = tk.Button(
            root, text="🌐 Fetch Live Currency Exchange API", font=("Helvetica", 11, "bold"),
            fg="#11111b", bg="#a6e3a1", activebackground="#b4befe",
            width=32, pady=8, borderwidth=0, command=self.fetch_live_api
        )
        self.api_btn.pack(pady=10)
        
        # Footer
        self.footer_label = tk.Label(
            root, text="Python Automation Engine v2.0 (API Enabled)", 
            font=("Helvetica", 9, "italic"), fg="#585b70", bg="#1e1e2e"
        )
        self.footer_label.pack(side="bottom", pady=15)

    def process_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            df = pd.read_csv(file_path)
            df["Total_Revenue"] = df["Units"] * df["Price_Per_Unit"]
            product_summary = df.groupby("Product")["Total_Revenue"].sum()
            
            messagebox.showinfo("Success", "Local data compiled! Generating visualization...")
            
            plt.style.use('ggplot')
            fig, ax = plt.subplots(figsize=(7, 4.5))
            product_summary.plot(kind='barh', color='#89b4fa', ax=ax)
            ax.set_title("Revenue Contribution by Product Line", fontsize=12, fontweight='bold')
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Data Error", f"Could not process file.\nDetails: {str(e)}")

    def fetch_live_api(self):
        try:
            # Querying a live public financial exchange rate API
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)

            # Raise an exception if the web request failed
            response.raise_for_status()
            
            data = response.json()
            rates = data.get("rates", {})
            
            ngn = rates.get("NGN", "N/A")
            eur = rates.get("EUR", "N/A")
            gbp = rates.get("GBP", "N/A")
            jpy = rates.get("JPY", "N/A")
            
            
            msg = (
                f"Live Exchange Rates (Base: USD):\n\n"
                f"• Nigerian Naira (NGN): {ngn}\n"
                f"• Euro (EUR): {eur}\n"
                f"• British Pound (GBP): {gbp}\n"
                f"• Japanese Yen (JPY): {jpy}\n\n"
   f"Data fetched successfully from live external server!"
            )
            messagebox.showinfo("Live API Response", msg)
            
        except requests.exceptions.RequestException as err:
            messagebox.showerror("Network Error", f"Failed to connect to API.\nDetails: {str(err)}")

if __name__ == "__main__":
    window = tk.Tk()
    app = ProfessionalApp(window)
    window.mainloop()
