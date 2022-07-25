import pygame


class Inventory:

    # Paramètres inventaire fermé (x, y, width, height)
    closebox = (40, 520, 40, 40)
    position_text_x = 56
    position_text_y = 522

    # Paramètre pour inventaire ouvert
    openbox = (100, 100, 600, 400)
    openborder = (98, 98, 604, 404)
    mdp_x = 110
    mdp_y = 460

    # Couleur du texte
    colortext = (80,80,80)





    def __init__(self):

        self.inventory_box = pygame.image.load(f'assets/dialogs/dialog_box.png')
        self.open_invent = False
        self.font_close = pygame.font.Font(f'assets/dialogs/dialog_font.ttf', 26)
        self.font_open = pygame.font.Font(f'assets/dialogs/dialog_font.ttf', 14)





    def inventory_open_close(self, screen, mdp):

        if self.open_invent:

            # Cadre
            pygame.draw.rect(screen, (240, 240, 240), self.openbox)
            pygame.draw.rect(screen, (80, 80, 80), self.openborder, 2, 2, 2, 2)

            # Objet 1
            pygame.draw.rect(screen, self.colortext, (150, 120, 150, 200), 2, 2, 2, 2)
            obj_svg_1 = self.font_open.render("Vide", False, self.colortext)
            screen.blit(obj_svg_1, (210, 200))

            # Objet 2
            pygame.draw.rect(screen, self.colortext, (150+(150+25), 120, 150, 200), 2, 2, 2, 2)
            obj_svg_2 = self.font_open.render("Vide", False, self.colortext)
            screen.blit(obj_svg_2, (210+170, 200))

            # Objet 3
            pygame.draw.rect(screen, self.colortext, (150+(150+25)*2, 120, 150, 200), 2, 2, 2, 2)
            obj_svg_3 = self.font_open.render("Vide", False, self.colortext)
            screen.blit(obj_svg_3, (210+345, 200))

            # Mot de passe
            #pygame.draw.rect(screen, self.colortext, (self.mdp_x, self.mdp_y, 260, 30), 2, 2, 2, 2)
            mdp = self.font_open.render(f'Mot de passe : {mdp}', False, self.colortext)
            screen.blit(mdp, (self.mdp_x+10, self.mdp_y+5))

            # Info touche retour au menu
            pygame.draw.rect(screen, self.colortext, (self.mdp_x,self.mdp_y - 40,53,30), 2, 2, 2, 2)
            touche = self.font_open.render("esc    Revenir au menu", False, self.colortext)
            screen.blit(touche, (self.mdp_x + 10, self.mdp_y - 40 + 4))

            # Info touche retour au menu
            pygame.draw.rect(screen, self.colortext, (self.mdp_x, self.mdp_y - 80, 30, 30), 2, 2, 2, 2)
            touche = self.font_open.render("i    fermer l'inventaire", False, self.colortext)
            screen.blit(touche, (self.mdp_x + 10, self.mdp_y - 80 + 4))

            return

        else:
            pygame.draw.rect(screen, (190, 190, 190), self.closebox, 2, 2, 2, 2)
            text = self.font_close.render("i", False, (190, 190, 190))
            screen.blit(text, (self.position_text_x, self.position_text_y))
            return




