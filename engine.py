# Engine for re-use in other games

import pygame.freetype
class Button:
    #   (start x , start y, length, height), text, font-size, font-colour,
    # text = button text
    # text_return = text to return when pressed
    # button details =  start x , start y, width, height, colour, style
    # font details = font-size, font-colour
    #def __init__(self, surface, position_x, position_y, text, size, colour, level, button_width, button_height):
    def __init__(self, surface, text, text_return, position_x, position_y, button_width,
                 button_height, colour, colour_on, style, size, font_colour, border, border_colour):
        self.position_x = position_x
        self.position_y = position_y
        self.text = text
        self.text_return = text_return
        self.font_size = size
        self.colour = colour
        self.colour_on = colour_on
        self.button_width = button_width
        self.button_height = button_height
        self.active = False
        self.surface = surface
        self.font_colour = font_colour
        self.border = border
        self.border_colour = border_colour
        self.style = style
        self.my_ft_font = pygame.freetype.Font("venv/fonts/ModernDOS4378x8.ttf", size)
        self.text_length = self.my_ft_font.get_rect(self.text, size=self.font_size)

        self.button_colour = self.colour
        if self.text_return == "text":
            print("text")
            self.text_position_x = self.position_x
            self.text_position_y = self.position_y

        else:
            #if text is too big it will print as many characters as it can fit
            while len(self.text)*self.font_size >= self.button_width:
                self.text =  self.text[:-1]
                print(self.text)
            text_position_x = position_x + (self.button_width / 2) - (self.my_ft_font.get_rect(self.text, size=size)[2]) / 2
            text_position_y = position_y + (self.button_height / 2) - (self.my_ft_font.get_rect(self.text, size=size)[3]) / 2
            print(position_x, (self.button_width / 2), (len(text) * size) / 2)

            self.text_position_x = self.position_x + (self.button_width / 2) - (
                self.my_ft_font.get_rect(self.text, size=self.font_size)[2]) / 2
            self.text_position_y = self.position_y + (self.button_height / 2) - (
                self.my_ft_font.get_rect(self.text, size=self.font_size)[3]) / 2



        #print("Test_Length", text_length)
        #pygame.draw.rect(self.surface, self.colour, (position_x, position_y, self.button_width, self.button_height))
        #self.my_ft_font.render_to(self.surface, (text_position_x, text_position_y), self.text, self.font_colour)

        self.button_draw()


    def button_switch(self):
        print("HIT", self.text_return)
        #print(self.position_x, self.position_y, self.button_width, self.button_height)
        if self.active == False:
            self.button_colour = self.colour_on
            self.active = True
        else:
            self.button_colour = self.colour
            self.active = False
        print("Self Active is now ", self.active)
        self.button_draw()


    def button_draw(self):
        pygame.draw.rect(self.surface, self.button_colour,
                             (self.position_x, self.position_y, self.button_width, self.button_height), 0, 0)
        if self.border != 0:
            pygame.draw.rect(self.surface, self.border_colour,
                             (self.position_x, self.position_y, self.button_width, self.button_height), self.border, 0)

        # print("Test_Length", text_length)
        self.my_ft_font.render_to(self.surface, (self.text_position_x, self.text_position_y), self.text, self.font_colour)

    def check_if_pressed(self, position):
        if position[0] >= self.position_x and \
                position[0] <= self.position_x + self.button_width and \
                position[1] >= self.position_y and \
                position[1] <= self.position_y + self.button_height:
            self.button_switch()

class Text:
    # Creates a Text object using the screen sizes (x - horizontal, y - virtical position)
    def __init__(self, surface, text, position_x, position_y, colour, background_colour, font_size):
        self.x = position_x
        self.y = position_y
        self.position_x = position_x * font_size
        self.position_y = position_y * font_size
        self.text = text
        self.colour = colour
        self.background_colour = background_colour
        #self.background_colour = None
        self.surface = surface
        self.size = font_size
        self.my_ft_font_text = pygame.freetype.Font("venv/fonts/ModernDOS4378x8.ttf", self.size)
        self.text_length = self.my_ft_font_text.get_rect(self.text)


    def text_draw(self):
        # Draw the background color
        #pygame.draw.rect(self.surface, self.background_colour,
         #                    (self.position_x, self.position_y, self.text_length.width, self.text_length.height), 0, 0)

        # print("Test_Length", text_length)
        self.my_ft_font_text.render_to(self.surface, (self.position_x, self.position_y),
                                       self.text, self.colour, self.background_colour, size=self.size)

    def recalculate(self):
        # Recalculate when the screen changes
        self.position_x = self.x * self.size
        self.position_y = self.y * self.size


class Wait_for_key_press:
    def __init__(self):
        self.wait = True

    def update(self,surface):
        pygame.event.clear()
        while self.wait:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.wait = False
                return "finish"
            elif event.type == pygame.KEYDOWN:
                self.wait = False


