# Author: Guanxiong


import warp as wp
import numpy as np
from warp.render import UsdRenderer
from visual_utils.kinematics import compute_spring_xform


def render_usd(
    xpos_particles: np.ndarray,
    springs: np.ndarray,
    times: np.ndarray,
    usd_path: str) -> None:
    r"""
    Render the rollout of a mass-spring system, and save to
    a USD file.

    Parameters:
        xpos_particles: Particle positions across frames
            (num_frames, num_particles, 3)
        springs: Indices of the particles connected by springs,
            i.e. edge list (num_springs, 2)
        times: Simulation time, in seconds, of each frame
            (num_frames, )
        usd_path: Path to save the USD file
    """
    # check input
    assert xpos_particles.ndim == 3
    num_frames = xpos_particles.shape[0]
    assert num_frames > 1, "Need at least 2 frames to render"
    assert times.shape[0] == num_frames

    # build renderer
    frame_dt = times[1] - times[0]
    renderer_usd = UsdRenderer(
        usd_path,
        up_axis="Y",
        fps=int(1.0 / frame_dt),
        scaling=1.0)
    
    # render    
    for frame_idx in range(num_frames):
        xpos_frame = xpos_particles[frame_idx]
        sim_time = times[frame_idx]
        render_usd_per_frame(
            renderer_usd,
            xpos_frame,
            springs,
            sim_time)
    
    # save
    renderer_usd.save()
    print(f"USD file saved to {usd_path}")


def render_usd_per_frame(
    renderer: UsdRenderer,
    xpos_particles: np.ndarray,
    springs: np.ndarray,
    time: float) -> None:
    r"""
    Render a mass-spring system in a single frame with a USD
    renderer.

    Parameters:
        renderer: The USD renderer to render the step
        xpos_particles: World-frame positions of the particles
            (num_particles, 3)
        springs: Indices of the particles connected by springs
            (num_springs, 2)
        time: The simulation time in seconds

    """
    renderer.begin_frame(time)
    # render each particle as a sphere
    for particle_idx in range(xpos_particles.shape[0]):
        renderer.render_sphere(
            f"particle_{particle_idx:02d}",
            xpos_particles[particle_idx],
            wp.quat_identity(),
            0.1,
            color=(1.0, 0.0, 0.0))
    # render each spring as a cylinder
    for spring_idx in range(springs.shape[0]):
        pos_part_a = xpos_particles[springs[spring_idx, 0]]
        pos_part_b = xpos_particles[springs[spring_idx, 1]]
        pos_spr, rot_spr, scale_spr = compute_spring_xform(
            pos_part_a, pos_part_b)
        renderer.render_cylinder(
            f"spring_{spring_idx:02d}",
            pos_spr,
            rot_spr,
            scale_spr,
            0.04,
            0.5,
            color=(0.0, 0.0, 1.0))
    renderer.end_frame()
    return
