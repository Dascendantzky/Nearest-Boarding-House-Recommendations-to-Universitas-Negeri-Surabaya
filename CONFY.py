import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import pandas as pd
import os
import csv
import textwrap
import random


CSV_FILE = 'data_kos.csv'


# Halaman awal 
class AwalanPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Halaman Utama')
        self.geometry('1278x700')
        self.resizable(False,False)

        awalan1 = Image.open('awalan.png')
        awalan = awalan1.resize((1278,700))
        self.bg_awalan = ImageTk.PhotoImage(awalan)

        self.label_awalan = tk.Label(self, image=self.bg_awalan, bg='white', bd=0)
        self.label_awalan.place(x=0, y=0)

        self.button_admin = Image.open("t.admin.png")
        self.button_admin = self.button_admin.resize((260,75), Image.LANCZOS)
        self.button_photoadmin = ImageTk.PhotoImage(self.button_admin)

        # tombol label untuk ke admin
        self.button_labeladmin = tk.Label(self, image=self.button_photoadmin, borderwidth=0)
        self.button_labeladmin.place(x=980, y=470)

        self.button_labeladmin.bind("<Button-1>", self.go_to_login)

        self.button_yess = Image.open("t.yess.png")
        self.button_yess = self.button_yess.resize((260,75), Image.LANCZOS)
        self.button_photo = ImageTk.PhotoImage(self.button_yess)

        # tombol label untuk ke welcome page
        self.button_labelyess = tk.Label(self, image=self.button_photo, borderwidth=0)
        self.button_labelyess.place(x=980, y=350)

        self.button_labelyess.bind("<Button-1>", self.go_to_search)

    def go_to_search(self, event):
        self.destroy()  
        search_page = HomePage()
        search_page.mainloop()

    def go_to_login(self, event):
        self.destroy()
        login_page = LoginPage()
        login_page.mainloop()


# Halaman login untuk admin menginput username dan password
class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Login Admin')
        self.geometry('1278x700')
        self.resizable(False,False)

        login1 = Image.open('login.png')
        login = login1.resize((1278,700))
        self.bg_login = ImageTk.PhotoImage(login)

        self.label_login = tk.Label(self, image=self.bg_login, bg='white', bd=0)
        self.label_login.place(x=0, y=0)

        self.entry_username = tk.Entry(self, width= 25, borderwidth= 0)
        self.entry_username.config(font=("Arial", 17))
        self.entry_username.place(x= 480, y=340)

        self.entry_password = tk.Entry(self, show="*", width=25, borderwidth= 0)
        self.entry_password.config(font=("Arial", 17))
        self.entry_password.place(x= 480, y= 470)

        self.button_login = Image.open("tlogin.png")
        self.button_login = self.button_login.resize((115,37), Image.LANCZOS)
        self.button_photologin = ImageTk.PhotoImage(self.button_login)

        self.login_button = tk.Label(self, image=self.button_photologin, borderwidth=0)
        self.login_button.place(x=606, y=535)

        self.login_button.bind("<Button-1>", self.check_login)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70,25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=107, y=95)

        self.back_button.bind("<Button-1>", self.go_back)

    def go_back(self, event):
        self.destroy()
        awalan_page = AwalanPage()
        awalan_page.mainloop()

    def check_login(self, password):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin12":
            self.destroy()
            datakos_page = MainAdmin()
            datakos_page.mainloop()
        else:
            messagebox.showerror("Error", "Username atau password salah")


# Halaman menu untuk admin
class MainAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Halaman Admin')
        self.geometry('1278x700')
        self.resizable(False,False)

        img_admin = Image.open('main admin.png')
        img_hal = img_admin.resize((1278,700))
        self.bg_home = ImageTk.PhotoImage(img_hal)

        self.label_home = tk.Label(self, image=self.bg_home, bg='white', bd=0)
        self.label_home.place(x=0, y=0)

        # tombol tombol ke search dan sorting
        self.button = Image.open("tclick.png")
        self.button = self.button.resize((105,22), Image.LANCZOS)
        self.button_photo = ImageTk.PhotoImage(self.button)

        self.add_button = tk.Label(self, image=self.button_photo, borderwidth= 0)
        self.add_button.place(x=342, y=560)
        self.add_button.bind("<Button-1>", self.go_to_add)

        self.search_button = tk.Label(self, image=self.button_photo, borderwidth= 0)
        self.search_button.place(x=848, y=560)
        self.search_button.bind("<Button-1>", self.go_to_list)

        # Tombol Back
        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70,25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=82, y=62)
        self.back_button.bind("<Button-1>", self.go_back)

    def go_back(self, event):
        self.destroy()
        awalan_page = AwalanPage()
        awalan_page.mainloop()

    def go_to_add(self, event):
        self.destroy()  # Close the current window
        search_page = datakos()
        search_page.mainloop()

    def go_to_list(self, event):
        self.destroy()  # Close the current window
        search_page = bookingkos()
        search_page.mainloop()


class Node:
    def __init__(self, data): # menginisialisasi node yang masih kosong
        self.data = data
        self.prev = None
        self.next = None


# Halaman daftar kos yang telah dibooking
class bookingkos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Data Booking Kos')
        self.geometry('1278x700')
        self.resizable(False, False)

        img_list = Image.open('bg booking.png')
        img_hal = img_list.resize((1278, 700))
        self.bg_list = ImageTk.PhotoImage(img_hal)

        self.label_list = tk.Label(self, image=self.bg_list, bg='white', borderwidth=0)
        self.label_list.place(x=0, y=0)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1132, y=63)
        self.back_button.bind("<Button-1>", self.go_back1)

        self.tree = ttk.Treeview(self, show='headings', columns=("Nama", "Phone", "Booking Date", "Nama Kos"))

        self.tree.column("Nama", anchor=tk.CENTER, width=10, stretch=tk.YES)
        self.tree.column("Phone", anchor=tk.CENTER, width=100, stretch=tk.YES)
        self.tree.column("Booking Date", anchor=tk.CENTER, width=100, stretch=tk.YES)
        self.tree.column("Nama Kos", anchor=tk.CENTER, width=10, stretch=tk.YES)

        self.tree.heading("Nama", text="Nama", anchor=tk.CENTER)
        self.tree.heading("Phone", text="Phone", anchor=tk.CENTER)
        self.tree.heading("Booking Date", text="Booking Date", anchor=tk.CENTER)
        self.tree.heading("Nama Kos", text="Nama Kos", anchor=tk.CENTER)

        self.tree.place(x=135, y=160, width=1010, height=400)  # Adjusting the size and position

        # Set font for Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=30, borderwidth=0, bg = "fffef8", fieldbg = "fffef8")  # Change font and row height
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), bg = "fffef8")  # Change heading font
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.booking_list = DoublyLinkedList()
        self.load_csv_data()

    def load_csv_data(self):
        if not os.path.exists("data_bookings.csv"):
            messagebox.showerror("Error", "File data_bookings.csv tidak ditemukan")
            return

        with open("data_bookings.csv", newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Memeriksa apakah baris tidak kosong
                    if len(row) >= 4:  # Memeriksa apakah baris memiliki setidaknya 4 elemen
                        booking_data = {"Nama": row[0], "No. Handphone": row[1], "Tanggal Booking": row[2], "Nama Kos": row[3]}
                        self.booking_list.insert(booking_data)
                        self.tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3]))
                    else:
                        print("Data tidak lengkap:", row)
                else:
                    print("Baris kosong")

    def go_back1(self, event):
        self.destroy()
        awalan_page = MainAdmin()
        awalan_page.mainloop()
        

