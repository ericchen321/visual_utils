# Author: Guanxiong


import numpy as np
from typing import Tuple


def define_rectangular_sheet(
    num_springs_y: int,
    num_springs_x: int,
    spring_l0_row: float,
    spring_l0_col: float,
    diagonal: bool) -> Tuple[np.ndarray, np.ndarray]:
    r"""
    Define a 2D, rectangular-shaped sheet of masses connected by
    springs. We define that the sheet rests on x-y plane with particle
    0 being at pos (0, 0). The sheet extends horizontally along +x
    direction and vertically along -y direction:
    0  -  1  -  2  -  3
    |  \  |  \  |  \  |
    4  -  5  -  6  -  7
    |  \  |  \  |  \  |
    8  -  9  -  10 - 11

    Parameters:
        num_springs_y: Number of springs along a column/y-axis
        num_springs_x: Number of springs along a row/x-axis
        spring_l0_row: Rest length of springs in a row
        spring_l0_col: Rest length of springs in a column
        diagonal: Whether to include diagonal springs or not

    Return:
        A tuple of
        - edge list, i.e. spring definitions in terms of particle
            indices. Ordered by horizontal springs -> vertical
            springs -> diagonal springs if diagonal=True
            (num_springs, 2)
        - Rest configuration of particles in object's local frame
            (num_particles, 3)
        - Rest length of each spring
            (num_springs, 1)
    """
    # define particle positions in object's local frame
    num_particles_x = num_springs_x + 1
    num_particles_y = num_springs_y + 1
    pos_local = np.zeros(
        (num_particles_y, num_particles_x, 3), dtype=np.float32)
    for row_idx in range(num_particles_y):
        for col_idx in range(num_particles_x):
            pos_local[row_idx, col_idx] = np.array(
                [col_idx * spring_l0_col, -row_idx * spring_l0_row, 0.0],
                dtype=np.float32)
            
    # define springs. We define horizontal (col) springs first, then
    # vertical (row) springs, and finally and optionally, diagonal
    # springs
    num_springs = 2 * num_springs_y * num_springs_x + \
        num_springs_y + num_springs_x
    if diagonal:
        num_springs += num_springs_y * num_springs_x
    springs = np.zeros((num_springs, 2), dtype=np.int32)
    spring_l0s = np.zeros((num_springs, 1), dtype=np.float32)
    for row_idx in range(num_particles_y):
        for col_idx in range(num_springs_x):
            spring_idx = row_idx * num_springs_x + col_idx
            springs[spring_idx] = np.array(
                [row_idx * num_particles_x + col_idx,
                row_idx * num_particles_x + col_idx + 1],
                dtype=np.int32)
            spring_l0s[spring_idx] = spring_l0_col
    num_springs_h = num_particles_y * num_springs_x
    for row_idx in range(num_springs_y):
        for col_idx in range(num_particles_x):
            spring_idx = num_springs_h + row_idx * num_particles_x + col_idx
            springs[spring_idx] = np.array(
                [row_idx * num_particles_x + col_idx,
                (row_idx + 1) * num_particles_x + col_idx],
                dtype=np.int32)
            spring_l0s[spring_idx] = spring_l0_row
    if diagonal:
        num_springs_v = num_particles_x * num_springs_y
        for row_idx in range(num_springs_y):
            for col_idx in range(num_springs_x):
                spring_idx = num_springs_h + num_springs_v + \
                    row_idx * num_springs_x + col_idx
                springs[spring_idx] = np.array(
                    [row_idx * num_particles_x + col_idx,
                    (row_idx + 1) * num_particles_x + col_idx + 1],
                    dtype=np.int32)
                spring_l0s[spring_idx] = np.sqrt(
                    spring_l0_row**2 + spring_l0_col**2)

    return springs, pos_local.reshape(-1, 3), spring_l0s