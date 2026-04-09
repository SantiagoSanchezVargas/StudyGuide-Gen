import json
import os
import uuid
import re
import threading
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pyperclip


def leer_archivo_local(ruta):
    """
    Lee el contenido de un archivo .txt local.

    Args:
        ruta (str): La ruta absoluta al archivo .txt.

    Returns:
        str: El contenido del archivo.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si no es un archivo .txt.
    """
    if not ruta.endswith('.txt'):
        raise ValueError("El archivo debe ser un .txt")
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"El archivo {ruta} no existe")
    with open(ruta, 'r', encoding='utf-8') as f:
        return f.read()


def crear_guia(titulo, materia, tipo_documento, puntos_clave, roadmap):
    """
    Crea un diccionario que representa una guía de estudio con la estructura requerida.

    Args:
        titulo (str): El título de la guía.
        materia (str): La materia de la guía.
        tipo_documento (str): El tipo de documento ("ESTUDIO", "LABORATORIO", "MARCO_REFERENCIAL").
        puntos_clave (list): Lista de diccionarios, cada uno con 'pregunta', 'respuesta', y 'verificado'.
        roadmap (list): Lista de tareas sugeridas.

    Returns:
        dict: Diccionario con id, titulo, materia, fecha, tipo_documento, puntos_clave, y roadmap.
    """
    guia = {
        "id": str(uuid.uuid4()),
        "titulo": titulo,
        "materia": materia,
        "tipo_documento": tipo_documento,
        "fecha": datetime.now().isoformat(),
        "puntos_clave": puntos_clave,
        "roadmap": roadmap
    }
    return guia


def guardar_guia(nueva_guia):
    """
    Guarda una nueva guía en el archivo guias.json de manera segura.

    Verifica si el archivo existe; si no, lo crea como una lista vacía.
    Lee el contenido actual, añade la nueva guía y guarda los cambios.
    Usa try-except para capturar errores de escritura y evitar corrupción del archivo.

    Args:
        nueva_guia (dict): El diccionario de la guía a guardar.

    Raises:
        Exception: Si ocurre un error durante la escritura.
    """
    archivo = "guias.json"
    guias = []
    
    # Verificar si el archivo existe y leer contenido
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                guias = json.load(f)
        except json.JSONDecodeError:
            # Si el archivo está corrupto, inicializar como lista vacía
            guias = []
    
    # Añadir la nueva guía
    guias.append(nueva_guia)
    
    # Guardar los cambios con manejo de errores
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(guias, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception(f"Error al guardar la guía: {str(e)}")


def extraer_estudio(texto):
    """
    Extrae puntos clave para tipo ESTUDIO: genera preguntas y respuestas de conceptos.

    Args:
        texto (str): El texto a procesar.

    Returns:
        dict: {'puntos_clave': list, 'roadmap': list}
    """
    oraciones = [oracion.strip() for oracion in texto.split('.') if oracion.strip()]
    puntos_clave = []
    palabras_clave = ["es", "son", "consiste en"]
    
    for oracion in oraciones:
        if any(palabra in oracion.lower() for palabra in palabras_clave):
            pregunta = f"¿Qué es {oracion.split()[0]}?"
            respuesta = oracion
            if len(respuesta) < 10:
                respuesta = f"REVISIÓN NECESARIA: {respuesta}"
            puntos_clave.append({
                "pregunta": pregunta,
                "respuesta": respuesta,
                "verificado": False
            })
    
    roadmap = ["Revisar conceptos clave", "Practicar preguntas", "Verificar respuestas"]
    return {'puntos_clave': puntos_clave, 'roadmap': roadmap}


def extraer_laboratorio(texto):
    """
    Extrae para tipo LABORATORIO: genera roadmap de tareas basadas en palabras clave.

    Args:
        texto (str): El texto a procesar.

    Returns:
        dict: {'roadmap': list}
    """
    roadmap = []
    if "materiales" in texto.lower():
        roadmap.append("Organizar tabla de materiales")
    if "procedimiento" in texto.lower():
        roadmap.append("Redactar procedimiento detallado")
    if "resultados" in texto.lower():
        roadmap.append("Analizar y tabular resultados")
    if "conclusión" in texto.lower():
        roadmap.append("Escribir conclusiones")
    if not roadmap:
        roadmap = ["Revisar secciones del laboratorio"]
    return {'roadmap': roadmap}


def extraer_marco_referencial(texto):
    """
    Extrae citas para tipo MARCO_REFERENCIAL usando regex.

    Args:
        texto (str): El texto a procesar.

    Returns:
        dict: {'citas': list}
    """
    # Regex para citas: Apellido (Año) o (Apellido, Año)
    pattern = r'\b[A-Z][a-z]+\s*\(\d{4}\)|et al\.|\(et al\., \d{4}\)'
    citas = re.findall(pattern, texto)
    citas = list(set(citas))  # Eliminar duplicados
    return {'citas': citas}


def procesar_documento(tipo_documento, texto_crudo):
    """
    Procesa un texto crudo para generar resultados según el tipo de documento.

    Args:
        tipo_documento (str): "ESTUDIO", "LABORATORIO" o "MARCO_REFERENCIAL".
        texto_crudo (str): El texto crudo a procesar.

    Returns:
        dict: Resultados según el tipo.

    Raises:
        ValueError: Si el tipo_documento no es válido o el texto es muy corto.
    """
    if tipo_documento not in ["ESTUDIO", "LABORATORIO", "MARCO_REFERENCIAL"]:
        raise ValueError("Tipo de documento no válido")
    
    if len(texto_crudo) < 50:
        raise ValueError("El texto es muy corto para generar una guía útil. Proporciona más contenido.")
    
    if tipo_documento == "ESTUDIO":
        return extraer_estudio(texto_crudo)
    elif tipo_documento == "LABORATORIO":
        return extraer_laboratorio(texto_crudo)
    elif tipo_documento == "MARCO_REFERENCIAL":
        return extraer_marco_referencial(texto_crudo)


def guardar_entrada(tipo_documento, roadmap):
    """
    Guarda una entrada en guias.json con id, timestamp, tipo_documento y roadmap.

    Args:
        tipo_documento (str): El tipo de documento.
        roadmap (list): La lista de roadmap.
    """
    entrada = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "tipo_documento": tipo_documento,
        "roadmap": roadmap
    }
    
    archivo = "guias.json"
    entradas = []
    
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                entradas = json.load(f)
        except json.JSONDecodeError:
            entradas = []
    
    entradas.append(entrada)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(entradas, f, ensure_ascii=False, indent=4)


