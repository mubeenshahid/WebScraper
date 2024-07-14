import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class WebScraperGUI:
    def __init__(self, master):
        self.master = master
        master.title("Web Scraper")
        master.geometry("600x500")
        master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        style.configure('TButton', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))
        style.configure('TCombobox', font=('Arial', 12))

        main_frame = ttk.Frame(master, padding="20 20 20 20", style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.url_label = ttk.Label(main_frame, text="Enter URL:")
        self.url_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky='we', pady=(0, 15))

        self.tag_label = ttk.Label(main_frame, text="Select tag to scrape:")
        self.tag_label.grid(row=2, column=0, sticky='w', pady=(0, 5))

        self.tag_var = tk.StringVar()
        self.tag_options = ['p', 'h1', 'h2', 'a', 'div', 'span']
        self.tag_dropdown = ttk.Combobox(main_frame, textvariable=self.tag_var, values=self.tag_options,
                                         state='readonly')
        self.tag_dropdown.grid(row=3, column=0, sticky='we', pady=(0, 15))
        self.tag_dropdown.set('p')

        self.scrape_button = ttk.Button(main_frame, text="Scrape", command=self.scrape_website)
        self.scrape_button.grid(row=4, column=0, sticky='we', pady=(0, 15))

        self.result_label = ttk.Label(main_frame, text="Scraped Results:")
        self.result_label.grid(row=5, column=0, sticky='w', pady=(0, 5))

        self.result_text = tk.Text(main_frame, height=10, width=50, font=('Arial', 10))
        self.result_text.grid(row=6, column=0, columnspan=2, sticky='nswe', pady=(0, 15))

        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.result_text.yview)
        scrollbar.grid(row=6, column=2, sticky='ns')
        self.result_text['yscrollcommand'] = scrollbar.set

        self.pdf_button = ttk.Button(main_frame, text="Generate PDF", command=self.generate_pdf)
        self.pdf_button.grid(row=7, column=0, sticky='we')

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.scraped_data = []

    def scrape_website(self):
        url = self.url_entry.get()
        tag = self.tag_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            elements = soup.find_all(tag)
            self.scraped_data = [elem.text.strip() for elem in elements if elem.text.strip()]

            self.result_text.delete(1.0, tk.END)
            for item in self.scraped_data:
                self.result_text.insert(tk.END, item + "\n\n")

            messagebox.showinfo("Success", f"Web scraping completed. Found {len(self.scraped_data)} {tag} elements.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def generate_pdf(self):
        if not self.scraped_data:
            messagebox.showerror("Error", "No data to generate PDF. Please scrape a website first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return  # User cancelled the file dialog

        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []

        data = [["Scraped Data"]]
        for item in self.scraped_data:
            data.append([item])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)

        messagebox.showinfo("Success", f"PDF generated: {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperGUI(root)
    root.mainloop()