# Halaman admin untuk menginput data kos
class datakos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Data Kos')
        self.geometry('1278x700')
        self.resizable(False,False)

        datakos1 = Image.open('datakos.png')
        datakos = datakos1.resize((1278,700))
        self.bg_datakos = ImageTk.PhotoImage(datakos)

        self.label_datakos = tk.Label(self, image=self.bg_datakos, bg= "white", bd=0)
        self.label_datakos.place(x=0, y=0)

        # Entry nama kos
        self.nama_entry = tk.Entry(self, width=60, borderwidth= 0, bg = "#fffef8")
        self.nama_entry.config(font=("Arial", 15))
        self.nama_entry.place(x=480, y=132)

        # Entry harga
        self.harga_entry = tk.Entry(self, width=60, borderwidth= 0,  bg = "#fffef8")
        self.harga_entry.config(font=("Arial", 15))
        self.harga_entry.place(x=480, y=187)

        # Entry wilayah
        self.wilayah_entry = tk.Text(self, height= 1, width=30, borderwidth= 0,  bg = "#fffef8")
        self.wilayah_entry.config(font=("Arial", 15))
        self.wilayah_entry.place(x=480, y=244)

        # Entry no telepon
        self.no_telp_entry = tk.Entry(self, width=60, borderwidth= 0,  bg = "#fffef8")
        self.no_telp_entry.config(font=("Arial", 15))
        self.no_telp_entry.place(x=480, y=299)

        # Entry kamar kosong
        self.kamar_combobox = ttk.Combobox(self, values=['1 kamar', '2 kamar', '3 kamar', '4 kamar', '5 kamar', '6 kamar',
                                                         '7 kamar', '8 kamar', '9 kamar', '10 kamar'], width= 58)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TCombobox',
                        fieldbackground='#fffef8',
                        background='#fffef8',
                        selectbackground='#fffef8',
                        selectforeground='#fffef8',
                        borderwidth= 0)
        
        self.kamar_combobox.config(font = ("Arial", 15))
        self.kamar_combobox.place(x=480, y=356)


        # Entry fasilitas kos
        self.fasilitas_entry = tk.Text(self, height=1, width=60, borderwidth= 0,  bg = '#fffef8')
        self.fasilitas_entry.config(font=("Arial", 15))
        self.fasilitas_entry.place(x=480, y=410)

        # Checkbutton jenkel kos
        self.pria_var = tk.BooleanVar()
        self.pria_checkbox = tk.Checkbutton(self, text='Pria', variable=self.pria_var, width=10, height= 2, borderwidth= 0, bg = '#d1dde2')
        self.pria_checkbox.config(font=("Arial", 15, "bold"))
        self.pria_checkbox.place(x=480, y=450)
        
        self.wanita_var = tk.BooleanVar()
        self.wanita_checkbox = tk.Checkbutton(self, text='Wanita', variable=self.wanita_var, width=15, height= 2, borderwidth= 0, bg = '#d1dde2')
        self.wanita_checkbox.config(font=("Arial", 15, "bold"))
        self.wanita_checkbox.place(x=670, y=450)
        
        self.campur_var = tk.BooleanVar()
        self.campur_checkbox = tk.Checkbutton(self, text='Campur', variable=self.campur_var, width=15, height= 2, borderwidth= 0, bg = '#d1dde2')
        self.campur_checkbox.config(font=("Arial", 15,"bold"))
        self.campur_checkbox.place(x=900, y=450)
        

        # Entry jarak ke kos
        self.jarak_entry = tk.Entry(self, width=60, borderwidth= 0,  bg = "#fffef8")
        self.jarak_entry.config(font=("Arial", 15))
        self.jarak_entry.place(x=480, y=520)

        # Entry gambar kos
        self.gambar_entry = tk.Entry(self, width=58, state='readonly', borderwidth= 0)
        self.gambar_entry.config(font=("Arial", 12))
        self.gambar_entry.place(x=480, y=579)
        
        self.gambar_button = tk.Button(self, text='Pilih Gambar', command=self.choose_image, width= 10, bg = "#fffef8", border= 1)
        self.gambar_button.config(font=("Arial", 11, "bold"))
        self.gambar_button.place(x=1020, y= 573)

        # tombol submit
        self.button_submit = Image.open("tsubmit.png")
        self.button_submit = self.button_submit.resize((90,23), Image.LANCZOS)
        self.button_photosubmit = ImageTk.PhotoImage(self.button_submit)

        self.submit_button = tk.Label(self, image=self.button_photosubmit, borderwidth= 0)
        self.submit_button.place(x=670, y=653)

        self.submit_button.bind("<Button-1>", self.submit_data)

        # Tombol input ulang
        self.button_clear = Image.open("tclear.png")
        self.button_clear = self.button_clear.resize((80,23), Image.LANCZOS)
        self.button_photoclear = ImageTk.PhotoImage(self.button_clear)

        self.clear_button = tk.Label(self, image=self.button_photoclear,borderwidth=0)
        self.clear_button.place(x=847, y=653)

        self.clear_button.bind("<Button-1>", self.clear_input)
        
        # Tombol Back
        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1090, y=55)

        self.back_button.bind("<Button-1>", self.go_back)

    def go_back(self, event):
        self.destroy()
        awalan_page = MainAdmin()
        awalan_page.mainloop()
    
    # menghapus semua data yg di inputkan sebelumnya (button clear)
    def clear_input(self, event):
        self.nama_entry.delete(0, tk.END)
        self.harga_entry.delete(0, tk.END)
        self.wilayah_entry.delete('1.0', tk.END)
        self.no_telp_entry.delete(0, tk.END)
        self.fasilitas_entry.delete('1.0', tk.END)
        self.kamar_combobox.set('')
        self.pria_var.set(False)
        self.wanita_var.set(False)
        self.campur_var.set(False)
        self.jarak_entry.delete(0, tk.END)
        self.gambar_entry.delete(0, tk.END)

    # mengambil gambar di file dalam device admin (pilih gambar)
    def choose_image(self):
        filenama = filedialog.askopenfilename(initialdir="/", title="Pilih Gambar", filetypes=(("Image Files", "*.png *.jpg *.jpeg *.gif"),))
        self.gambar_entry.config(state='normal')
        self.gambar_entry.delete(0, tk.END)
        self.gambar_entry.insert(0, filenama)
        self.gambar_entry.config(state='readonly')

    # Membuat kode unik secara random 
    def generate_unique_code(self):
        existing_codes = set(pd.read_csv(CSV_FILE)['Kode Unik'])
        while True:
            code = str(random.randint(1000, 9999))
            if code not in existing_codes:
                return code

    # Memasukkan data kedalam file csv
    def submit_data(self, event):
        # Mengambil data dari entry yang telah diinputkan
        nama = self.nama_entry.get().strip()
        harga = self.harga_entry.get().strip()
        wilayah = self.wilayah_entry.get('1.0', tk.END).strip()
        no_telp = self.no_telp_entry.get().strip()
        kamar = self.kamar_combobox.get().strip()
        fasilitas = self.fasilitas_entry.get('1.0', tk.END).strip()
        gender = [jenis for jenis, var in zip(['Pria', 'Wanita', 'Campur'], [self.pria_var, self.wanita_var, self.campur_var]) if var.get()]
        jarak = self.jarak_entry.get().strip()
        gambar = self.gambar_entry.get().strip()
        kode_unik = self.generate_unique_code()

        if any(not value for value in [nama, harga, wilayah, no_telp, kamar, fasilitas]):
            messagebox.showerror('Error', 'Mohon isi semua kolom')
            return

        data = {
            'Kode Unik': [kode_unik],
            'Nama Kos': [nama],
            'Harga': [harga],
            'Wilayah': [wilayah],
            'No HP': [no_telp],
            'Kamar Kosong': [kamar],
            'Fasilitas': [fasilitas],
            'Jenis Kelamin': [', '.join(gender)],
            'Jarak ke UNESA': [jarak],
            'Gambar': [gambar]
        }

        # Menginput data yang telah diambil ke dalam file csv
        df = pd.DataFrame(data)
        df.to_csv(CSV_FILE, index=False, mode='a', header=not pd.read_csv(CSV_FILE, encoding='latin-1').index.any())
        messagebox.showinfo('Informasi', 'Data berhasil disimpan')
        self.clear_input()