# Ejemplo de uso (puedes descomentarlo para probar)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("Academic Architect Pro")
        self.geometry("1200x700")
        
        # Layout de dos columnas
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panel Izquierdo (Entrada)
        self.frame_entrada = ctk.CTkFrame(self)
        self.frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_entrada, text="Academic Architect Pro", font=("Arial", 20, "bold")).pack(pady=10)
        
        ctk.CTkLabel(self.frame_entrada, text="Tipo de Documento:").pack(pady=5)
        self.combo_tipo = ctk.CTkComboBox(self.frame_entrada, values=["ESTUDIO", "LABORATORIO", "MARCO_REFERENCIAL"])
        self.combo_tipo.pack(pady=5)
        
        self.btn_cargar = ctk.CTkButton(self.frame_entrada, text="Cargar Archivo .txt", command=self.cargar_archivo, fg_color="#007BFF")
        self.btn_cargar.pack(pady=5)
        
        ctk.CTkLabel(self.frame_entrada, text="O pega el texto aquí:").pack(pady=5)
        self.textbox_entrada = ctk.CTkTextbox(self.frame_entrada, height=300)
        self.textbox_entrada.pack(pady=5, fill="both", expand=True)
        
        self.btn_generar = ctk.CTkButton(self.frame_entrada, text="Generar Norte / Procesar", command=self.generar, fg_color="#28A745", height=40)
        self.btn_generar.pack(pady=10)
        
        # Panel Derecho (Resultados)
        self.frame_resultados = ctk.CTkScrollableFrame(self, fg_color="#2B2B2B")
        self.frame_resultados.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(self.frame_resultados, text="Resultados", font=("Arial", 16)).pack(pady=10)
        
        # Variables
        self.texto_crudo = ""
        self.resultados = None
    
    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            try:
                self.texto_crudo = leer_archivo_local(ruta)
                self.textbox_entrada.delete("1.0", "end")
                self.textbox_entrada.insert("1.0", self.texto_crudo)
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {str(e)}")
    
    def generar(self):
        tipo = self.combo_tipo.get()
        if not tipo:
            messagebox.showerror("Error", "Selecciona un tipo de documento.")
            return
        
        texto = self.textbox_entrada.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Advertencia", "Ingresa o carga un texto.")
            return
        
        # Deshabilitar botón
        self.btn_generar.configure(state="disabled", text="Procesando...")
        
        # Procesar en thread
        threading.Thread(target=self._procesar, args=(tipo, texto)).start()
    
    def _procesar(self, tipo, texto):
        try:
            self.resultados = procesar_documento(tipo, texto)
            
            # Limpiar resultados anteriores
            for widget in self.frame_resultados.winfo_children():
                if widget != self.frame_resultados.winfo_children()[0]:  # Mantener el label
                    widget.destroy()
            
            # Mostrar resultados
            if tipo == "ESTUDIO":
                for punto in self.resultados['puntos_clave']:
                    self._crear_tarjeta(f"Pregunta: {punto['pregunta']}\nRespuesta: {punto['respuesta']}")
                for tarea in self.resultados['roadmap']:
                    self._crear_tarjeta(f"Roadmap: {tarea}")
            elif tipo == "LABORATORIO":
                for tarea in self.resultados['roadmap']:
                    self._crear_tarjeta(f"Tarea: {tarea}")
            elif tipo == "MARCO_REFERENCIAL":
                for cita in self.resultados['citas']:
                    self._crear_tarjeta_cita(cita)
            
            # Guardar entrada
            guardar_entrada(tipo, self.resultados.get('roadmap', []))
            
            messagebox.showinfo("Éxito", "Procesamiento completado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar: {str(e)}")
        finally:
            self.btn_generar.configure(state="normal", text="Generar Norte / Procesar")
    
    def _crear_tarjeta(self, texto):
        tarjeta = ctk.CTkFrame(self.frame_resultados, corner_radius=10)
        tarjeta.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(tarjeta, text=texto, wraplength=400).pack(pady=10, padx=10)
    
    def _crear_tarjeta_cita(self, cita):
        tarjeta = ctk.CTkFrame(self.frame_resultados, corner_radius=10)
        tarjeta.pack(pady=5, fill="x", padx=10)
        ctk.CTkLabel(tarjeta, text=f"Cita: {cita}").pack(pady=5, padx=10)
        btn_copiar = ctk.CTkButton(tarjeta, text="Copiar Cita", command=lambda: self._copiar_cita(cita), fg_color="#007BFF")
        btn_copiar.pack(pady=5)
    
    def _copiar_cita(self, cita):
        pyperclip.copy(cita)
        messagebox.showinfo("Copiado", "Cita copiada al portapapeles.")


if __name__ == "__main__":
    app = App()
    app.mainloop()