import requests
import os
import sys
import time

# --- Configuración: Reemplaza con tus URLs de descarga directa ---
# Las URLs deben apuntar a la descarga directa de los archivos alojados en Hugging Face.
PKL_FILES = {
    "final_dataset.pkl": "https://huggingface.co/datasets/Grizky/Recomendador/resolve/main/final_dataset.pkl",
    "optimized_data.pkl": "https://huggingface.co/datasets/Grizky/Recomendador/resolve/main/optimized_data.pkl"
}
OUTPUT_DIR = "data/processed"
# ----------------------------------------------------------------

def download_file(url, local_filename):
    """Descarga un archivo de una URL a la ruta local con manejo básico de progreso."""
    print(f"\nDescargando {local_filename}...")
    try:
        # Añadir un user-agent para evitar el rechazo por algunos servidores
        headers = {'User-Agent': 'Mozilla/5.0'}
        with requests.get(url, stream=True, headers=headers, timeout=300) as r:
            r.raise_for_status() # Lanza error si el código HTTP es 4xx/5xx
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0
            start_time = time.time()
            
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    
                    # Mostrar progreso (solo si el tamaño total es conocido)
                    if total_size > 0:
                        progress = downloaded_size / total_size
                        # Usamos \r para sobrescribir la línea
                        sys.stdout.write(f"\rProgreso: {progress:.2%} | {downloaded_size / (1024*1024):.2f} MB de {total_size / (1024*1024):.2f} MB")
                        sys.stdout.flush()
            
            end_time = time.time()
            print(f"\n✅ Descarga de {local_filename} completada en {end_time - start_time:.2f} segundos.")
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error al descargar {local_filename}: {e}")
        print("Asegúrate de que la URL sea un enlace de descarga DIRECTA y que 'requests' esté instalado.")

def main():
    # Asegurarse de que la carpeta de destino exista
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Iniciando descarga de archivos .pkl grandes desde Hugging Face Hub...")
        
    for filename, url in PKL_FILES.items():
        local_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(local_path):
            print(f"⏩ {filename} ya existe en {OUTPUT_DIR}. Saltando descarga.")
            continue
            
        download_file(url, local_path)
        
    print("\nProceso de descarga de datos completado.")
    print("El sistema está listo. Puedes ejecutar: python -m streamlit run app.py")

if __name__ == "__main__":
    try:
        import requests
        main()
    except ImportError:
        print("="*60)
        print("❌ ERROR: La librería 'requests' no está instalada.")
        print("Por favor, ejecuta: pip install requests")
        print("="*60)