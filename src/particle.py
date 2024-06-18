"""Define a classe Particula."""

from math import sqrt
from config import Config


(
    N,
    SIM_W,
    BOTTOM,
    DAM,
    DAM_BREAK,
    G,
    SPACING,
    K,
    K_NEAR,
    REST_DENSITY,
    R,
    SIGMA,
    MAX_VEL,
    WALL_DAMP,
    VEL_DAMP,
) = Config().return_config()


class Particle:
    """
    Uma única partícula do fluido simulado

    Atributos:
        x_pos: posição x da partícula
        y_pos: posição y da partícula
        previous_x_pos: posição x da partícula no quadro anterior
        previous_y_pos: posição y da partícula no quadro anterior
        visual_x_pos: posição x da partícula que é exibida na tela
        visual_y_pos: posição y da partícula que é exibida na tela
        rho: densidade da partícula
        rho_near: densidade próxima da partícula, usada para evitar colisões entre partículas
        press: pressão da partícula
        press_near: pressão próxima da partícula, usada para evitar colisões entre partículas
        neighbors: lista dos vizinhos da partícula
        x_vel: velocidade x da partícula
        y_vel: velocidade y da partícula
        x_force: força x aplicada à partícula
        y_force: força y aplicada à partícula
    """

    def __init__(self, x_pos: float, y_pos: float):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.previous_x_pos = x_pos
        self.previous_y_pos = y_pos
        self.visual_x_pos = x_pos
        self.visual_y_pos = y_pos
        self.rho = 0.0
        self.rho_near = 0.0
        self.press = 0.0
        self.press_near = 0.0
        self.neighbors = []
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.x_force = 0.0
        self.y_force = -G

    def update_state(self, dam: bool):
        """
        Atualiza o estado da partícula
        """
        # Redefine a posição anterior
        (self.previous_x_pos, self.previous_y_pos) = (self.x_pos, self.y_pos)

        # Aplica a força usando a segunda lei de Newton e integração de Euler com massa = 1 e dt = 1
        (self.x_vel, self.y_vel) = (
            self.x_vel + self.x_force,
            self.y_vel + self.y_force,
        )

        # Move a partícula de acordo com sua velocidade usando integração de Euler com dt = 1
        (self.x_pos, self.y_pos) = (self.x_pos + self.x_vel, self.y_pos + self.y_vel)

        # Define a posição visual. A posição visual é a que é exibida na tela
        # É usado para evitar que partículas instáveis sejam exibidas
        (self.visual_x_pos, self.visual_y_pos) = (self.x_pos, self.y_pos)

        # Redefine a força
        (self.x_force, self.y_force) = (0.0, -G)

        # Define a velocidade usando integração de Euler com dt = 1
        (self.x_vel, self.y_vel) = (
            self.x_pos - self.previous_x_pos,
            self.y_pos - self.previous_y_pos,
        )

        # Calcula a velocidade
        velocity = sqrt(self.x_vel**2 + self.y_vel**2)

        # Reduz a velocidade se ela for muito alta
        if velocity > MAX_VEL:
            self.x_vel *= VEL_DAMP
            self.y_vel *= VEL_DAMP

        # Restrições de parede, se uma partícula estiver fora dos limites, crie uma força de mola para trazê-la de volta
        if self.x_pos < -SIM_W:
            self.x_force -= (self.x_pos - -SIM_W) * WALL_DAMP
            self.visual_x_pos = -SIM_W

        # O mesmo que uma restrição de parede, mas para a barragem que se moverá de dam para SIM_W
        if dam is True and self.x_pos > DAM:
            self.x_force -= (self.x_pos - DAM) * WALL_DAMP

        # O mesmo para a parede direita
        if self.x_pos > SIM_W:
            self.x_force -= (self.x_pos - SIM_W) * WALL_DAMP
            self.visual_x_pos = SIM_W

        # O mesmo, mas para o chão
        if self.y_pos < BOTTOM:
            # Usamos SIM_W em vez de BOTTOM aqui porque, caso contrário, as partículas ficam muito baixas
            self.y_force -= (self.y_pos - SIM_W) * WALL_DAMP
            self.visual_y_pos = BOTTOM

        # Redefine a densidade
        self.rho = 0.0
        self.rho_near = 0.0

        # Redefine os vizinhos
        self.neighbors = []

    def calculate_pressure(self):
        """
        Calcula a pressão da partícula
        """
        self.press = K * (self.rho - REST_DENSITY)
        self.press_near = K_NEAR * self.rho_near
