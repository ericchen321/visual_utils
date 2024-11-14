# Visualization utilities for WARP projects

This repo contains utility functions for your WARP projects, including one that renders a mass-spring system to a USD file.

## Installation
1. Install Git LFS.
2. Recursively clone the repo and its submodule:
```
git clone --recurse-submodules -j8 <url to the repo>
```
3. Install conda and create a conda environment.
4. Install packages in `requirements.txt`.
5. Go to `render_usd.render_cylinder()` of your **local** WARP installation. Replace the implementation of the function with the implementation provided in this codebase.

## Example
Run `python/examples/render_sheet.py` to render simulations of a mass-spring sheet to USD files.

## APIs
`visual_utils.sheet.define_rectangular_sheet()`: Define a 2D, rectangular-shaped sheet of particles and springs

`visual_utils.render.render_usd()`: Renders a rollout of a mass-spring
system to a USD file