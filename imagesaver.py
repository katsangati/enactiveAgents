import pygame


class ImageSaver:
    """
    Class that implements image saving and output.
    """
    def __init__(self, output_path):
        self.output_path = output_path
        self.TIMESTEP = 1

    def save_next_img(self, screen):
        pygame.image.save(screen, self.output_path + str(format(self.TIMESTEP, '03'))+".jpeg")
        self.TIMESTEP += 1