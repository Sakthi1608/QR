from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import sqlite3
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import cv2

class QRScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Organizer")
        self.root.geometry("600x400")

        self.db_helper = DBHelper()

        self.scan_button = tk.Button(root, text="Scan QR Code", command=self.open_scanner, width=20)
        self.scan_button.pack(pady=20)

        self.view_button = tk.Button(root, text="View Saved Scans", command=self.view_scans, width=20)
        self.view_button.pack(pady=20)

    def open_scanner(self):
        scanner_window = tk.Toplevel(self.root)
        scanner = ScannerWindow(scanner_window, self.db_helper)

    def view_scans(self):
        scans = self.db_helper.get_all_scans()
        scans_window = tk.Toplevel(self.root)
        scans_window.title("Saved Scans")

        for i, scan in enumerate(scans):
            label = tk.Label(scans_window, text=f"[{scan[2]}] {scan[1]}")
            label.grid(row=i, column=0, padx=10, pady=5)


class DBHelper:
    def __init__(self):
        self.conn = sqlite3.connect('scans.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scans 
                               (id INTEGER PRIMARY KEY, data TEXT, category TEXT)''')
        self.conn.commit()

    def insert_scan(self, data, category):
        self.cursor.execute("INSERT INTO scans (data, category) VALUES (?, ?)", (data, category))
        self.conn.commit()

    def get_all_scans(self):
        self.cursor.execute("SELECT * FROM scans")
        return self.cursor.fetchall()


class ScannerWindow:
    def __init__(self, root, db_helper):
        self.root = root
        self.db_helper = db_helper
        self.root.title("QR Code Scanner")
        self.root.geometry("640x480")

        self.camera = cv2.VideoCapture(0)
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack()

        self.scan_button = tk.Button(self.root, text="Save Scan", command=self.save_scan, width=20)
        self.scan_button.pack(pady=10)

        self.category_var = tk.StringVar(self.root)
        self.category_var.set("Others")  # default value
        self.category_menu = tk.OptionMenu(self.root, self.category_var, "Website", "Contact", "Payment", "Others")
        self.category_menu.pack(pady=10)

        self.run_camera()

    def run_camera(self):
        _, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = ImageTk.PhotoImage(image)

        self.canvas.create_image(0, 0, image=image, anchor=tk.NW)
        self.root.after(10, self.run_camera)
        self.process_frame(frame)

    def process_frame(self, frame):
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            self.display_scanned_data(barcode_data)

    def display_scanned_data(self, data):
        self.saved_data = data
        messagebox.showinfo("Scanned Data", f"Scanned Data: {data}")

    def save_scan(self):
        category = self.category_var.get()
        self.db_helper.insert_scan(self.saved_data, category)
        messagebox.showinfo("Saved", "Scan saved successfully!")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRScannerApp(root)
    root.mainloop()

from pyzbar.pyzbar import decode
from PIL import Image

img = Image.open("https://api.qrserver.com/v1/create-qr-code/?data=Hi+from+Vadhana%21+This+is+my+QR+code+%F0%9F%98%8A&size=200x200")
decoded_objects = decode(img)

for obj in decoded_objects:
    print("QR Code Data:", obj.data.decode("utf-8"))