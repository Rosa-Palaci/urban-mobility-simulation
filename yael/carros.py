import mesa
import random

# -------------------- Agente Semáforo --------------------
class SemaforoAgente(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "semaforo"
        self.estado = "Amarillo"  # Estado inicial
        self.programa_luces = {}  # Diccionario para el programa de luces
        self.pos = (model.ancho // 2, model.alto // 2)  # Posición inicial en el centro de la intersección

    def planear_luces(self):
        vehiculos = [agente for agente in self.model.schedule.agents if agente.tipo == "coche"]
        if vehiculos:
            tiempos = [(coche, coche.tiempo_espera) for coche in vehiculos if self.es_cercano(coche)]
            if tiempos:
                coche_prioritario = min(tiempos, key=lambda x: x[1])[0]
                self.programa_luces[coche_prioritario.carril] = "Verde"
                self.estado = "Verde"  # Cambiar el estado del semáforo basado en el coche prioritario
            else:
                self.estado = "Amarillo"
        else:
            self.estado = "Rojo"

def es_cercano(self, coche):
    """Determina si un coche está lo suficientemente cerca para influir en el semáforo."""
    return abs(coche.pos[0] - self.pos[0]) <= 1 and abs(coche.pos[1] - self.pos[1]) <= 1



    def cambiar_estado(self):
        if self.programa_luces:
            for carril, estado in self.programa_luces.items():
                if estado == "Verde":
                    self.estado = "Verde"
                    return
        self.estado = "Rojo"  # Cambiar a rojo si no hay luces verdes programadas

    def step(self):
        self.planear_luces()
        self.cambiar_estado()

# -------------------- Agente Coche --------------------
class CocheAgente(mesa.Agent):
    def __init__(self, unique_id, model, carril, destino):
        super().__init__(unique_id, model)
        self.tipo = "coche"
        self.carril = carril
        self.destino = destino
        self.estado = "Normal"
        self.tiempo_espera = 0
        self.felicidad = 100
        self.pos = (random.randint(0, model.ancho - 1), random.randint(0, model.alto - 1))

    def enviar_informacion(self, semaforo):
        tiempo_llegada = random.randint(1, 10)  # Simulación de tiempo estimado de llegada
        self.tiempo_espera = tiempo_llegada
        semaforo.programa_luces[self.carril] = tiempo_llegada

    def actualizar_felicidad(self):
        # Disminuye la felicidad si el coche está esperando mucho
        if self.estado == "Ansioso/Enojado":
            self.felicidad -= 5
        else:
            self.felicidad += 1
        self.felicidad = max(0, min(100, self.felicidad))  # Limitar la felicidad entre 0 y 100

    def mover(self):
     if self.estado != "En Espera":
         if self.carril == "recto":
             if self.pos[0] < self.model.ancho - 1:  
                 self.pos = (self.pos[0] + 1, self.pos[1])  # Movimiento en el eje X
         elif self.carril == "izquierda":
             if self.pos[0] > 0:  
                 self.pos = (self.pos[0] - 1, self.pos[1])  # Movimiento en el eje X
         elif self.carril == "derecha":
             if self.pos[0] < self.model.ancho - 1:  
                 self.pos = (self.pos[0] + 1, self.pos[1])  # Movimiento en el eje X
         elif self.carril == "norte":
             if self.pos[1] < self.model.alto - 1:  # Movimiento en el eje Y
                 self.pos = (self.pos[0], self.pos[1] + 1)
         elif self.carril == "sur":
             if self.pos[1] > 0:  # Movimiento en el eje Y
                 self.pos = (self.pos[0], self.pos[1] - 1)
     else:
         pass  # No mueve si está en espera


    def negociar(self, otro_coche):
        """ Negociación entre coches para ceder el paso """
        if self.tiempo_espera < otro_coche.tiempo_espera:
            self.felicidad += 2
            otro_coche.felicidad -= 2
            return "cedo el paso"
        elif self.tiempo_espera > otro_coche.tiempo_espera:
            self.felicidad -= 2
            otro_coche.felicidad += 2
            return "cedo el paso"
        return "espero"

    def step(self):
        print(f"{self.unique_id} | Pos: {self.pos} | Estado: {self.estado} | Semáforo: {self.model.semaforo.estado}")
        self.tiempo_espera += 1
        self.actualizar_felicidad()

        semaforo = next((agente for agente in self.model.schedule.agents if agente.tipo == "semaforo"), None)
        if semaforo:
            self.enviar_informacion(semaforo)
    
        if semaforo.estado == "Rojo":
            self.estado = "En Espera"  # Los coches esperan si el semáforo está rojo
        else:
            self.estado = "Normal"  # Los coches pueden moverse si el semáforo está verde o amarillo

        self.mover()

        coches = [agente for agente in self.model.schedule.agents if agente.tipo == "coche" and agente != self]
        for coche in coches:
            if self.pos == coche.pos:  # Si los coches están cerca, negocian
                self.negociar(coche)

# -------------------- Modelo de Simulación --------------------
class InterseccionModelo(mesa.Model):
    def __init__(self, num_semaforos, num_coches, ancho, alto):
        super().__init__()
        self.schedule = mesa.time.RandomActivation(self)
        self.ancho = ancho
        self.alto = alto

        # Crear semáforos
        self.semaforo = None
        for i in range(num_semaforos):
            semaforo = SemaforoAgente(i, self)
            self.schedule.add(semaforo)
            if self.semaforo is None:  # Asignar un semáforo principal
                self.semaforo = semaforo

        # Crear coches
        for i in range(num_coches):
            carril = random.choice(["principal", "izquierda", "derecha"])
            destino = random.choice(["norte", "sur", "este", "oeste"])
            coche = CocheAgente(i + num_semaforos, self, carril, destino)
            self.schedule.add(coche)

    def step(self):
        self.schedule.step()