# Halaman menu untuk user
class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Halaman Utama')
        self.geometry('1278x700')
        self.resizable(False,False)


        img_hal1 = Image.open('main page.png')
        img_hal = img_hal1.resize((1278,700))
        self.bg_home = ImageTk.PhotoImage(img_hal)

        self.label_home = tk.Label(self, image=self.bg_home, bg='white', bd=0)
        self.label_home.place(x=0, y=0)

        # tombol tombol ke search dan sorting
        self.button_search = Image.open("tclick.png")
        self.button_search = self.button_search.resize((105,22), Image.LANCZOS)
        self.button_photosearch = ImageTk.PhotoImage(self.button_search)

        self.search_button = tk.Label(self, image=self.button_photosearch, borderwidth= 0)
        self.search_button.place(x=863, y=304)
        self.search_button.bind("<Button-1>", self.go_to_search)

        self.search_button = tk.Label(self, image=self.button_photosearch, borderwidth= 0)
        self.search_button.place(x=355, y=585)
        self.search_button.bind("<Button-1>", self.go_to_unesa)
        
        self.search_button = tk.Label(self, image=self.button_photosearch, borderwidth= 0)
        self.search_button.place(x=863, y=585)
        self.search_button.bind("<Button-1>", self.go_to_price)

        # Tombol Back
        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((65,25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=70, y=65)

        self.back_button.bind("<Button-1>", self.go_back)

    def go_back(self, event):
        self.destroy()
        awalan_page = AwalanPage()
        awalan_page.mainloop()

    def go_to_search(self, event):
        self.destroy()  # Close the current window
        search_page = SearchForm()
        search_page.mainloop()

    def go_to_unesa(self, event):
        self.destroy()  # Close the current window
        search_page = SortDistance()
        search_page.mainloop()

    def go_to_price(self, event):
        self.destroy()  # Close the current window
        search_page = SortPrice()
        search_page.mainloop()


# Membuat node (tipe data dll)
class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    # memasukan data baru ke pohon biner
    def insert(self, data):
        if self.data is not None:
            if data["Nama Kos"] < self.data["Nama Kos"]:  # mencocokan node, jika kurang dari maka di kiri
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data) #rekursif
            elif data["Nama Kos"] > self.data["Nama Kos"]:  #mencocokan node, jika lebih dari maka di kiri
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data) #rekursif
        else:
            self.data = data 

    @classmethod
    def build_binary_tree(cls, df):
        root = None
        for index, row in df.iterrows():
            if root is None:
                root = cls(row)
            else:
                root.insert(row)
        return root


    def search(self, key, search_by_region=False):
        key = key.lower()
        results = [] # menampung hasil pencarian
        if search_by_region:
            if key in self.data["Wilayah"].lower(): # menjaci data berdasarkan wilayah
                results.append(self.data)
        else:
            if key in self.data["Nama Kos"].lower(): # mencari data berdasarkan nama kos
                results.append(self.data)

        # menambahkan data berdasarkan wilayah yang masih ada
        if self.left is not None:
            results += self.left.search(key, search_by_region) 
        if self.right is not None:
            results += self.right.search(key, search_by_region)

        return results


