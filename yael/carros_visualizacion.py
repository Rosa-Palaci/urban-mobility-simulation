import mesa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from carros import CocheAgente, SemaforoAgente, InterseccionModelo

# -------------------- Función de Visualización --------------------
def visualizar(modelo):
    plt.clf()
    ax = plt.gca()
    
    # Graficar coches
    for agente in modelo.schedule.agents:
        if agente.tipo == "coche":
            ax.scatter(agente.pos[0], agente.pos[1], color='blue', label='Coche' if 'Coche' not in ax.get_legend_handles_labels()[1] else "")
    
    # Graficar semáforo
    semaforo = next((agente for agente in modelo.schedule.agents if agente.tipo == "semaforo"), None)
    if semaforo:
        color_semaforo = 'green' if semaforo.estado == 'Verde' else ('red' if semaforo.estado == 'Rojo' else 'yellow')
        ax.scatter(semaforo.pos[0], semaforo.pos[1], color=color_semaforo, label='Semáforo')

    ax.set_xlim(-1, modelo.ancho)
    ax.set_ylim(-1, modelo.alto)
    ax.set_title("Simulación de Intersección")
    ax.set_xlabel("Eje X")
    ax.set_ylabel("Eje Y")
    ax.legend()
    
    plt.pause(0.5)  # Pausa para la visualización

# -------------------- Ejecución de la Simulación --------------------
num_semaforos = 1
num_coches = 10
ancho_mapa = 10
alto_mapa = 10

modelo_interseccion = InterseccionModelo(num_semaforos, num_coches, ancho_mapa, alto_mapa)

plt.ion()  # Activar modo interactivo para matplotlib
for _ in range(50):  # Número de pasos de simulación
    modelo_interseccion.step()
    visualizar(modelo_interseccion)

plt.ioff()  # Desactivar modo interactivo al final
plt.show()