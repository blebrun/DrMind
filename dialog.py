import pygame


class DialogBox:

    X_POSITION = 60
    Y_POSITION = 470

    def __init__(self):
        self.box = pygame.image.load(f'assets/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = self.upload_dialog('intro')
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font(f'assets/dialogs/dialog_font.ttf', 18)
        self.reading = False

    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    # Afficher la boire de dialogue + le texte
    def render(self, screen):

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            if self.letter_index <45:
                text1 = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
                screen.blit(text1, (self.X_POSITION + 50, self.Y_POSITION + 20))

            elif self.letter_index <90:
                text1 = self.font.render(self.texts[self.text_index][0:45], False, (0, 0, 0))
                text2 = self.font.render(self.texts[self.text_index][45:self.letter_index], False, (0, 0, 0))
                screen.blit(text1, (self.X_POSITION + 50, self.Y_POSITION + 20))
                screen.blit(text2, (self.X_POSITION + 50, self.Y_POSITION + 40))
            else:
                text1 = self.font.render(self.texts[self.text_index][0:45], False, (0, 0, 0))
                text2 = self.font.render(self.texts[self.text_index][45:90], False, (0, 0, 0))
                text3 = self.font.render(self.texts[self.text_index][91:self.letter_index], False, (0, 0, 0))
                screen.blit(text1, (self.X_POSITION + 50, self.Y_POSITION + 20))
                screen.blit(text2, (self.X_POSITION + 50, self.Y_POSITION + 40))
                screen.blit(text3, (self.X_POSITION + 50, self.Y_POSITION + 60))

    # Passer à la ligne de dialogue suivante
    def next_text(self):
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False
            pygame.mixer.music.set_volume(0.2)

    def upload_dialog(self, nom):
        dialog = []
        with open(f'assets/sprites/{nom}.txt', encoding='utf8') as txt:
            while True:
                line1 = txt.readline()
                for line2 in line1:
                    line2 = line1.replace("\r", "").replace("\n", "")
                if not line1:
                    break
                dialog.append(line2)
        return dialog

    def execute_intro(self, screen):
        pygame.time.Clock().tick(60)
        self.reading = True
        if self.text_index < len(self.texts):
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.execute(screen)
        else:
            self.reading = False













