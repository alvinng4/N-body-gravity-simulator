import sys

import pygame
import pygame.gfxdraw
from pygame.sprite import Sprite


class Grav_obj(Sprite):
    def __init__(
        self, grav_sim, params: dict, real_scale, name: str = None, img_path: str = None
    ):
        super().__init__()
        self.screen = grav_sim.screen
        self.camera = grav_sim.camera
        self.settings = grav_sim.settings
        self.color = self.settings.grav_obj_color
        if not name.strip().title() == "Sun":
            self.img_scale = grav_sim.settings.img_scale
        else:
            self.img_scale = 1

        self.params = params
        self.diameter = real_scale * self.img_scale * self.settings.screen_height
        if img_path:
            try:
                load_image = pygame.image.load(img_path).convert_alpha()
                self.image = pygame.transform.scale(
                    load_image, (self.diameter, self.diameter)
                )
                self.rect = self.image.get_rect()
            except FileNotFoundError:
                sys.exit(
                    "Error: Image not found. Check that you are in the correct directory, and the image path provided for Grav_obj is correct."
                )

        self.rect.centerx = self.params["x"]
        self.rect.centery = self.params["y"]

    def update(self):
        """Update the apparent position of all grav_objs with camera"""
        self.rect.center = (
            self.params["x"] - self.camera.pos_x,
            self.params["y"] - self.camera.pos_y,
        )

    @classmethod
    def create_solor_system(self, grav_sim):
        centerx = grav_sim.screen.get_rect().centerx
        centery = grav_sim.screen.get_rect().centery
        sun = Grav_obj(
            grav_sim, {"x": centerx, "y": centery}, 0.05, "Sun", "images/sun.png"
        )
        mercury = Grav_obj(
            grav_sim,
            {"x": 1.1 * centerx, "y": centery},
            0.0005,
            "Mercury",
            "images/mercury.png",
        )
        venus = Grav_obj(
            grav_sim,
            {"x": 1.2 * centerx, "y": centery},
            0.0005,
            "Venus",
            "images/venus.png",
        )
        earth = Grav_obj(
            grav_sim,
            {"x": 1.3 * centerx, "y": centery},
            0.0005,
            "Earth",
            "images/earth.png",
        )
        mars = Grav_obj(
            grav_sim,
            {"x": 1.5 * centerx, "y": centery},
            0.0005,
            "Mars",
            "images/mars.png",
        )
        jupiter = Grav_obj(
            grav_sim,
            {"x": 1.8 * centerx, "y": centery},
            0.0005,
            "Jupiter",
            "images/jupiter.png",
        )
        saturn = Grav_obj(
            grav_sim,
            {"x": 2 * centerx, "y": centery},
            0.0005,
            "Saturn",
            "images/saturn.png",
        )
        uranus = Grav_obj(
            grav_sim,
            {"x": 4 * centerx, "y": centery},
            0.0005,
            "Uranus",
            "images/uranus.png",
        )
        neptune = Grav_obj(
            grav_sim,
            {"x": 5 * centerx, "y": centery},
            0.0005,
            "Neptune",
            "images/neptune.png",
        )
        grav_sim.grav_objs.add(sun)
        grav_sim.grav_objs.add(mercury)
        grav_sim.grav_objs.add(venus)
        grav_sim.grav_objs.add(earth)
        grav_sim.grav_objs.add(mars)
        grav_sim.grav_objs.add(jupiter)
        grav_sim.grav_objs.add(saturn)
        grav_sim.grav_objs.add(uranus)
        grav_sim.grav_objs.add(neptune)

    @classmethod
    def create_figure_8(self, grav_sim):
        pass
