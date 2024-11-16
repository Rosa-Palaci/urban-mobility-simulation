from mesa import Agent

class SemaforoAgent(Agent):
    def __init__(self, unique_id, model, initial_state="rojo"):
        super().__init__(unique_id, model)
        self.state = initial_state  # Estado inicial del semáforo ("rojo", "amarillo" o "verde")
        self.timer = 0  # Temporizador para cambiar el estado

    def step(self):
        # Cambiar estado cada 5 pasos para verde y rojo, 2 pasos para amarillo
        self.timer += 1
        if self.state == "rojo" and self.timer % 5 == 0:
            self.state = "verde"
            self.timer = 0  # Reiniciar el temporizador al cambiar a verde
        elif self.state == "verde" and self.timer % 5 == 0:
            self.state = "amarillo"
            self.timer = 0  # Reiniciar el temporizador al cambiar a amarillo
        elif self.state == "amarillo" and self.timer % 2 == 0:
            self.state = "rojo"
            self.timer = 0  # Reiniciar el temporizador al cambiar a rojo
