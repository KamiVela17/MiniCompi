# -*- coding: utf-8 -*-
import Tkinter as tk
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk
import subprocess
import os
from sintactico import analizar_y_traducir

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Mini Compilador de Valorant")
        self.configure(bg='#333')

        self.title_label = tk.Label(self, text="Compilador Valorant", font=("Helvetica", 16, "bold"), bg='#333', fg='white')
        self.title_label.pack(pady=(20, 10))

        self.instructions_label = tk.Label(self, text="Seleccione un archivo TXT para analizar:", font=("Helvetica", 10), bg='#333', fg='white')
        self.instructions_label.pack(pady=(0, 20))

        self.boton_analizar = tk.Button(self, text="Seleccionar Archivo", command=self.seleccionar_archivo_y_analizar, bg='#5C85FB', fg='white', font=("Helvetica", 12), bd=0)
        self.boton_analizar.pack(pady=(0, 20), ipadx=10, ipady=5)

        self.minsize(400, 200)
        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

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
