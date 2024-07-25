"""
Demonstration on using the gravity simulator to simulate the asteroid belt

Warning: This script will take a lot of storage space on your computer (probably a few GBs).
         It will attempt to erase the data after the video is generated.
"""

import csv
from pathlib import Path
import sys

import numpy as np
import PIL
import matplotlib.pyplot as plt

import gravity_sim


def main():
    grav_sim = gravity_sim.GravitySimulator()
    system = grav_sim.create_system()
    system.load("solar_system")
    system.remove(name="Mercury")
    system.remove(name="Venus")
    colors = [
        "orange",
        "skyblue",
        "red",
        "darkgoldenrod",
        "gold",
        "paleturquoise",
        "blue",
    ]
    marker_sizes = [6.0, 1.0, 1.0, 2.0, 1.5, 4.0, 3.5, 3.0, 3.0]

    # system.remove(name="Neptune")
    # system.remove(name="Uranus")
    # x, v = from_orbital_elements_to_cartesian(
    #     mp=1.0,
    #     ms=1.0,
    #     semimajor_axis=5.5,
    #     eccentricity=0.7,
    #     true_anomaly=np.radians(20.0),
    #     inclination=np.radians(0.4),
    #     argument_of_periapsis=np.radians(4.0),
    #     longitude_of_ascending_node=np.radians(4.0),
    #     G=system.G,
    # )
    # m = 1.0
    # system.add(x, v, m, objects_name="Added Star")
    # colors = ["orange", "skyblue", "red", "darkgoldenrod", "gold", "orange"]
    # marker_sizes = [6.0, 2.0, 1.5, 4.0, 3.5, 6.0]

    massive_objects_count = system.objects_count

    N = 50000

    rng = np.random.default_rng()
    a = rng.uniform(2.1, 3.2, size=N)  # Semi-major axis in AU
    ecc = rng.uniform(0.0, 0.2, size=N)  # Eccentricity
    inc = rng.uniform(-0.5, 0.5, size=N)  # Inclination in radians
    raan = rng.uniform(
        0, 360, size=N
    )  # Right ascension of the ascending node in degrees
    argp = rng.uniform(0, 360, size=N)  # Argument of perigee in degrees
    nu = rng.uniform(0, 360, size=N)  # True anomaly in degrees

    for i in range(N):
        x, v = from_orbital_elements_to_cartesian(
            mp=1.0,
            ms=0.0,
            semimajor_axis=a[i],
            eccentricity=ecc[i],
            true_anomaly=np.radians(nu[i]),
            inclination=np.radians(inc[i]),
            argument_of_periapsis=np.radians(argp[i]),
            longitude_of_ascending_node=np.radians(raan[i]),
            G=system.G,
        )

        system.add(x, v, 0.0)

    system.center_of_mass_correction()

    file_path = Path(__file__).parent / "gravity_sim" / "results"
    file_path.mkdir(parents=True, exist_ok=True)
    data_path = file_path / "astroid_belt_sim.csv"

    print("Simulating asteroid belt...")
    grav_sim.launch_simulation(
        system,
        "rk4",
        grav_sim.years_to_days(5.0),
        dt=grav_sim.years_to_days(0.001),
        store_every_n=10,
        acceleration="massless",
        flush=True,
        flush_results_path=str(data_path),
        no_print=True,
    )

    # Draw frames
    print()
    print("Drawing frames...")
    fig = plt.figure()
    plt.style.use("dark_background")
    ax = fig.add_subplot(111, projection="3d")

    xlim_min = -3
    xlim_max = 3
    ylim_min = -3
    ylim_max = 3
    zlim_min = -3
    zlim_max = 3

    # In the library, we use PillowWriter to generate animations.
    # However, for some reason, the PillowWriter run out of memory
    # in this case. Therefore, we save each frames as images and
    # combine them as gif instead.
    save_count = 0
    csv.field_size_limit(sys.maxsize)
    with open(data_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0].startswith("#"):
                continue

            row = row[3:]
            row = list(map(float, row))

            # Plot the trajectory from the beginning to current position
            for i in range(0, massive_objects_count):
                ax.grid(False)
                ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
                ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
                ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_zticks([])
                ax.xaxis.set_visible(False)
                ax.yaxis.set_visible(False)
                ax.zaxis.set_visible(False)
                ax.xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
                ax.yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
                ax.zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

                ax.plot(
                    np.array(row[i * 3]),
                    np.array(row[1 + i * 3]),
                    "o",
                    label=system.objects_names[i],
                    color=colors[i],
                    markersize=marker_sizes[i],
                )

            x = row[(massive_objects_count * 3) : (system.objects_count * 3) : 3]
            y = row[(massive_objects_count * 3 + 1) : (system.objects_count * 3) : 3]
            z = row[(massive_objects_count * 3 + 2) : (system.objects_count * 3) : 3]
            ax.scatter(
                x,
                y,
                z,
                color="white",
                marker=".",
                s=0.1,
                alpha=0.1,
            )

            # Add legend
            legend = ax.legend(loc="center right", bbox_to_anchor=(1.325, 0.5))
            legend.facecolor = "transparent"

            # Adjust figure for the legend
            if save_count == 0:
                fig.subplots_adjust(right=0.7)
                fig.tight_layout()

            # Set axis labels and setting 3d axes scale before capturing the frame
            # ax.set_xlabel("$x$ (AU)")
            # ax.set_ylabel("$y$ (AU)")
            # ax.set_zlabel("$z$ (AU)")

            ax.set_xlim3d([xlim_min, xlim_max])
            ax.set_ylim3d([ylim_min, ylim_max])
            ax.set_zlim3d([zlim_min, zlim_max])

            # Set equal aspect ratio to prevent distortion
            ax.set_aspect("equal")

            # Capture the frame
            plt.savefig(file_path / f"frames_{save_count:04d}.png", dpi=300)
            save_count += 1

            # Clear the plot to prepare for the next frame
            ax.clear()

        plt.close("all")

    print()
    print("Combining frames to gif...")
    frames = []
    for i in range(save_count):
        frames.append(PIL.Image.open(file_path / f"frames_{i:04d}.png"))

    frames[0].save(
        file_path / "astroid_belt.gif",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=34,
    )

    for i in range(save_count):
        (file_path / f"frames_{i:04d}.png").unlink()
    data_path.unlink()

    print(f"Output completed! Please check {file_path / 'astroid_belt.gif'}")
    print()


