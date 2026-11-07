import time
import multiprocessing
import numpy as np

# Configuración de la escena y resolución
WIDTH, HEIGHT = 1024, 1024
TILE_SIZE = 64

def render_tile(args):
    x_start, y_start, width, height = args
    # Búfer temporal exclusivo para este mosaico (evita condiciones de carrera)
    tile_buffer = np.zeros((height, width, 3), dtype=np.float32)
    
    # Simulación de cálculo de rayos (Ray Tracing / Monte Carlo simplificado y vectorizado con NumPy)
    for y in range(height):
        for x in range(width):
            px = x_start + x
            py = y_start + y
            # Operación matemática simulada del color del rayo
            r = (px / WIDTH) * 255
            g = (py / HEIGHT) * 255
            b = 128.0
            tile_buffer[y, x] = [r, g, b]
            
    return x_start, y_start, tile_buffer

def main():
    print("- Benchmarking HPC Raytracer en Python")
    print(f"Resolución: {WIDTH}x{HEIGHT} | Tamaño Mosaico: {TILE_SIZE}x{TILE_SIZE}")
    
    # Generar coordenadas de los mosaicos (Tiles)
    tiles = []
    for y in range(0, HEIGHT, TILE_SIZE):
        for x in range(0, WIDTH, TILE_SIZE):
            w = min(TILE_SIZE, WIDTH - x)
            h = min(TILE_SIZE, HEIGHT - y)
            tiles.append((x, y, w, h))
            
    num_cores = 12
    print(f"PCAM Mapeo: Asignando {len(tiles)} mosaicos a {num_cores} núcleos lógicos...")
    
    start_time = time.time()
    
    # Ejecución concurrente usando multiprocessing.Pool (Sin bloqueos / Lock-free)
    with multiprocessing.Pool(processes=num_cores) as pool:
        results = pool.map(render_tile, tiles)
        
    # Consolidación del Framebuffer final en el hilo principal
    framebuffer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    for x_start, y_start, tile_buffer in results:
        h, w, _ = tile_buffer.shape
        framebuffer[y_start:y_start+h, x_start:x_start+w] = tile_buffer
        
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Renderizado completado en: {elapsed_time:.4f} segundos")

if __name__ == '__main__':
    main()