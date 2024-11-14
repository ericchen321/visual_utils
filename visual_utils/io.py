# Author: Guanxiong


import h5py
import numpy as np
from typing import Dict, Tuple
from enum import Enum


class ParamName(str, Enum):
    PARTICLE_MASSES = "particle_masses"
    PARTICLE_RADII = "particle_radii"
    NUM_SPRINGS_ROW = "num_springs_row"
    NUM_SPRINGS_COL = "num_springs_col"
    PARTICLES = "particles"
    KIN_PARTICLES = "kin_particles"
    SPRING_TPLGY = "spring_topology"
    SPRING_KS = "spring_ks"
    SPRING_BS = "spring_bs"
    SPRING_L0S = "spring_l0s"
    SPRING_LIMIT_MAX_STRAIN = "spring_limit_max_strain"
    SPRING_STRAIN_MAXS = "spring_strain_maxs"
    SPRING_LIMIT_CMPR = "spring_limit_compression"
    SPRING_STRAIN_MINS = "spring_strain_mins"
    RAYLEIGH_B = "rayleigh_b"
    XPOS_PARTICLES_REST = "xpos_particles_rest"
    GRAV_CONST = "grav_const"
    GROUND = "ground"
    FRAME_DT = "frame_dt"
    SIM_DURATION = "sim_duration"
    SIM_FRAMES = "sim_frames"
    SIM_SUBSTEPS = "sim_substeps"
    SIM_DT = "sim_dt"
    SIM_STEPS = "sim_steps"


class DataName(str, Enum):
    # particle kinematics
    XPOS_PARTICLES = "xpos_particles"
    XVEL_PARTICLES = "xvel_particles"
    DIST_SIGNED = "dist_signed"
    SPRING_L = "spring_length"
    STRAIN = "strain"
    SE3_PARTICLES = "se3_particles"
    SO3_ORTH_ERRS = "so3_orth_errs"
    FEAS = "feasibility"
    # particle dynamics
    XFRC_PARTICLES = "xfrc_particles"
    XFRC_CAUG_GT = "xfrc_caug_gt"
    XFRC_CAUG_PRED = "xfrc_caug_pred"
    XFRC_ELASTIC = "xfrc_elastic"
    XFRC_DAMPING = "xfrc_damping"
    XFRC_BARRIER = "xfrc_barrier"
    XFRC_EXTERNAL = "xfrc_external"
    E_ELASTIC = "e_p_elastic"
    E_GRAV = "e_p_gravity"
    E_KINETIC = "e_k"
    E_TOTAL = "e_total"
    E_CAUG_GT = "e_caug_gt"
    E_CAUG_PRED = "e_caug_pred"
    # spring dynamics
    XFRC_ELASTIC_SPRS = "xfrc_elastic_sprs"
    XFRC_DAMPING_SPRS = "xfrc_damping_sprs"
    XFRC_BARRIER_SPRS = "xfrc_barrier_sprs"
    XFRC_SPRS = "xfrc_sprs"


def load_data_from_h5(
    h5_path: str) -> Tuple[
        Dict[str, np.ndarray], Dict[str, np.ndarray]]:
    r"""
    Load data of a sequence from an H5 file.

    Parameters:
        h5_path: Path to the H5 file.

    Return:
        A tuple of dictionaries:
        1) dict of sim params, 2) dict of sim data.
    """
    # init
    dict_params = {}
    dict_data = {}
    param_names = list(ParamName)
    data_names = list(DataName)

    # read
    with h5py.File(h5_path, "r") as h5file:
        for field_name, data in h5file.items():
            if field_name in param_names:
                dict_params[field_name] = np.array(data[()])
            elif field_name in data_names:
                dict_data[field_name] = np.array(data[:])
            else:
                raise ValueError(f"Unknown data name: {field_name}")
    print(f"Simulation params and data loaded from {h5_path}")
    return dict_params, dict_data