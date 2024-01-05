import sys

import pygame.font


class Menu:
    """A class to build the menu"""

    def __init__(self, grav_sim):
        """Initialize button attributes."""
        self.screen = grav_sim.screen

        self.menu_active == False

        self.resume_button = Button(grav_sim, 0.8, "Resume")
        self.exit_button = Button(grav_sim, 1.2, "Exit")
        

    def menu_active(self):
        return self.menu_active

    def draw(self):
        self.resume_button.draw()
        self.exit_button.draw()

    def _check_button(self, mouse_pos):
        if self.resume_button.rect.collidepoint(mouse_pos):
            self.menu_active = False
        if self.exit_button.rect.collidepoint(mouse_pos):
            sys.exit()
        


class Button:
    """A class to build buttons"""

    def __init__(self, grav_sim, height_factor, msg):
        """Initialize button attributes."""
        self.screen = grav_sim.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width = 0.25 * grav_sim.settings.SCREEN_WIDTH
        self.height = 0.1 * grav_sim.settings.SCREEN_HEIGHT

        self.button_color = (245, 245, 245)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = height_factor * self.screen_rect.centery

        # The button message needs to be printed only once.
        self._print_msg(msg)

    def _print_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
