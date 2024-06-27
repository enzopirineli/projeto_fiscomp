"""Utilitários e cálculos físicos."""

from math import sqrt

from config import Config
from particle import Particle


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


def start(
    xmin: float, xmax: float, ymin: float, space: float, count: int
) -> list[Particle]:
    """
    Cria um retângulo de partículas dentro de xmin, xmax e ymin
    Começamos criando uma partícula em (xmin, ymin)
    e então adicionamos partículas até alcançar o número de partículas
    Partículas são representadas por suas posições [x, y]

    Args:
        xmin (float): x min bound do retângulo
        xmax (float): x max bound do retângulo
        ymin (float): y min bound do retângulo
        space (float): espaço entre partículas
        count (int): número de partículas

    Returns:
        list: lista de objetos Particle
    """
    result = []
    x_pos, y_pos = xmin, ymin
    for _ in range(count):
        result.append(Particle(x_pos, y_pos))
        x_pos += space
        if x_pos > xmax:
            x_pos = xmin
            y_pos += space
    return result


def calculate_density(particles: list[Particle]) -> None:
    """
    Calcula a densidade de partículas
        A densidade é calculada somando a distância relativa de partículas vizinhas
        Distinguimos densidade e densidade próxima para evitar que partículas colidam entre si,
        o que cria instabilidade

    Args:
        particles (list[Particle]): lista de partículas
    """
    for i, particle_1 in enumerate(particles):
        density = 0.0
        density_near = 0.0
        # A densidade é calculada somando a distância relativa de partículas vizinhas
        for particle_2 in particles[i + 1:]:
            distance = sqrt(
                (particle_1.x_pos - particle_2.x_pos) ** 2
                + (particle_1.y_pos - particle_2.y_pos) ** 2
            )
            if distance < R:
                # distância normal é entre 0 e 1
                normal_distance = 1 - distance / R
                density += normal_distance**2
                density_near += normal_distance**3
                particle_2.rho += normal_distance**2
                particle_2.rho_near += normal_distance**3
                particle_1.neighbors.append(particle_2)
        particle_1.rho += density
        particle_1.rho_near += density_near


def create_pressure(particles: list[Particle]) -> None:
    """
    Calcula a força de pressão de partículas
        A lista de vizinhos e a pressão já foram calculadas por calculate_density
        Calculamos a força de pressão somando a força de pressão de cada vizinho
        e aplicamos em direção ao vizinho

    Args:
        particles (list[Particle]): lista de partículas
    """
    for particle in particles:
        press_x = 0.0
        press_y = 0.0
        for neighbor in particle.neighbors:
            particle_to_neighbor = [
                neighbor.x_pos - particle.x_pos,
                neighbor.y_pos - particle.y_pos,
            ]
            distance = sqrt(particle_to_neighbor[0] ** 2 + particle_to_neighbor[1] ** 2)
            normal_distance = 1 - distance / R
            total_pressure = (
                particle.press + neighbor.press
            ) * normal_distance**2 + (
                particle.press_near + neighbor.press_near
            ) * normal_distance**3
            pressure_vector = [
                particle_to_neighbor[0] * total_pressure / distance,
                particle_to_neighbor[1] * total_pressure / distance,
            ]
            neighbor.x_force += pressure_vector[0]
            neighbor.y_force += pressure_vector[1]
            press_x += pressure_vector[0]
            press_y += pressure_vector[1]
        particle.x_force -= press_x
        particle.y_force -= press_y


def calculate_viscosity(particles: list[Particle]) -> None:
    """
    Calcula a força de viscosidade de partículas
    Força = (distância relativa de partículas)*(peso de viscosidade)*(diferença de velocidade de partículas)
    Diferença de velocidade é calculada no vetor entre as partículas

    Args:
        particles (list[Particle]): lista de partículas
    """

    for particle in particles:
        for neighbor in particle.neighbors:
            particle_to_neighbor = [
                neighbor.x_pos - particle.x_pos,
                neighbor.y_pos - particle.y_pos,
            ]
            distance = sqrt(particle_to_neighbor[0] ** 2 + particle_to_neighbor[1] ** 2)
            normal_p_to_n = [
                particle_to_neighbor[0] / distance,
                particle_to_neighbor[1] / distance,
            ]
            relative_distance = distance / R
            velocity_difference = (particle.x_vel - neighbor.x_vel) * normal_p_to_n[0] + (
                particle.y_vel - neighbor.y_vel
            ) * normal_p_to_n[1]
            if velocity_difference > 0:
                viscosity_force = [
                    (1 - relative_distance) * SIGMA * velocity_difference * normal_p_to_n[0],
                    (1 - relative_distance) * SIGMA * velocity_difference * normal_p_to_n[1],
                ]
                particle.x_vel -= viscosity_force[0] * 0.5
                particle.y_vel -= viscosity_force[1] * 0.5
                neighbor.x_vel += viscosity_force[0] * 0.5
                neighbor.y_vel += viscosity_force[1] * 0.5
