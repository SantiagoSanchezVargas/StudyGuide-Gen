# StudyGuide-Gen: Asistente de Estructuración Académica

## Descripción

**StudyGuide-Gen** es una herramienta innovadora diseñada para estudiantes de ingeniería y desarrolladores que buscan optimizar su experiencia académica. Esta aplicación pone el "norte" en tus proyectos universitarios al automatizar la estructuración de laboratorios, marcos referenciales y guías de estudio, transformando documentos desorganizados en recursos claros y accionables. Con un enfoque en la eficiencia, StudyGuide-Gen elimina el tedio de la organización manual, permitiéndote enfocarte en el aprendizaje y la innovación.

En un mundo donde el tiempo es oro, StudyGuide-Gen actúa como tu compañero digital, extrayendo información clave de textos planos y generando outputs personalizados. Ya sea que estés preparando un laboratorio complejo, compilando referencias académicas o creando flashcards para repasar conceptos, esta app asegura que tus materiales estén siempre un paso adelante, facilitando un flujo de trabajo académico más productivo y menos estresante.

## Características Principales

- **Modo Laboratorio**: Extrae automáticamente materiales esenciales de documentos y genera roadmaps personalizados para guiar tus experimentos y proyectos prácticos.
- **Modo Referencial**: Utiliza procesamiento de texto avanzado con expresiones regulares (Regex) para extraer y formatear citas en estilos APA e IEEE, simplificando la creación de marcos referenciales.
- **Modo Estudio**: Genera flashcards interactivas y resalta conceptos clave para un estudio eficiente y memorable.
- **Interfaz Moderna**: Construida con CustomTkinter, ofrece una experiencia de usuario fluida con un elegante modo oscuro que reduce la fatiga visual durante sesiones largas.
- **Zero-Database**: Almacenamiento local ligero mediante archivos JSON, asegurando privacidad y portabilidad sin dependencias externas.

## Tecnologías Usadas

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.0-orange)
![JSON](https://img.shields.io/badge/JSON-Standard%20Library-green)
![Regex](https://img.shields.io/badge/Regex-re%20Module-red)

## Instalación

Sigue estos pasos para instalar y ejecutar StudyGuide-Gen en tu máquina local:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/StudyGuide-Gen.git
   cd StudyGuide-Gen
   ```

2. **Crea un entorno virtual** (recomendado para aislar dependencias):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install customtkinter
   ```

¡Listo! Ahora puedes ejecutar la aplicación.

## Uso

1. Abre la aplicación ejecutando `python generador_guias.py`.
2. Sube un archivo de texto (.txt) que contenga tu documento académico.
3. Selecciona el tipo de documento (Laboratorio, Referencial o Estudio) y deja que StudyGuide-Gen haga el resto.

La app procesará el texto y generará la salida correspondiente en segundos, lista para usar en tus proyectos.

## Roadmap del Proyecto

Estamos trabajando en futuras actualizaciones para hacer StudyGuide-Gen aún más poderosa:

- **Exportación a PDF/Markdown**: Permite guardar tus guías generadas en formatos ampliamente compatibles para compartir y archivar.
- **Integración con APIs de IA**: Incorpora inteligencia artificial para sugerencias personalizadas y análisis más profundos de texto.
- **Soporte Multiidioma**: Expande la funcionalidad a otros idiomas para una audiencia global.
- **Modo Colaborativo**: Habilita la edición compartida de guías en tiempo real.

¡Mantente al tanto de las actualizaciones siguiendo el repositorio!

---

*Desarrollado con pasión para la comunidad académica. Si encuentras útil StudyGuide-Gen, considera darle una estrella en GitHub.*