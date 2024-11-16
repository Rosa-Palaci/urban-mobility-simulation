import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from microbus_model import MicrobusModel
import time
from microbus_agent import MicrobusAgent


# Parámetros de la simulación
width, height = 10, 10
num_agents = 5

# Cargar las imágenes del microbús y el destino (parada de tacos)
micro_image = mpimg.imread("images/micro.png")
destination_image = mpimg.imread("images/parada.png")

# Crear el modelo
model = MicrobusModel(width, height, num_agents)

# Configuración de la visualización
fig, ax = plt.subplots()
plt.ion()  # Modo interactivo para actualizar la visualización en cada paso

# Configurar título y descripción
plt.suptitle("Simulación de Microbuses hacia Paradas Aleatorias en CDMX", fontsize=16)
description_text = "Cada microbús se dirige a una parada de tacos aleatoria en la cuadrícula."

# Función para dibujar la cuadrícula y los agentes
def draw_grid(model, step, start_time):
    ax.clear()
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks(range(width + 1))
    ax.set_yticks(range(height + 1))
    ax.grid(True)

    # Dibujar microbuses y destinos
    for agent in model.schedule.agents:
        if isinstance(agent, MicrobusAgent):
            x, y = agent.pos
            ax.imshow(micro_image, extent=(x, x+1, y, y+1), aspect='auto')
            dest_x, dest_y = agent.destination
            ax.imshow(destination_image, extent=(dest_x, dest_x+1, dest_y, dest_y+1), aspect='auto')

    # Dibujar semáforos
    for semaforo in model.semaforos:
        x, y = semaforo.pos
        color = "green" if semaforo.state == "verde" else ("yellow" if semaforo.state == "amarillo" else "red")
        ax.add_patch(plt.Circle((x + 0.5, y + 0.5), 0.3, color=color))

    # Calcular tiempo de ejecución
    elapsed_time = time.time() - start_time
    ax.set_title(f"{description_text}\nPaso actual: {step}, Tiempo de ejecución: {elapsed_time:.2f} segundos")

    plt.draw()
    plt.pause(0.5)

# Iniciar temporizador de la simulación
start_time = time.time()

# Ejecutar la simulación y actualizar la visualización
for i in range(10):  # Ejecuta 10 pasos de la simulación
    print(f"Step {i + 1}")
    model.step()
    draw_grid(model, i + 1, start_time)

    # Imprimir la posición de cada agente después de cada paso
    for agent in model.schedule.agents:
        print(f"Micro {agent.unique_id} Posicion: {agent.pos}")

# Finalizar la visualización interactiva
plt.ioff()
plt.show()
