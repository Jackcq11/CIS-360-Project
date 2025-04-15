import yfinance as yf
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tabulate import tabulate

def get_stock_data(ticker, period):
    if not ticker:
        messagebox.showerror("Error", "Please enter a valid stock ticker symbol.")
        return None
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    
    if df.empty:
        messagebox.showerror("Error", f"No data found for ticker '{ticker}'.")
        return None
    
    return df

def fetch_and_display_data(entry_ticker, period_var, text_output):
    ticker = entry_ticker.get().strip().upper()
    period_mapping = {
        "1 Day": "1d",
        "5 Days": "5d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "Max": "max"
    }

    period = period_mapping.get(period_var.get(), "1mo")  # Default to 1 Month if invalid
    data = get_stock_data(ticker, period)

    if data is not None:
        text_output.config(state="normal")  # Enable editing temporarily
        text_output.delete("1.0", tk.END)  # Clear previous output
        text_output.tag_configure("center", justify="center")  # Set center alignment
        
        data = data.round(3)
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        formatted_table = tabulate(data, headers="keys", tablefmt="pretty")

        text_output.insert(tk.END, formatted_table, "center")  # Apply center tag
        text_output.config(state="disabled")  # Disable editing again

def fetch_and_display_change(entry_ticker, period_var, text_output):
    ticker = entry_ticker.get().strip().upper()
    period_mapping = {
        "5 Days": "5d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "Max": "max"
    }

    period = period_mapping.get(period_var.get(), "1d")  # Default to 1 Day if invalid
    data = get_stock_data(ticker, period)

    if data is not None:
        first_price = data.iloc[0]['Close']
        last_price = data.iloc[-1]['Close']
        percent_change = ((last_price - first_price) / first_price) * 100

        result = f"\nStock Price Change Analysis:\n"
        result += f"Start Price: ${first_price:.2f}\n"
        result += f"End Price: ${last_price:.2f}\n"
        result += f"Percentage Change: "

        text_output.config(state="normal")  # Enable editing temporarily
        text_output.delete("1.0", tk.END)  # Clear previous output
        text_output.tag_configure("center", justify="center")  # Center text

        # Configure tags for color styling
        text_output.tag_configure("positive", foreground="green", font=("Helvetica", 18, "bold"))
        text_output.tag_configure("negative", foreground="red", font=("Helvetica", 18, "bold"))
        text_output.tag_configure("default", foreground="black", font=("Helvetica", 18))

        # Insert base text
        text_output.insert(tk.END, result, ("default", "center"))  # Apply center tag

        # Insert percentage change with color
        if percent_change >= 0:
            text_output.insert(tk.END, f"+{percent_change:.2f}%\n", ("positive", "center"))
        else:
            text_output.insert(tk.END, f"{percent_change:.2f}%\n", ("negative", "center"))
        text_output.config(state="disabled")  # Disable editing again

def show_graph(entry_ticker, period_var, text_output):
    ticker = entry_ticker.get().strip().upper()
    period_mapping = {
        "5 Days": "5d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "Max": "max"
    }

    period = period_mapping.get(period_var.get(), "1d")  # Default to 1 Day if invalid
    data = get_stock_data(ticker, period)

    if data is not None:
        len = len(data)


def upload_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not filename:
        return None
    try:
        data = pd.read_csv(filename)
        return True, data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV file: {e}")
        return None

def main():
    # GUI Setup
    root = tk.Tk()
    root.title("Stock Data Viewer")
    window_width = 930
    window_height = 750
    root.geometry(f"{window_width}x{window_height}")

    # Stock ticker input
    tk.Label(root, text="Stock Ticker:").grid(row=0, column=0, padx=5, pady=5)
    entry_ticker = tk.Entry(root)
    entry_ticker.grid(row=0, column=1, padx=5, pady=5)

    # Time period dropdown
    tk.Label(root, text="Select Time Period:").grid(row=1, column=0, padx=5, pady=5)
    period_options = ["5 Days", "1 Month", "3 Months", "6 Months", "1 Year", "5 Years", "Max"]

    period_var = tk.StringVar(value="5 Days")
    dropdown_period = ttk.Combobox(root, textvariable=period_var, values=period_options, state="readonly")
    dropdown_period.grid(row=1, column=1, padx=5, pady=5)

    # Buttons
    btn_fetch = tk.Button(root, text="Get Stock Data", command=lambda: fetch_and_display_data(entry_ticker, period_var, text_output))
    btn_fetch.grid(row=3, column=0, padx=5, pady=5)

    btn_analyze = tk.Button(root, text="Check Percentage Change", command=lambda: fetch_and_display_change(entry_ticker, period_var, text_output))
    btn_analyze.grid(row=4, column=0, padx=5, pady=5)

    btn_upload = tk.Button(root, text="Upload CSV", command=lambda: upload_csv())
    btn_upload.grid(row=3, column=1, padx=5, pady=5)

    # Output text area
    text_output = tk.Text(root, height=20, width=105)
    text_output.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    text_output.config(state="disabled")  # Disable editing
    text_output2 = tk.Text(root, height=30, width=130)
    text_output2.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    text_output2.config(state="disabled")  # Disable editing


    root.resizable(False, False)
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