class Dialogue:
    # Dialogue consists of text message and an ok button def ok does this
    # Def for more complex dialogues to be added. Expecting (yes, no, cancel), possible options, text entry maybe
    def __init__(self, surface, text_header,  text, text_return, style):
        self.text = text
        self.text_return = text_return
        self.active = False
        self.surface = surface
        self.MaxLine = 0
        # style of dialogue can be changed
        self.style = style
        self.text_header = text_header
        if style == "windows":
            self.style_windows()

        else:
            self.style_default()
        # work out the number of lines
        count = 0
        for line in self.text:
            count = count + 1
            test = self.my_ft_font.get_rect(line)[2]
            print("Test", test)
            if self.MaxLine < test:
                self.MaxLine = test
            print("MaxLine", self.MaxLine)
        #set dimensions based on text attributes
        self.dialogue_width = self.MaxLine + (self.size * 2)
        self.dialogue_height = (count + 4) * self.size
        screen_width = self.surface.get_width() / 2
        screen_height = self.surface.get_height() / 2
        self.position_x = screen_width - (self.dialogue_width / 2)
        self.position_y = screen_height - (self.dialogue_height /2)

        #need to add options for the type of dialogue
        self.ok()

    def style_windows(self):
        self.size = 12
        self.my_ft_font = pygame.freetype.Font("venv/fonts/sans.ttf", self.size)
        self.font_colour = (0, 0, 0)
        self.colour = (227, 227, 227)


    def style_default(self):
        #Default style is deliberately 8 bit style
        self.size = 16
        self.font_colour = (0, 0, 0)
        self.colour = (255, 0, 0)
        self.my_ft_font = pygame.freetype.Font("venv/fonts/ModernDOS4378x8.ttf", self.size)


    def ok(self):
        # OK just has the one button
        self.sub_buttons = []
        #draw dialogue
        self.draw_dialogue()
        # If windows style needs a blue border
        if self.style == "windows":
            self.border = 1
            self.border_colour = (0,0,255)
        else:
            self.border = 2
            self.border_colour = self.font_colour

        #Add an OK button (go for reverse colours for simplicity at this point)
        self.sub_buttons.append(Button(self.surface, "OK", "ok", (self.position_x + (self.dialogue_width / 2) - 2 * self.size),
                    (self.position_y + self.dialogue_height - (self.size * 2)),
                     self.size * 4, self.size * 1.5,self.colour, self.colour,self.style, self.size, self.font_colour, self.border, self.border_colour))
        self.active = False

        pygame.display.flip()
        self.wait_for_click()

    def wait_for_click(self):
        dialogue = True
        clock = pygame.time.Clock()
        while dialogue:
            clock.tick(30)
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    for d in self.sub_buttons:
                        d.check_if_pressed(position)
                        if d.active == True and d.text_return == "ok":
                                self.surface.fill((0,0,0))
                                dialogue = False
                        if d.active == True and d.text_return == "x":
                                self.surface.fill((0,0,0))
                                dialogue = False
                    print(position)
                    if position[0] >= self.position_x and position[0] <= self.position_x + self.dialogue_width:
                        print("right",self.position_x)
                        print("left", self.position_x + self.dialogue_width)
                    if position[1] >=self.position_y and position[1] <=self.position_y + self.dialogue_height:
                        print("top",self.position_y)
                        print("bottom", self.position_y + self.dialogue_height )
                    print("========")
    def draw_dialogue(self):
        # Need how to calculate this based on text size. (Text wrap, how to do this)
        # also will go for the centre of the screen
        # possible scroll bar (might not work all that well)
        # add number of buttons here and calculate and create sub-buttons
        print(self.surface)

        #Header white
        pygame.draw.rect(self.surface, (255, 255, 255),
                         (self.position_x, self.position_y -  self.size * 1.5 ,
                          self.dialogue_width,  self.size * 1.5), 0, 0)
        # Header Text
        self.my_ft_font.render_to(self.surface, (self.position_x  + (self.size / 2),
                                                 self.position_y - self.size),
                                                self.text_header, self.font_colour)

        # Header button X (top right) - will always use Windows font so no too chunky
        self.sub_buttons.append(
            Button(self.surface, "X", "x", (self.position_x + self.dialogue_width - (self.size * 2)),
                   (self.position_y - (self.size * 1.25) ),
                   self.size * 2, self.size * 1.25, (255,255,255), self.colour,"windows", self.size * 1.2, (0,0,0),0,0))

        #solid background
        pygame.draw.rect(self.surface, self.colour,
                         (self.position_x, self.position_y, self.dialogue_width, self.dialogue_height), 0, 0)
        #white edging
        pygame.draw.rect(self.surface, (255,255,255),
                         (self.position_x, self.position_y, self.dialogue_width, self.dialogue_height), 1, 0)


        text_position_x = self.position_x + (self.dialogue_width / 2) - (self.MaxLine) / 2

        text_position_y = self.position_y + self.size
        for line in self.text:
                text_position_x = self.position_x + (self.dialogue_width / 2) - (self.my_ft_font.get_rect(line)[2]) / 2
                self.my_ft_font.render_to(self.surface, (text_position_x, text_position_y), line, self.font_colour)
                text_position_y = text_position_y + self.size



