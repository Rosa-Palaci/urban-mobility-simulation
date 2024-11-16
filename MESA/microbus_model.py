from mesa import Model
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation
import networkx as nx
import random
from semaforo_agent import SemaforoAgent
from microbus_agent import MicrobusAgent

class MicrobusModel(Model):
    def __init__(self, width, height, num_agents):
        super().__init__()
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.city_graph = nx.grid_2d_graph(width, height)

        # Crear y posicionar semáforos
        self.semaforos = []
        for i in range(3):  # Agregar 3 semáforos
            x, y = self.random.randint(0, width-1), self.random.randint(0, height-1)
            semaforo = SemaforoAgent(f"Semaforo-{i}", self)
            self.grid.place_agent(semaforo, (x, y))
            self.schedule.add(semaforo)
            self.semaforos.append(semaforo)
        
        for i in range(self.num_agents):
            # Generar una posición aleatoria para el destino
            destination_x = random.randint(0, width - 1)
            destination_y = random.randint(0, height - 1)
            destination = (destination_x, destination_y)
            
            # Crear el agente microbús con el destino aleatorio
            agent = MicrobusAgent(i, self, destination=destination)
            self.schedule.add(agent)
            
            # Colocar al agente en una posición aleatoria inicial
            x, y = self.random.randint(0, width-1), self.random.randint(0, height-1)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        self.schedule.step()
