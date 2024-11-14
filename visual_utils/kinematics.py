# Author: Guanxiong


import numpy as np
from typing import Tuple
from scipy.spatial.transform import Rotation as R


def compute_spring_xform(
    pos_part_a: np.ndarray,
    pos_part_b: np.ndarray) -> Tuple[
        np.ndarray, np.ndarray, np.ndarray]:
    r"""
    From a spring's two endpoints, compute the mid-point, rotation,
    and scale of the spring.

    Parameters:
        pos_part_a: Position of the first particle (3, )
        pos_part_b: Position of the second particle (3, )

    Returns:
        pos_spr: Position of the spring (3, )
        rot_spr: Rotation of the spring (4, )
        scale_spr: (Local) scale of the spring (3, )
    """        
    # compute position of spring
    pos_spr = 0.5 * (pos_part_a + pos_part_b)
    
    # compute scale of spring
    pos_rel = pos_part_b - pos_part_a
    height = np.linalg.norm(pos_rel)
    scale_spr = np.array([1.0, height, 1.0])
    
    # compute unitary direction vector of spring
    dvec_spr = pos_rel / (height + 1e-6)
    
    # compute axis vector of rotation
    up_vec = np.array([0.0, 1.0, 0.0])
    rot_axis = np.cross(up_vec, dvec_spr)
    rot_axis = rot_axis / (np.linalg.norm(rot_axis) + 1e-6)
    
    # compute angle of rotation
    dot_prod = np.dot(up_vec, dvec_spr)
    angle_spring = np.arccos(dot_prod)
    
    # build rotation object
    rot_spr_obj = R.from_rotvec(angle_spring * rot_axis)
    
    # extract rotation as a quaternion
    rot_spr = rot_spr_obj.as_quat()

    return pos_spr, rot_spr, scale_spr