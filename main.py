# -*- coding: utf-8 -*-
import Tkinter as tk
import ttk
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk
import os
from sintactico import analizar_y_traducir

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Mini Compilador de Valorant")
        self.configure(bg='#202020')  # Un fondo oscuro que combina con el tema de Valorant

        # Carga y muestra el logo de Valorant
        self.load_logo()

        self.title_label = tk.Label(self, text="Compilador Valorant", font=("Helvetica", 16, "bold"), bg='#202020', fg='white')
        self.title_label.pack(pady=(10, 10))

        self.instructions_label = tk.Label(self, text="Seleccione un archivo TXT para analizar:", font=("Helvetica", 10), bg='#202020', fg='white')
        self.instructions_label.pack(pady=(0, 20))

        self.boton_analizar = ttk.Button(self, text="Seleccionar Archivo", command=self.seleccionar_archivo_y_analizar, style='TButton')
        self.boton_analizar.pack(pady=(0, 20), ipadx=10, ipady=5)

        self.minsize(500, 300)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

    def load_logo(self):
        # Ajusta la ruta según la ubicación de tu archivo
        logo_path = os.path.join(os.path.dirname(__file__), 'icono.png')
        img = Image.open(logo_path)
        img = img.resize((175, 125), Image.ANTIALIAS)  # Redimensionar la imagen para ajustarla
        photo = ImageTk.PhotoImage(img)
        self.logo_label = tk.Label(self, image=photo, bg='#202020')
        self.logo_label.image = photo  # Mantener una referencia
        self.logo_label.pack(pady=(20, 10))

    def seleccionar_archivo_y_analizar(self):
        filepath = tkFileDialog.askopenfilename(
            title="Seleccionar archivo TXT",
            filetypes=(("Archivos TXT", "*.txt"), ("Todos los archivos", "*.*")),
            parent=self
        )
        if filepath:
            try:
                with open(filepath, 'r') as file:
                    source_code = file.read()
                analizar_y_traducir(source_code)
            except Exception as e:
                print("Ocurrió un error:", e)
                tkMessageBox.showerror("Error", str(e), parent=self)

if __name__ == '__main__':
    app = Application()
    app.mainloop()