class DoublyLinkedList: 
    def __init__(self): #data baru akan ditetapkan head dan tail
        self.head = None 
        self.tail = None

    def insert(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node


# halaman search berdasarkan wilayah
class SearchForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Pencarian Kos')
        self.geometry('1278x700')
        self.resizable(False,False)
        self.current_page = 0
        self.items_per_page = 15

        img_hal1 = Image.open('bg search.png')
        img_hal = img_hal1.resize((1278,700))
        self.bg_search = ImageTk.PhotoImage(img_hal)

        self.label_search = tk.Label(self, image=self.bg_search, bg='white', bd=0)
        self.label_search.place(x=0, y=0)

        # entry wilayah yg dicari
        self.alamat_entry = tk.Entry(self, width=25, bg = "#D1DDE2")
        self.alamat_entry.config(font=("Arial", 16))
        self.alamat_entry.place(x=650, y=60)

        # tombol search
        self.button_search = Image.open("tsearch.png")
        self.button_search = self.button_search.resize((90, 30), Image.LANCZOS)
        self.button_photosearch = ImageTk.PhotoImage(self.button_search)

        self.search_label = tk.Label(self, image=self.button_photosearch, borderwidth=0)
        self.search_label.place(x=1005, y=60)

        self.search_label.bind("<Button-1>", self.search_alamat)
    
        self.result_frame = tk.Frame(self, bg="#D1DDE5")
        self.result_frame.place(x=73, y=150)

        self.button_prev = Image.open("t.prev.png")
        self.button_prev = self.button_prev.resize((80,27), Image.LANCZOS)
        self.button_photoprev = ImageTk.PhotoImage(self.button_prev)

        self.prev_label = tk.Label(self, image=self.button_photoprev, borderwidth=0)
        self.prev_label.place(x=48, y=640)

        self.prev_label.bind("<Button-1>", self.prev_page)

        self.button_next = Image.open("tnext.png")
        self.button_next = self.button_next.resize((80,27), Image.LANCZOS)
        self.button_photonext = ImageTk.PhotoImage(self.button_next)

        self.next_label = tk.Label(self, image=self.button_photonext, borderwidth=0)
        self.next_label.place(x=1149, y=640)

        self.next_label.bind("<Button-1>", self.next_page)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70,25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1132, y=64)

        self.back_button.bind("<Button-1>", self.go_back1)

        self.button_reset = Image.open("reset.png")
        self.button_reset = self.button_reset.resize((80, 27), Image.LANCZOS)
        self.button_photoreset = ImageTk.PhotoImage(self.button_reset)

        self.reset_button = tk.Label(self, image=self.button_photoreset, borderwidth=0)
        self.reset_button.place(x=600, y=640)

        self.reset_button.bind("<Button-1>", self.go_reset)

        self.image_frames = []
        self.root = None
        self.show_all_data()

    def go_back1(self, event):
        self.destroy()
        awalan_page = HomePage()
        awalan_page.mainloop()

    def go_reset(self, event):
        self.destroy()
        awalan_page = SearchForm()
        awalan_page.mainloop()

    def next_page(self, event):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.show_all_data()

    def prev_page(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_all_data()

    def search_alamat(self, event):
        self.clear_result()
        search_query = self.alamat_entry.get()
        if not search_query:
            messagebox.showerror('Error', 'Wilayah atau Nama Kos harus diisi')
            return
        if self.root is None:
            messagebox.showerror('Error', 'Data tidak ditemukan')
            return

        # menampilkan data hasil kos
        search_by_region = False
        try:
            df = pd.read_csv(CSV_FILE)
            if search_query.lower() in df["Wilayah"].str.lower().values:
                search_by_region = True
        except FileNotFoundError:
            messagebox.showerror('Error', 'File CSV tidak ditemukan')
            return
        
        # mencocokan yang disearch di binary tree
        results = self.root.search(search_query, search_by_region=search_by_region)
        if not results:
            messagebox.showinfo('Info', 'Tidak ada kos dengan wilayah atau nama tersebut')
            return

        self.filtered_results = pd.DataFrame(results)
        self.total_filtered_results = len(results)
        self.current_page = 0
        self.show_all_data()

    def show_all_data(self):
        try:
            if hasattr(self, 'filtered_results'):
                start_index = self.current_page * self.items_per_page
                end_index = min(start_index + self.items_per_page, self.total_filtered_results)
                self.display_kos_info(self.filtered_results[start_index:end_index])
                total_results = self.total_filtered_results
            else:
                df = pd.read_csv(CSV_FILE)
                if self.root is None:
                    self.root = Node.build_binary_tree(df)
                start_index = self.current_page * self.items_per_page
                end_index = min(start_index + self.items_per_page, len(df))
                self.display_kos_info(df[start_index:end_index])
                total_results = len(df)
            
            self.total_pages = (total_results + self.items_per_page - 1) // self.items_per_page
            self.update_button_states()

        except FileNotFoundError:
            messagebox.showerror('Error', 'File CSV tidak ditemukan')

    def update_button_states(self):
        # Update state tombol "Next"
        if self.current_page >= self.total_pages - 1:
            self.next_label.config(state=tk.DISABLED, color = 'none')
        else:
            self.next_label.config(state=tk.NORMAL)
        
        # Update state tombol "Prev"
        if self.current_page <= 0:
            self.prev_label.config(state=tk.DISABLED, color = 'none')
        else:
            self.prev_label.config(state=tk.NORMAL)
            

    # Menampilkan kos
    def display_kos_info(self, kos_info):
        self.clear_result()
        count = 0
        for index, row in kos_info.iterrows():
            nama_kos = textwrap.fill(f'Nama Kos: {row["Nama Kos"]}', width=28)
            harga = textwrap.fill(f'Harga: {row["Harga"]}', width=28)
            wilayah = textwrap.fill(f'Wilayah: {row["Wilayah"]}', width=28)
            kamar_kosong =textwrap.fill(f'Kamar Kosong: {row["Kamar kosong"]}', width=28)
            jenis_kelamin = textwrap.fill(f'Jenis Kelamin: {row["Jenis Kelamin"]}', width=28)

            result_str = f'{nama_kos}\n{harga}\n{wilayah}\n{kamar_kosong}\n{jenis_kelamin}\n\n'

            result_text = tk.Text(self.result_frame, height=8, width=29, borderwidth= 0, font=("Arial", 10, "bold"))
            result_text.insert(tk.END, result_str)
            result_text.config(state="disabled")
            result_text.grid(row=count // 5, column=count % 5, padx=11, pady=11, )
            
            image_path = row.get("Foto", "")
            if image_path and os.path.exists(image_path):
                image_button = tk.Button(self.result_frame, text="Gambar Kos", bg="#D1DDE2", border=0,
                command=lambda r=row: self.show_image(r, image_path))
                image_button.grid(row=count // 5, column=count % 5, sticky="s", pady=25)
            count += 1

    #  Halaman informasi kos
    def show_image(self, row, image_paths):
        if not os.path.exists(image_paths):
            messagebox.showerror("Error", "Gambar tidak ditemukan")
            return

        img_inform = Image.open('bg info.png')
        self.resizable(False, False)
        img_inform_kos = img_inform.resize((1278,700))
        self.bg_inform = ImageTk.PhotoImage(img_inform_kos)

        self.label_inform = tk.Label(self, image=self.bg_inform, bg='white', bd=0)
        self.label_inform.place(x=0, y=0)

        kos_image = Image.open(image_paths)
        kos_image = kos_image.resize((800, 500), Image.LANCZOS)
        kos_photo = ImageTk.PhotoImage(kos_image)

        self.kos_label = tk.Label(self, image=kos_photo, bg='white', bd=0)
        self.kos_label.image = kos_photo  
        self.kos_label.place(x=70, y=130)

        details_nama = (f'{row["Nama Kos"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_nama)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=200)

        details_harga = (f'{row["Harga"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_harga)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=258)

        details_wilayah = (f'{row["Wilayah"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_wilayah)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=318)

        details_jenkel = (f'{row["Jenis Kelamin"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_jenkel)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=369)

        details_kamarkosong = (f'{row["Jarak ke UNESA"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_kamarkosong)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1015, y=428)

        details_fasilitas = (f'{row["Fasilitas"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=19, height= 5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_fasilitas)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1010, y=485)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1090, y=50)
        self.back_button.bind("<Button-1>", self.go_back)

        self.button_booking = Image.open("tbook.png")
        self.button_booking = self.button_booking.resize((100, 35), Image.LANCZOS)
        self.button_photobooking = ImageTk.PhotoImage(self.button_booking)

        self.booking_button = tk.Label(self, image=self.button_photobooking, borderwidth=0)
        self.booking_button.place(x=1037, y=621)
        self.booking_button.bind("<Button-1>", lambda event: self.go_booking1(row["Nama Kos"], row["No HP"]))

    def go_back(self, event):
        self.destroy()
        awalan_page = SearchForm()
        awalan_page.mainloop()
    
    def go_booking1(self, nama_kos, no_hp):
            self.destroy()
            awalan_page = BookingForm(nama_kos, no_hp)
            awalan_page.mainloop()

    def clear_result(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()


# Halaman sorting berdasarkan Jarak 
class SortDistance(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sorting Jarak')
        self.geometry('1278x700')
        self.resizable(False, False)
        self.current_page = 0
        self.items_per_page = 15

        img_hal1 = Image.open('bg dist.png')
        img_hal = img_hal1.resize((1278, 700))
        self.bg_search = ImageTk.PhotoImage(img_hal)

        self.label_search = tk.Label(self, image=self.bg_search, bg='white', bd=0)
        self.label_search.place(x=0, y=0)

        self.result_frame = tk.Frame(self, bg="#D1DDE2")
        self.result_frame.place(x=73, y=150)

        self.button_prev2 = Image.open("t.prev.png")
        self.button_prev2 = self.button_prev2.resize((80, 27), Image.LANCZOS)
        self.button_photoprev2 = ImageTk.PhotoImage(self.button_prev2)

        self.prev_label2 = tk.Label(self, image=self.button_photoprev2, borderwidth=0)
        self.prev_label2.place(x=40, y=640)
        self.prev_label2.bind("<Button-1>", self.prev_page2)

        self.button_next2 = Image.open("tnext.png")
        self.button_next2 = self.button_next2.resize((80, 27), Image.LANCZOS)
        self.button_photonext2 = ImageTk.PhotoImage(self.button_next2)

        self.next_label2 = tk.Label(self, image=self.button_photonext2, borderwidth=0)
        self.next_label2.place(x=1155, y=640)
        self.next_label2.bind("<Button-1>", self.next_page2)

        self.button_back2 = Image.open("tback.png")
        self.button_back2 = self.button_back2.resize((70, 25), Image.LANCZOS)
        self.button_photoback2 = ImageTk.PhotoImage(self.button_back2)

        self.back_button2 = tk.Label(self, image=self.button_photoback2, borderwidth=0)
        self.back_button2.place(x=1135, y=64)
        self.back_button2.bind("<Button-1>", self.go_back2)

        # Memanggil fungsi untuk menampilkan data terurut
        self.load_and_display_sorted_data()

    def go_back2(self, event):
        self.destroy()
        awalan_page = HomePage()
        awalan_page.mainloop()

    def next_page2(self, event):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_and_display_sorted_data()

    def prev_page2(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_and_display_sorted_data()

    def read_csv(self, filepath):
        with open(filepath, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read header
            data = [row for row in csv_reader]
        return header, data

    def extract_distances(self, data, distance_index):
        distances = []
        for row in data:
            distance_str = row[distance_index].replace(',', '.')
            if ' km' in distance_str:
                distance = float(distance_str.replace(' km', ''))
            elif ' m' in distance_str:
                distance = float(distance_str.replace(' m', '')) / 1000.0
            else:
                continue  
            distances.append((distance, row[0])) # buat kode unik
        return distances

    # Mengurutkan berdasarkan jarak
    def bucket_sort(self, values):
        if not values:
            return []

        max_value = max(values, key=lambda x: x[0])[0]
        min_value = min(values, key=lambda x: x[0])[0]
        bucket_count = len(values)
        size = (max_value - min_value) / bucket_count

        buckets = [[] for _ in range(bucket_count)]

        for value in values:
            index = int((value[0] - min_value) / size)
            if index != bucket_count:
                buckets[index].append(value)
            else:
                buckets[bucket_count - 1].append(value)

        sorted_values = []
        for bucket in buckets:
            sorted_values.extend(sorted(bucket, key=lambda x: x[0]))

        return sorted_values

    # Menampilkan data yang telah terurut berdasarkan jaraknya
    def sort_data_by_distances(self, data, sorted_distances, distance_index):
        distance_to_data = {}
        for row in data:
            unique_code = row[0]
            distance_str = row[distance_index].replace(',', '.')
            if ' km' in distance_str:
                distance = float(distance_str.replace(' km', ''))
            elif ' m' in distance_str:
                distance = float(distance_str.replace(' m', '')) / 1000.0
            else:
                continue  # If neither 'km' nor 'm' is found, skip this row
            distance_to_data[(distance, unique_code)] = row

        sorted_data = [distance_to_data[distance] for distance in sorted_distances]
        return sorted_data

    # Memuat data data terurut
    def load_and_display_sorted_data(self):
        input_filename = "data_kos.csv"

        header, data = self.read_csv(input_filename)
        distance_index = header.index('Jarak ke UNESA')  # Adjust to the name of the distance column

        distances = self.extract_distances(data, distance_index)
        sorted_distances = self.bucket_sort(distances)

        sorted_data = self.sort_data_by_distances(data, sorted_distances, distance_index)

        df_sorted = pd.DataFrame(sorted_data, columns=header)

        self.total_pages = (len(df_sorted) + self.items_per_page - 1) // self.items_per_page

        self.display_data(df_sorted)
        self.update_button_states()

    # Menapilkan data terurut dalam bentuk text box data terurut
    def display_data(self, sorted_df):
        self.clear_result()

        start_index = self.current_page * self.items_per_page
        count = 0
        for index in range(start_index, len(sorted_df)):
            if count >= self.items_per_page:
                break

            row = sorted_df.iloc[index]

            # Membungkus teks menggunakan textwrap.fill
            nama_kos = textwrap.fill(f'Nama Kos: {row["Nama Kos"]}', width=28)
            jarak_ke_unesa = textwrap.fill(f'Jarak ke UNESA: {row["Jarak ke UNESA"]}', width=28)
            harga = textwrap.fill(f'Harga: {row["Harga"]}', width=28)
            kamar_kosong = textwrap.fill(f'Kamar Kosong: {row["Kamar kosong"]}', width=28)
            jenis_kelamin = textwrap.fill(f'Jenis Kelamin: {row["Jenis Kelamin"]}', width=28)
            
            result_str = f'{nama_kos}\n{jarak_ke_unesa}\n{harga}\n{kamar_kosong}\n{jenis_kelamin}\n\n'

            result_text = tk.Text(self.result_frame, height=8, width=29, borderwidth=0, font=("Arial", 10, "bold"))
            result_text.insert(tk.END, result_str)
            result_text.config(state="disabled")
            result_text.grid(row=count // 5, column=count % 5, padx=11, pady=11)

            image_path = row.get("Foto", "")
            if image_path and os.path.exists(image_path):
                image_button = tk.Button(self.result_frame, text="Gambar Kos", bg="#D1DDE2", border=0, command=lambda r=row: self.show_image(r, image_path))
                image_button.grid(row=count // 5, column=count % 5, sticky="s", pady=17)
            count += 1

    def clear_result(self):
            for widget in self.result_frame.winfo_children():
                widget.destroy() 

    # Halaman informasi kos
    def show_image(self, row, image_paths):
        if not os.path.exists(image_paths):
            messagebox.showerror("Error", "Gambar tidak ditemukan")
            return

        img_inform = Image.open('bg info.png')
        self.resizable(False, False)
        img_inform_kos = img_inform.resize((1278, 700))
        self.bg_inform = ImageTk.PhotoImage(img_inform_kos)

        self.label_inform = tk.Label(self, image=self.bg_inform, bg='white', bd=0)
        self.label_inform.place(x=0, y=0)

        kos_image = Image.open(image_paths)
        kos_image = kos_image.resize((800, 500), Image.LANCZOS)
        kos_photo = ImageTk.PhotoImage(kos_image)

        self.kos_label = tk.Label(self, image=kos_photo, bg='white', bd=0)
        self.kos_label.image = kos_photo  
        self.kos_label.place(x=70, y=130)

        details_nama = (f'{row["Nama Kos"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_nama)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=200)

        details_harga = (f'{row["Harga"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_harga)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=258)

        details_wilayah = (f'{row["Wilayah"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_wilayah)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=318)

        details_jenkel = (f'{row["Jenis Kelamin"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_jenkel)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1000, y=369)

        details_kamarkosong = (f'{row["Jarak ke UNESA"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_kamarkosong)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1015, y=428)

        details_fasilitas = (f'{row["Fasilitas"]}\n')
        self.details_text = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=19, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text.insert(tk.END, details_fasilitas)
        self.details_text.configure(state='disabled')
        self.details_text.place(x=1010, y=485)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1090, y=50)

        self.back_button.bind("<Button-1>", self.go_back)

        self.button_booking = Image.open("tbook.png")
        self.button_booking = self.button_booking.resize((100, 35), Image.LANCZOS)
        self.button_photobooking = ImageTk.PhotoImage(self.button_booking)

        self.booking_button = tk.Label(self, image=self.button_photobooking, borderwidth=0)
        self.booking_button.place(x=1037, y=621)

        self.booking_button.bind("<Button-1>", lambda event: self.go_booking2(row["Nama Kos"], row["No HP"]))

    def go_back(self, event):
        self.destroy()
        awalan_page = SortDistance()
        awalan_page.mainloop()

    def go_booking2(self, nama_kos, no_hp):
        self.destroy()
        awalan_page = BookingForm(nama_kos, no_hp)
        awalan_page.mainloop()

    def clear_result(self):
            for widget in self.result_frame.winfo_children():
                widget.destroy() 

    # Pengaturan prev dan back button
    def update_button_states(self):
        self.prev_label2.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED, color = 'none')
        self.next_label2.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED, color = 'none')


# Halaman sorting berdasarkan harga
class SortPrice(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sorting Harga')
        self.geometry('1278x700')
        self.resizable(False, False)
        self.current_page = 0
        self.items_per_page = 15

        img_hal1 = Image.open('bg price.png')
        img_hal = img_hal1.resize((1278, 700))
        self.bg_search = ImageTk.PhotoImage(img_hal)

        self.label_search = tk.Label(self, image=self.bg_search, bg='white', bd=0)
        self.label_search.place(x=0, y=0)

        self.result_frame = tk.Frame(self, bg="#D1DDE2")
        self.result_frame.place(x=73, y=150)

        self.button_prev2 = Image.open("t.prev.png")
        self.button_prev2 = self.button_prev2.resize((80, 27), Image.LANCZOS)
        self.button_photoprev2 = ImageTk.PhotoImage(self.button_prev2)

        self.prev_label2 = tk.Label(self, image=self.button_photoprev2, borderwidth=0)
        self.prev_label2.place(x=40, y=640)

        self.prev_label2.bind("<Button-1>", self.prev_page2)

        self.button_next2 = Image.open("tnext.png")
        self.button_next2 = self.button_next2.resize((80, 27), Image.LANCZOS)
        self.button_photonext2 = ImageTk.PhotoImage(self.button_next2)

        self.next_label2 = tk.Label(self, image=self.button_photonext2, borderwidth=0)
        self.next_label2.place(x=1155, y=640)

        self.next_label2.bind("<Button-1>", self.next_page2)

        self.button_back2 = Image.open("tback.png")
        self.button_back2 = self.button_back2.resize((70, 25), Image.LANCZOS)
        self.button_photoback2 = ImageTk.PhotoImage(self.button_back2)

        self.back_button2 = tk.Label(self, image=self.button_photoback2, borderwidth=0)
        self.back_button2.place(x=1135, y=64)

        self.back_button2.bind("<Button-1>", self.go_back2)

        # Call function to display sorted data
        self.load_and_display_sorted_data()

    def go_back2(self, event):
        self.destroy()
        awalan_page = HomePage()
        awalan_page.mainloop()

    def next_page2(self, event):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_and_display_sorted_data()

    def prev_page2(self, event):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_and_display_sorted_data()
    
    def update_button_states(self):
        self.prev_label2.config(state=tk.NORMAL if self.current_page > 0 else tk.DISABLED, color = 'none')
        self.next_label2.config(state=tk.NORMAL if self.current_page < self.total_pages - 1 else tk.DISABLED, color = 'none')

    def read_csv(self, filepath):
        # Read CSV file and return header and data
        with open(filepath, mode='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read header
            data = [row for row in csv_reader]
        return header, data

    def extract_prices(self, data, Harga):
        """Extract prices from data based on the price column index and remove thousand separators."""
        prices = [float(row[Harga].replace('.', '').replace(',', '.')) for row in data]
        return prices

    def bucket_sort(self, prices):
        """Sort prices using bucket sort algorithm."""
        if not prices:
            return []

        max_value = max(prices)
        min_value = min(prices)
        bucket_count = len(prices)
        size = (max_value - min_value) / bucket_count

        buckets = [[] for _ in range(bucket_count)]

        for price in prices:
            index = int((price - min_value) / size)
            if index != bucket_count:
                buckets[index].append(price)
            else:
                buckets[bucket_count - 1].append(price)

        sorted_prices = []
        for bucket in buckets:
            sorted_prices.extend(sorted(bucket))

        return sorted_prices

    def sort_data_by_prices(self, data, sorted_prices, Harga, kode_unik):
        """Sort data based on sorted prices and ensure uniqueness based on unique code."""
    # Initialize dictionary to store data grouped by unique code
        code_to_data = {}

    # Iterate through data to group by unique code
        for row in data:
            code = row[kode_unik]  # Adjust to the actual column name of the unique code
            if code in code_to_data:
                code_to_data[code].append(row)
            else:
                code_to_data[code] = [row]

    # Initialize list to store sorted data
        sorted_data = []

    # Iterate through sorted prices and collect data in order
        for price in sorted_prices:
            for code in code_to_data:
                for item in code_to_data[code]:
                    if float(item[Harga].replace('.', '').replace(',', '.')) == price:
                        sorted_data.append(item)
                    # Remove item to ensure uniqueness
                        code_to_data[code].remove(item)
                        break

        return sorted_data


    def load_and_display_sorted_data(self):
        # Input file name
        input_filename = "data_kos.csv"

        # Read data from CSV file
        header, data = self.read_csv(input_filename)
        price_index = header.index('Harga')  # Adjust to the name of the price column
        kode_unik_index = header.index('Kode Unik')  # Adjust to the name of the unique code column

        # Extract and sort prices
        prices = self.extract_prices(data, price_index)
        sorted_prices = self.bucket_sort(prices)

        # Sort data based on sorted prices
        sorted_data = self.sort_data_by_prices(data, sorted_prices, price_index, kode_unik_index)

        # Create DataFrame from sorted data
        df_sorted = pd.DataFrame(sorted_data, columns=header)
        self.total_pages = (len(df_sorted) + self.items_per_page - 1) // self.items_per_page
        # Paginate and display sorted data
        self.display_data(df_sorted)
        self.update_button_states()

    def display_data(self, sorted_df):
        self.clear_result()

        # Get the data for the current page
        start_index = self.current_page * self.items_per_page
        end_index = start_index + self.items_per_page
        count = 0

        for index in range(start_index, end_index):
            if index >= len(sorted_df):
                break

            row = sorted_df.iloc[index]
            nama_kos = row["Nama Kos"]
            harga = row["Harga"]

            nama_kos = textwrap.fill(f'Nama Kos: {row["Nama Kos"]}', width=28)
            harga = textwrap.fill(f'Harga: {row["Harga"]}', width=28)
            wilayah = textwrap.fill(f'Wilayah: {row["Wilayah"]}', width=28)
            kamar_kosong = textwrap.fill(f'Kamar Kosong: {row["Kamar kosong"]}', width=28)
            jenis_kelamin = textwrap.fill(f'Jenis Kelamin: {row["Jenis Kelamin"]}', width=28)
            
            result_str = f'{nama_kos}\n{harga}\n{wilayah}\n{kamar_kosong}\n{jenis_kelamin}\n\n'

            result_text = tk.Text(self.result_frame, height=8 , width=29, borderwidth=0, font=("Arial", 10, "bold"))                                                             
            result_text.insert(tk.END, result_str)
            result_text.config(state="disabled")
            result_text.grid(row=count // 5, column=count % 5, padx=11, pady=11)

            image_path = row.get("Foto", "")
            if image_path and os.path.exists(image_path):
                image_button = tk.Button(self.result_frame, text="Gambar Kos", bg="#D1DDE2", border=0, command=lambda r=row: self.show_image(r, image_path))
                image_button.grid(row=count // 5, column=count % 5, sticky="s", pady=17)

            count += 1

    def clear_result(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

    def show_image(self, row, image_paths):
        if not os.path.exists(image_paths):
            messagebox.showerror("Error", "Gambar tidak ditemukan")
            return

        img_inform = Image.open('bg info.png')
        self.resizable(False, False)
        img_inform_kos = img_inform.resize((1278, 700))
        self.bg_inform = ImageTk.PhotoImage(img_inform_kos)

        self.label_inform = tk.Label(self, image=self.bg_inform, bg='white', bd=0)
        self.label_inform.place(x=0, y=0)

        kos_image = Image.open(image_paths)
        kos_image = kos_image.resize((800,500), Image.LANCZOS)
        kos_photo = ImageTk.PhotoImage(kos_image)

        self.kos_label = tk.Label(self, image=kos_photo, bg='white', bd=0)
        self.kos_label.image = kos_photo
        self.kos_label.place(x=70, y=130)

        details_nama = (f'{row["Nama Kos"]}\n')
        self.details_text_nama = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_nama.insert(tk.END, details_nama)
        self.details_text_nama.configure(state='disabled')
        self.details_text_nama.place(x=1000, y=200)

        details_harga = (f'{row["Harga"]}\n')
        self.details_text_harga = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_harga.insert(tk.END, details_harga)
        self.details_text_harga.configure(state='disabled')
        self.details_text_harga.place(x=1000, y=258)

        details_wilayah = (f'{row["Wilayah"]}\n')
        self.details_text_wilayah = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_wilayah.insert(tk.END, details_wilayah)
        self.details_text_wilayah.configure(state='disabled')
        self.details_text_wilayah.place(x=1000, y=318)

        details_jenkel = (f'{row["Jenis Kelamin"]}\n')
        self.details_text_jenkel = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_jenkel.insert(tk.END, details_jenkel)
        self.details_text_jenkel.configure(state='disabled')
        self.details_text_jenkel.place(x=1000, y=369)

        details_kamarkosong = (f'{row["Jarak ke UNESA"]}\n')
        self.details_text_kamarkosong = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=15, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_kamarkosong.insert(tk.END, details_kamarkosong)
        self.details_text_kamarkosong.configure(state='disabled')
        self.details_text_kamarkosong.place(x=1015, y=428)

        details_fasilitas = (f'{row["Fasilitas"]}\n')
        self.details_text_fasilitas = tk.Text(self, bg='white', font=("Arial", 15, "bold"), width=19, height=5, wrap=tk.WORD, borderwidth=0)
        self.details_text_fasilitas.insert(tk.END, details_fasilitas)
        self.details_text_fasilitas.configure(state='disabled')
        self.details_text_fasilitas.place(x=1010, y=485)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=1090, y=50)

        self.back_button.bind("<Button-1>", self.go_back)

        self.button_booking = Image.open("tbook.png")
        self.button_booking = self.button_booking.resize((100, 35), Image.LANCZOS)
        self.button_photobooking = ImageTk.PhotoImage(self.button_booking)

        self.booking_button = tk.Label(self, image=self.button_photobooking, borderwidth=0)
        self.booking_button.place(x=1037, y=621)

        self.booking_button.bind("<Button-1>", lambda event: self.go_booking3(row["Nama Kos"], row["No HP"]))

    def go_back(self, event):
        self.destroy()
        awalan_page = SortPrice()
        awalan_page.mainloop()

    def go_booking3(self, nama_kos, no_hp):
        self.destroy()
        awalan_page = BookingForm(nama_kos, no_hp)
        awalan_page.mainloop()

    def clear_result(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()


# Halaman formulir booking kos
class BookingForm(tk.Tk):
    def __init__(self, nama_kos, no_hp):
        super().__init__()
        self.title("Booking Form")
        self.geometry("1278x700")
        self.nama_kos = nama_kos
        self.no_hp = no_hp

        img_booking = Image.open('data book.png')
        self.resizable(False, False)
        img_booking_kos = img_booking.resize((1278,700))
        self.bg_book = ImageTk.PhotoImage(img_booking_kos)

        self.label_book = tk.Label(self, image=self.bg_book, bg='white', bd=0)
        self.label_book.place(x=0, y=0)
        
        # Membuat formulir untuk user dapat membooking kamar
        self.nama_entry = tk.Entry(self, font=("Arial", 12, "bold"), width= 30, borderwidth=0)
        self.nama_entry.place(x= 830, y= 280)
        
        self.phone_entry = tk.Entry(self, font=("Arial", 12, "bold"), width= 30, borderwidth=0)
        self.phone_entry.place(x= 830, y= 385)
        
        self.date_entry = tk.Entry(self, font=("Arial", 12, "bold"), width= 30, borderwidth=0)
        self.date_entry.place(x= 830, y=495)

        self.button_confirm = Image.open("t.confirm.png")
        self.button_confirm = self.button_confirm.resize((115, 31), Image.LANCZOS)
        self.button_photoconfirm = ImageTk.PhotoImage(self.button_confirm)

        self.confirm_botton = tk.Label(self, image=self.button_photoconfirm, borderwidth=0)
        self.confirm_botton.place(x= 901, y=583)
        self.confirm_botton.bind("<Button-1>", self.confirm_booking)

        self.button_back = Image.open("tback.png")
        self.button_back = self.button_back.resize((70, 25), Image.LANCZOS)
        self.button_photoback = ImageTk.PhotoImage(self.button_back)

        self.back_button = tk.Label(self, image=self.button_photoback, borderwidth=0)
        self.back_button.place(x=145, y=90)
        self.back_button.bind("<Button-1>", self.go_back)

    def go_back(self, event):
        self.destroy()
        awalan_page = SearchForm()
        awalan_page.mainloop()
    
    def confirm_booking(self, event):
        # Get user input
        nama = self.nama_entry.get()
        phone = self.phone_entry.get()
        booking_date = self.date_entry.get()
        
        # Validasi input
        if not nama or not phone or not booking_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        # Menyimpan data booking dari user kedalam file csv
        with open("data_bookings.csv", "a") as file:
            file.write(f"{nama},{phone},{booking_date},{self.nama_kos}\n")
        
        # Konfirmasi jika booking sukses
        messagebox.showinfo("Sukses", "booking diterima!")
        
        # Halaman informasi pemilik kos
        confirmation_window = tk.Toplevel(self)
        confirmation_window.title("Booking Confirmation")
        confirmation_window.geometry("1278x700")

        confirmation_image = Image.open("kontak.png")
        confirmation_image = confirmation_image.resize((1278,700))
        confirmation_photo = ImageTk.PhotoImage(confirmation_image)

        label_confirmation_image = tk.Label(confirmation_window, image=confirmation_photo)
        label_confirmation_image.image = confirmation_photo  # Keep a reference to avoid garbage collection
        label_confirmation_image.place(x=0, y=0)
        
        # Add labels for displaying booking details
        tk.Label(confirmation_window, text=self.nama_kos, font=("Arial", 15, 'bold'), bg = "white").place(x=500, y=392)
        tk.Label(confirmation_window, text=self.no_hp, font=("Arial", 15, 'bold'), bg = "white").place(x=500, y=503)


if __name__ == '__main__':
    app = AwalanPage()
    app.mainloop()
  