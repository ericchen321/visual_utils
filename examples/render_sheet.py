# Author: Guanxiong
# render an animated sheet and save to a USD file


import os
import numpy as np
from tqdm import tqdm
import warp as wp
from visual_utils.io import (
    ParamName,
    DataName,
    load_data_from_h5)
from visual_utils.render import render_usd


wp.init()


def main():
    # make dir to store outputs
    out_dir = "outputs/render_sheet/"
    os.makedirs(out_dir, exist_ok=True)

    # load data
    dict_params, dict_data = load_data_from_h5(
        "assets/elastic_sheet.h5")

    # extract particle positions and spring list
    xpos_particles = dict_data[DataName.XPOS_PARTICLES]
    sim_substeps = dict_params[ParamName.SIM_SUBSTEPS]
    xpos_particles = xpos_particles[:, ::sim_substeps]
    springs = dict_params[ParamName.SPRING_TPLGY]

    # build the time vector
    frame_dt = dict_params[ParamName.FRAME_DT]
    sim_frames = dict_params[ParamName.SIM_FRAMES]
    times = frame_dt * np.arange(sim_frames)

    # render each rollout to a USD file
    num_rollouts = xpos_particles.shape[0]
    for rollout_idx in tqdm(range(num_rollouts)):
        usd_path = f"{out_dir}/rollout_{rollout_idx:02d}.usd"
        render_usd(
            xpos_particles[rollout_idx],
            springs,
            times,
            usd_path)


if __name__ == "__main__":
    main()