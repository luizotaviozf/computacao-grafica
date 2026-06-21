from tkinter import filedialog
from EntradaSaida.descritor_obj import DescritorOBJ

def salvar_obj(self):
        from tkinter import filedialog
        caminho = filedialog.asksaveasfilename(defaultextension=".obj")

        if not caminho:
            return

        with open(caminho, "w") as f:
            descritor = DescritorOBJ()

            for obj in self.display_file:
                f.write(descritor.descrever_objeto(obj) + "\n")