def from_orbital_elements_to_cartesian(
    mp,
    ms,
    semimajor_axis,
    eccentricity,
    true_anomaly,
    inclination,
    argument_of_periapsis,
    longitude_of_ascending_node,
    G,
):
    """

    Function that returns position and velocities computed from the input orbital
    elements. Angles in radians, inclination between 0 and 180

    Reference
    ---------
    https://github.com/MovingPlanetsAround/ABIE
    """

    cos_true_anomaly = np.cos(true_anomaly)
    sin_true_anomaly = np.sin(true_anomaly)

    cos_inclination = np.cos(inclination)
    sin_inclination = np.sin(inclination)

    cos_arg_per = np.cos(argument_of_periapsis)
    sin_arg_per = np.sin(argument_of_periapsis)

    cos_long_asc_nodes = np.cos(longitude_of_ascending_node)
    sin_long_asc_nodes = np.sin(longitude_of_ascending_node)

    ### e_vec is a unit vector directed towards periapsis ###
    e_vec_x = (
        cos_long_asc_nodes * cos_arg_per
        - sin_long_asc_nodes * sin_arg_per * cos_inclination
    )
    e_vec_y = (
        sin_long_asc_nodes * cos_arg_per
        + cos_long_asc_nodes * sin_arg_per * cos_inclination
    )
    e_vec_z = sin_arg_per * sin_inclination
    e_vec = np.array([e_vec_x, e_vec_y, e_vec_z])

    ### q is a unit vector perpendicular to e_vec and the orbital angular momentum vector ###
    q_vec_x = (
        -cos_long_asc_nodes * sin_arg_per
        - sin_long_asc_nodes * cos_arg_per * cos_inclination
    )
    q_vec_y = (
        -sin_long_asc_nodes * sin_arg_per
        + cos_long_asc_nodes * cos_arg_per * cos_inclination
    )
    q_vec_z = cos_arg_per * sin_inclination
    q_vec = np.array([q_vec_x, q_vec_y, q_vec_z])

    #    print 'alpha',alphax**2+alphay**2+alphaz**2 # For debugging; should be 1
    #    print 'beta',betax**2+betay**2+betaz**2 # For debugging; should be 1

    ### Relative position and velocity ###
    separation = (
        semimajor_axis
        * (1.0 - eccentricity**2)
        / (1.0 + eccentricity * cos_true_anomaly)
    )  # Compute the relative separation
    position_vector = (
        separation * cos_true_anomaly * e_vec + separation * sin_true_anomaly * q_vec
    )
    velocity_tilde = np.sqrt(
        G * (mp + ms) / (semimajor_axis * (1.0 - eccentricity**2))
    )  # Common factor
    velocity_vector = (
        -1.0 * velocity_tilde * sin_true_anomaly * e_vec
        + velocity_tilde * (eccentricity + cos_true_anomaly) * q_vec
    )

    return position_vector, velocity_vector


if __name__ == "__main__":
    main()
