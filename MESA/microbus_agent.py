from mesa import Agent
import networkx as nx
from semaforo_agent import SemaforoAgent

class MicrobusAgent(Agent):
    def __init__(self, unique_id, model, destination):
        super().__init__(unique_id, model)
        self.destination = destination
        self.estado = "normal"  # Estado inicial del microbús
        self.current_route = []  # Ruta actual que incluye semáforos y el destino final

    def a_star_route(self, start, end):
        graph = self.model.city_graph
        try:
            return nx.astar_path(graph, start, end, heuristic=self.heuristic)
        except nx.NetworkXNoPath:
            return []

    def heuristic(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1 - x2) + abs(y1 - y2)  # Distancia Manhattan

    def step(self):
        # Si no hay ruta calculada, incluir un semáforo en la ruta
        if not self.current_route:
            # Seleccionar un semáforo aleatorio del modelo
            semaforo = self.random.choice(self.model.semaforos)
            semaforo_pos = semaforo.pos

            # Calcular la ruta hacia el semáforo primero y luego al destino
            route_to_semaforo = self.a_star_route(self.pos, semaforo_pos)
            route_to_destination = self.a_star_route(semaforo_pos, self.destination)

            # Combinar las rutas para que pase por el semáforo
            self.current_route = route_to_semaforo[:-1] + route_to_destination

        # Verificar si el microbús está en la posición de un semáforo
        cell_contents = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cell_contents:
            if isinstance(obj, SemaforoAgent):
                if obj.state == "rojo":
                    self.estado = "detenido"
                    return  # No avanzar si el semáforo está en rojo

        # Si no hay semáforo en rojo, continuar movimiento
        self.estado = "en movimiento"

        # Moverse al siguiente paso en la ruta
        if len(self.current_route) > 1:
            next_step = self.current_route.pop(0)  # Tomar el siguiente paso en la ruta
            self.model.grid.move_agent(self, next_step)
