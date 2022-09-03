# Match 3 Retro style game
# Import and initialize the pygame library
# screen defined is split 40 wide and 30 high (retro stylie)
import time

import pygame
import random
import engine
from itertools import cycle

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.contact = False
        self.image = pygame.image.load("venv/graphics/target.png").convert_alpha()
        self.rect = self.image.get_rect()

    def update(self):

        self.rect.center = (self.x, self.y)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, screen):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 1
        self.colour = colour
        self.screen = screen
        self.screen_bound = int(self.screen.get_height())
        self.moving = True
        self.bottom_brick = False
        self.match = False

        #same stat needed in game class - level (may change to global variable)
        self.scale_up = (64,32)
        # add animation details
        self.images = []
        self.images.append(
            pygame.transform.scale(pygame.image.load("venv/graphics/blue1.png").convert_alpha(),self.scale_up))
        self.images.append(
            pygame.transform.scale(pygame.image.load("venv/graphics/green1.png").convert_alpha(), self.scale_up))
        self.images.append(
            pygame.transform.scale(pygame.image.load("venv/graphics/red1.png").convert_alpha(), self.scale_up))
        self.images.append(
            pygame.transform.scale(pygame.image.load("venv/graphics/pink1.png").convert_alpha(), self.scale_up))
        self.images.append(
            pygame.transform.scale(pygame.image.load("venv/graphics/dblue1.png").convert_alpha(), self.scale_up))

        self.image = self.images[colour]
        self.rect = self.image.get_rect()

    def update(self):
        if self.moving == False and self.dy != 0:
            self.y -= self.dy
            self.dy = 0
        self.hit_bottom_row()
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = (self.x, self.y)

    def hit_bottom_row(self):
        # check for the end of the screen
        check = self.y + self.scale_up[1]
        if check >= int(self.screen.get_height()):
            self.dy = 0
            self.bottom_brick = True

    def update_colour(self):
        self.image = self.images[self.colour]



class Game():
        def __init__(self):
            # Set up the drawing window
            self.screen_width = 640
            self.screen_height = 480
            self.text_rows = 30
            self.text_columns = 40

            self.screen = pygame.display.set_mode([self.screen_width, self.screen_height], pygame.DOUBLEBUF,8)

            self.level_playing = ""
            self.font_size = 16

            self.screen_resize()
            self.x = 0
            self.y = 0

            self.score = 0
            self.sound_setting = "on"
            self.blocks_match_sound = pygame.mixer.Sound("venv/sounds/blocks_match.ogg")
            self.end_game_sound = pygame.mixer.Sound("venv/sounds/End_game.ogg")
            self.finish_level_sound = pygame.mixer.Sound("venv/sounds/finish_level.ogg")

        # Decided not to implement in this game - fixed screen size instead
        def screen_resize(self):
            # Do not want to break the screen ratio of 3:2 so need to resize back to this
            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()
            self.width = int(self.screen_width / self.text_columns)
            self.height = int(self.screen_height / self.text_rows )
            self.font_size = min(self.width, self.height)
            #print("New font size is: ",self.font_size)
            self.my_ft_font = pygame.freetype.Font("venv/fonts/ModernDOS4378x8.ttf", self.font_size)
            self.screen_width = self.font_size * self.text_columns
            self.screen_height = self.font_size * self.text_rows

        # Trying to simplify, how you work out where button is
        def screen_position(self, row, column):
            self.x = (row - 1) * self.font_size
            self.y = (column - 1) * self.font_size

        def menu(self):
            # shows the main game menu
            # Run until the user asks to quit
            running = True
            # Fill the background
            # self.screen.fill((0, 0, 0))
            # background = pygame.image.load("venv/graphics/space.png").convert()
            # self.screen.blit(background, (0, 0))
            # background = background.convert_alpha()
            clock = pygame.time.Clock()

            #list created for any text on the menu screen
            my_text = []
            my_text.append(engine.Text(self.screen,"MATCH 3",3.3,1,(255,255,255),
                                       (255,0,0),self.font_size * 3))
            my_text.append(engine.Text(self.screen, "Up/down Arrow = scroll", 10, 8,
                                       (0, 255, 255), (0, 0, 0), self.font_size))
            my_text.append(engine.Text(self.screen, "left/right    = move", 10, 9,
                                       (0, 255, 255), (0, 0, 0), self.font_size))
            my_text.append(engine.Text(self.screen, "Up/down to change menu option", 7, 11,
                                       (0, 255, 255), (0, 0, 0), self.font_size))
            my_text.append(engine.Text(self.screen, "  Enter to select, or mouse ", 7, 12,
                                       (0, 255, 255), (0, 0, 0), self.font_size))
            sound = "Sound is:" + self.sound_setting
            my_text.append(engine.Text(self.screen, sound, 14, 13,
                                       (0, 255, 255), (0, 0, 0), self.font_size))

            # Add buttons (can have as many as you want in a screen in your list)
            my_buttons = []
            self.screen_position(15, 12)
            my_buttons.append(
                engine.Button(self.screen, "Play", "play", self.y, self.x, 300, 50, (0, 0, 255), (255, 0, 255),
                              "default", 32, (255, 255, 255), 5, (200, 200, 200)))
            self.screen_position(18, 12)
            my_buttons.append(
                engine.Button(self.screen, "Sound", "sound", self.y, self.x, 300, 50, (0, 0, 255), (255, 0, 255),
                            "default", 32, (255, 255, 255), 5, (200, 200, 200)))
            self.screen_position(21, 12)
            my_buttons.append(
                engine.Button(self.screen, "Credits", "credits", self.y, self.x, 300, 50, (0, 0, 255), (255, 0, 255),
                            "default", 32, (255, 255, 255), 5, (200, 200, 200)))
            self.screen_position(24, 12)
            my_buttons.append(
                engine.Button(self.screen, "Quit", "quit", self.y, self.x, 300, 50, (0, 0, 255), (255, 0, 255),
                              "default", 32, (255, 255, 255), 5, (200, 200, 200)))

            current_button = cycle(my_buttons)
            button = next(current_button)
            button.button_switch()

            while running:
                clock.tick(30)
                time_delta = clock.tick(60) / 1000.0
                self.screen.fill((0, 0, 0))

                for text_show in my_text:
                    text_show.text_draw()

                for _3 in my_buttons:
                    _3.button_draw()
                # Did the user click the window close button?
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        self.level_playing = "finish"
                    # No longer needed as screen is fixed
                    elif event.type == pygame.VIDEORESIZE:
                        self.screen_resize()
                        for f in my_text:
                            f.size = self.font_size
                            f.recalculate()
                        for f2 in my_buttons:
                            f.size = self.font_size

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for _ in my_buttons:
                            if _.active == True:
                                active_button = _
                                _.button_switch()
                        # This will check for any button presses
                        position = pygame.mouse.get_pos()
                        for _ in my_buttons:

                            _.check_if_pressed(position)
                            # If any buttons are active you can add what you want to happen here
                            if _.active == True and _.text_return == "credits":
                                # example of a dialogue of 'OK'
                                dialogue1 = engine.Dialogue(self.screen,"Credits",
                                                            ["Graphics and game: Adam Thirlwell (thirlwella@gmail.com)",
                                                            "Code license: GNU General Public License v3.0",
                                                            "",
                                                            "Font: downloaded from Fonts2u.com",
                                                            "license: GNU/GPL",
                                                            "",
                                                            "Sounds:",
                                                            "sampled from https://mixkit.co/free-sound-effects/game/",
                                                             "royalty free files",],
                                                            "ok"
                                                            , "windows")
                                _.button_switch()
                            elif _.text_return == "play" and _.active ==True:
                                running = False
                                _.active = False
                                self.level_playing = "level1"
                            elif _.text_return == "quit" and _.active == True:
                                running = False
                                self.level_playing = "finish"
                            elif _.text_return == "sound" and _.active == True:
                                if self.sound_setting == "on":
                                    self.sound_setting = "off"
                                else:
                                    self.sound_setting = "on"
                                self.level_playing = "menu"
                                running = False

                        #active_button.active.

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            for _ in my_buttons:
                                if _.active == True and _ != button:
                                    _.button_switch()
                            if button.active == True:
                                button.button_switch()
                            button = next(current_button)
                            if button.active == False:
                                button.button_switch()
                        if event.key == pygame.K_UP:
                            for _ in my_buttons:
                                if _.active == True and _ != button:
                                    _.button_switch()
                            if button.active == True:
                                button.button_switch()
                            for i in range(1, len(my_buttons)):
                                button = next(current_button)
                            if button.active == False:
                                button.button_switch()
                        if event.key == pygame.K_RETURN:
                            if button.text_return == "play":
                                running = False
                                self.level_playing = "level1"
                            if button.text_return == "quit":
                                running = False
                                self.level_playing = "finish"
                            button.button_switch()

                # Flip the display
                pygame.display.flip()

        def level(self, level):

            # Run until the user asks to quit
            running = True
            self.player = (224,000)
            self.drop_speed = 3 + level
            self.block_height = 32
            self.block_width = 64
            self.limit = 2
            self.column = 0
            self.blocks_were_moving = False
            self.blocks_are_moving = False
            clock = pygame.time.Clock()
            self.first_loop = True
            self.level_timer = 1000 # keeping simple to start with may need to use a timer
            self.show_matching = False
            # Set up level Text details
            level_text = []

            current_level = "LEVEL: " + str(level)
            level_text.append(engine.Text(self.screen, current_level, 27, 5, (255, 0, 0),
                                          None, self.font_size))

            score = engine.Text(self.screen, "SCORE: ", 27, 7, (255, 255, 0),
                                         None, self.font_size)

            level_text.append(engine.Text(self.screen, "Up Next:", 27, 10, (255, 255, 0),
                                          (0, 255, 0), self.font_size))
            level_text.append(engine.Text(self.screen, "PRESS ANY KEY TO START", 8, 20, (255,255,255),
                                          None, self.font_size))
            level_text.append(engine.Text(self.screen, current_level, 2.5, 7, (255, 255, 0),
                                          None, self.font_size * 3))


            #set up static group of blocks
            self.static_blocks = pygame.sprite.Group()
            self.targets = pygame.sprite.Group()

            #set up the block group - user controlled
            self.user_blocks = pygame.sprite.Group()
            self.user_up_next = pygame.sprite.Group()
            self.create_up_next_blocks()
            self.create_user_blocks()

            while running:
                clock.tick(30)
                self.level_timer -= 1
                # print(self.level_timer)
                # Fill the background
                self.screen.fill((0, 0, 255))
                #test.text_draw()
                score_text = "SCORE: " + str(self.score)
                score.text = score_text
                score.text_draw()

                pygame.draw.rect(self.screen,(0,0,0),(self.block_width * 1.5,0, self.block_width * 5, self.screen_height))


                for text_show in level_text:
                    text_show.text_draw()
                    #print(text_show.text)

                # Did the user click the window close button?
                one_move = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #self.menu_button()
                        running = False
                        self.level_playing = "finish"
                        #self.level_playing = "level2"
                    if event.type == pygame.VIDEORESIZE:
                        #print(self.screen)
                        self.screen_resize()
                    if event.type == pygame.KEYDOWN and one_move is True:
                        one_move = False
                        if event.key == pygame.K_RIGHT and self.column < self.limit:
                            able_to_move = True
                            for r in self.user_blocks:
                                # check to see if any static sprites are to the right
                                for _2 in self.static_blocks:
                                    if _2.rect.top <= r.rect.bottom and _2.rect.top >= r.rect.top  and\
                                            r.rect.left + r.rect.width == _2.rect.left:
                                        able_to_move = False
                            if able_to_move is True:
                                self.column += 1
                                for r in self.user_blocks:
                                    r.x += r.rect.width
                        if event.key == pygame.K_LEFT and self.column > (self.limit * -1):
                            able_to_move = True
                            for r in self.user_blocks:
                                # check to see if any static sprites are to the left
                                for _2 in self.static_blocks:
                                    if _2.rect.top <= r.rect.bottom and _2.rect.top >= r.rect.top and \
                                            r.rect.left - r.rect.width == _2.rect.left:
                                        able_to_move = False
                            if able_to_move is True:
                                self.column -= 1
                                for r in self.user_blocks:
                                    r.x -= r.rect.width
                        if event.key == pygame.K_DOWN:
                            #decide which brick is the lowest in the pack
                            list_user_bricks = []
                            for r in self.user_blocks:
                                list_user_bricks.append(r.rect.top)
                            top_brick = max(list_user_bricks)
                            #print("list user bricks", list_user_bricks)
                            #print("Max", max(list_user_bricks))
                            #print("Count", len(list_user_bricks))
                            for r in self.user_blocks:
                                if r.rect.top == top_brick:
                                    r.y -= r.rect.height * (len(list_user_bricks)-1)
                                else:
                                    r.y += r.rect.height

                        if event.key == pygame.K_UP:
                            #decide which brick is the lowest in the pack
                            list_user_bricks = []
                            for r in self.user_blocks:
                                list_user_bricks.append(r.rect.top)
                            top_brick = min(list_user_bricks)
                            #print("list user bricks", list_user_bricks)
                            #print("Min", min(list_user_bricks))
                            #print("Count", len(list_user_bricks))
                            # Moving the bricks about
                            for r in self.user_blocks:
                                if r.rect.top == top_brick:
                                    r.y += r.rect.height * (len(list_user_bricks)-1)
                                else:
                                    r.y -= r.rect.height

                    if event.type == pygame.KEYUP:
                        one_move = True


                        #self.screen = pygame.transform.smoothscale(self.screen, (500, 500))
                        #pygame.draw.circle(self.screen, (255, 0, 0), (0, 0), 75)

                # Draw a solid blue circle in the center
                #pygame.draw.circle(self.screen, (255, 0, 0), (250, 250), 75)

                #self.my_ft_font.render_to(self.screen, (0, 0), "ABCDEFGHIJKLMNOPQRSTUVWXYZ12345678900End", (255, 0, 255))
                #self.my_ft_font.render_to(self.screen, (0, self.font_size), "abcdefghijklmnopqrstuvwxyz!£$%^&*()_+=-/\.,", (255, 0, 255))

                #for _ in range(1, self.text_rows + 1):
                #    self.screen_position(_, _)
                #    self.my_ft_font.render_to(self.screen, (self.x, self.y), str(_) + " Testing 123", (0, 0, 255))

                #Put this in a loop. So blocks can move faster, but collision detection done for each one
                #also need to add in movement of static blocks, these must also only move 1 at a time dy must not be bigger
                #add extra loop instead
                for speed in range(0,self.drop_speed):
                    #Check to see if the user block has stopped moving
                    user_block_moving = True

                    # loop through the 3 blocks
                    for _ in self.user_blocks:
                        _.hit_bottom_row()
                        # If they are not moving then they need to be converted to static
                        if _.dy == 0:
                            user_block_moving = False
                            #print(_)

                        # check to see if any static sprites will stop them
                        for _2 in self.static_blocks:
                            if _.rect.bottom >= _2.rect.top and _.rect.left == _2.rect.left:
                                #print("bot",_.rect.bottom, "delta" ,_.dy, "top",_2.rect.top)
                                user_block_moving = False
                                _.moving = False
                                # If the user blocks are at the top of the screen - that is game over..
                                if _.rect.top < self.block_height * 3:
                                    print("game - over")
                                    running = False
                                    self.level_playing = 'finish'
                                    break


                    # update will move and check it does not leave bottom of screen
                    if user_block_moving == True:
                        self.user_blocks.update()

                    # check if static should move
                    self.should_any_static_be_moving()
                    # Update the static blocks
                    self.static_blocks.update()


                    # This will trigger checking for matching, also need to check against
                    # Any blocks already there. New Sprite group will be needed for this
                    if user_block_moving == False:
                        for _ in self.user_blocks:
                            _.dy = 0
                        self.convert_user_to_static()
                        self.create_user_blocks()
                #time.sleep(.25)

                self.targets.update()
                self.user_up_next.update()
                #Draw all the blocks
                self.user_blocks.draw(self.screen)
                self.user_up_next.draw(self.screen)
                self.static_blocks.draw(self.screen)
                self.targets.draw(self.screen)
                pygame.display.flip()

                if self.first_loop == True:
                    # Putting a 'Press Any Key' wait thing here
                    pygame.display.flip()
                    waiting = engine.Wait_for_key_press()
                    test = waiting.update(self.screen)
                    print(test)
                    # added this so you can close the screen in the wait module (maybe better way)
                    if test == 'finish':
                        self.level_playing = 'finish'
                        running = False


                    self.first_loop = False
                    #Takes the last 2 text items added to the list to remove the text
                    level_text.pop(len(level_text)-1)
                    level_text.pop(len(level_text) - 1)
                    # Add the Title to the top
                    level_text.append(engine.Text(self.screen, "MATCH  3", 4, 1, (0, 255, 0),
                                                  None, self.font_size * 2))

                # Pause the game to show the blocks that match and then destroy them
                if self.show_matching == True:
                    if self.sound_setting == "on":
                        self.blocks_match_sound.play()
                    time.sleep(.2)
                    for _ in self.static_blocks:
                        if _.match == True:
                            _.kill()
                    self.show_matching = False

                # Has the level finished (counts down every loop)
                if self.level_timer == 0:
                    running = False
                    level += 1
                    next_level = "level" + str(level)
                    self.level_playing = next_level
                    level_text.append(engine.Text(self.screen, "LEVEL", 4, 7, (255, 0, 255),
                                                  None, self.font_size * 3))
                    level_text.append(engine.Text(self.screen, "COMPLETE", 2.5, 8, (255, 0, 255),
                                                  None, self.font_size * 3))
                    level_text.append(engine.Text(self.screen, "PRESS ANY KEY", 13, 20, (255, 0, 255),
                                                  None, self.font_size))
                    for text_show in level_text:
                        text_show.text_draw()
                    pygame.display.flip()
                    if self.sound_setting == "on":
                        self.finish_level_sound.play()
                    waiting = engine.Wait_for_key_press()
                    test = waiting.update(self.screen)
                    print(test, self.level_playing)
                    # added this so you can close the screen in the wait module (maybe better way)
                    if test == 'finish':
                        self.level_playing = 'finish'
                        running = False
            if self.level_playing == 'finish':
                # Game over man game over
                level_text.append(engine.Text(self.screen, "GAME", 3.25, 2, (255, 0, 255),
                                              (0,0,0), self.font_size * 3))
                level_text.append(engine.Text(self.screen, "OVER", 3.25, 3, (255, 0, 255),
                                              (0,0,0), self.font_size * 3))
                level_text.append(engine.Text(self.screen, "PRESS ANY KEY", 10, 20, (255, 0, 255),
                                              (0,0,0), self.font_size))
                for text_show in level_text:
                    text_show.text_draw()
                pygame.display.flip()
                if self.sound_setting == "on":
                    self.end_game_sound.play()
                waiting = engine.Wait_for_key_press()
                test = waiting.update(self.screen)
                self.level_playing = "menu"
                print(test)

        def create_user_blocks(self):
                self.column = 0
                # add 3
                ub1 = Block(self.player[0], self.player[1], self.nxt.colour, self.screen)
                ub2 = Block(self.player[0], self.player[1] + self.block_height, self.nxt2.colour, self.screen)
                ub3 = Block(self.player[0], self.player[1] + self.block_height + self.block_height,
                            self.nxt3.colour, self.screen)

                self.user_blocks.add(ub1, ub2, ub3)
                self.create_up_next_blocks()

        def create_up_next_blocks(self):
                #clear out any up next
                self.user_up_next.empty()
                self.nxt = Block(self.block_width * 8, self.block_height * 6, random.randint(0, 2), self.screen)
                self.nxt.dy = 0
                self.nxt2 = Block(self.block_width * 8, self.block_height * 7, random.randint(0, 2), self.screen)
                self.nxt2.dy = 0
                self.nxt3 = Block(self.block_width * 8, self.block_height * 8, random.randint(0, 2), self.screen)
                self.nxt3.dy = 0

                self.user_up_next.add(self.nxt, self.nxt2, self.nxt3)

        def convert_user_to_static(self):
            for convert in self.user_blocks:
                self.static_blocks.add(convert)
                #print("Top", convert.rect.top)
            self.user_blocks.empty()
            #print("user should be empty", self.user_blocks)

            self.match_3()

            # At this point need code to detect which ones to delete
            # also need to have them fall - not so easy with static ones..
            # Add a new group or enhance static to move if no other below..

        def should_any_static_be_moving(self):
            # _4 is the brick being tested
            # keep a record for next time
            self.blocks_were_moving = self.blocks_are_moving
            self.blocks_are_moving = False
            for _4 in self.static_blocks:
                #print("**************")
                #print("I am in this location top left", _4.rect.top, _4.rect.left, "my dy is ", _4.dy)
                #print("my height is", _4.rect.height)
                stopped = False
                for _5 in self.static_blocks:
                    #print("  compare against", _5.rect.top, _5.rect.left)
                    if _4.rect.bottom == _5.rect.top and _4.rect.left == _5.rect.left:
                    #if _4.rect.top + _4.rect.height == _5.rect.top:
                        #print("This bad boy stops me moving", _5.rect.top)
                        _4.dy = 0
                        _4.moving = False
                        stopped = True

                if stopped == False:
                    _4.dy = 1
                    _4.moving = True
                if _4.bottom_brick == True:
                    #print("But I am the bottom brick now")
                    _4.moving = False
                    _4.dy = 0
            for _ in self.static_blocks:
                if _.moving == True:
                    # At least one block is moving..
                    self.blocks_are_moving = True
                    break

            # Test to see if state of moving has changed
            #print("BLOCKS are and where moving: ", self.blocks_are_moving, self.blocks_were_moving)
            if self.blocks_were_moving == True and self.blocks_are_moving == False:
                # If all static blocks are not moving, need to check if any are matching
                self.match_3()


        def match_3(self):
            # create 3 targets to test for matches
            start_x = self.player[0] + (self.block_width / 2)
            start_y = self.player[1] + (self.block_height / 2)
            t1 = Target(start_x, start_y, self.screen)
            t2 = Target(start_x + self.block_width, start_y , self.screen)
            t3 = Target(start_x + self.block_width + self.block_width, start_y ,self.screen)

            #Makes sure all static blocks are static..
            # not sure this is needed
            for stop in self.static_blocks:
                stop.dy = 0
                stop.moving = False

            #self.targets.update()

            #targets need to move around the grid, and see which blocks are hit
            #work out where to start
            grid_left_x = int(self.player[0] - (self.limit * self.block_width) + (self.block_width / 2))
            grid_bottom_y = int(self.screen_height - (self.block_height / 2))
            #print("grid left", grid_left_x)
            #print("grid bottom",grid_bottom_y)
            # main loop running from bottom left to top right
            # target moved in each direction looking for a match of three static blocks the same colour
            for x in range(grid_left_x, grid_left_x + (self.block_width *  self.limit * 2) + self.block_width,self.block_width):
                for y in range(grid_bottom_y, 0, (-1 * self.block_height) ):

                    # Test for 3 matching horizontal blocks of the same colour
                    t1.x = x
                    t2.x = x + self.block_width
                    t3.x = x + self.block_width + self.block_width
                    t1.y = t2.y = t3.y = y
                    #print("t1 etc", t1.x, t1.y)
                    self.targets.add(t1, t2, t3)
                    self.targets.update()
                    #print("Targets are now", self.targets)
                    self.static_blocks.update()
                    #self.targets.draw(self.screen)
                    #pygame.display.flip()

                    test_for_3 = pygame.sprite.groupcollide(self.static_blocks, self.targets, False, False)
                    if len(test_for_3) == 3:
                       #("Bingo found 3!")
                        colours = []
                        for _ in test_for_3:
                            #print("And the colours are:.. ", _.colour)
                            colours.append(_.colour)
                        colour_set = set(colours)
                        if len(colour_set) == 1:
                            #print("ALL THE COLOURS ARE THE SAME")

                            # As the colours match mark them for destruction
                            for _ in test_for_3:
                                _.match = True
                                #_.kill()
                    self.targets.empty()

                    # Repeat
                    # Test for 3 matching vertical blocks of the same colour
                    t1.y = y
                    t2.y = y + self.block_height
                    t3.y = y + self.block_height + self.block_height
                    t1.x = t2.x = t3.x = x
                    # print("t1 etc", t1.x, t1.y)
                    self.targets.add(t1, t2, t3)
                    self.targets.update()
                    # print("Targets are now", self.targets)
                    self.static_blocks.update()
                    # self.targets.draw(self.screen)
                    # pygame.display.flip()

                    test_for_3 = pygame.sprite.groupcollide(self.static_blocks, self.targets, False, False)
                    if len(test_for_3) == 3:
                        #print("Bingo found 3!")
                        colours = []
                        for _ in test_for_3:
                            #print("And the colours are:.. ", _.colour)
                            colours.append(_.colour)
                        colour_set = set(colours)
                        if len(colour_set) == 1:
                            #print("ALL THE COLOURS ARE THE SAME")
                            # As the colours match mark them for destruction
                            for _ in test_for_3:
                                _.match = True
                                # _.kill()
                    self.targets.empty()

                    #Repeat for diagonal this way ///
                    # Test for 3 matching horizontal blocks of the same colour
                    t1.x = x
                    t2.x = x + self.block_width
                    t3.x = x + self.block_width + self.block_width
                    t1.y = y
                    t2.y = y - self.block_height
                    t3.y = y - self.block_height - self.block_height
                    # print("t1 etc", t1.x, t1.y)
                    self.targets.add(t1, t2, t3)
                    self.targets.update()
                    # print("Targets are now", self.targets)
                    self.static_blocks.update()
                    #self.targets.draw(self.screen)
                    #pygame.display.flip()

                    test_for_3 = pygame.sprite.groupcollide(self.static_blocks, self.targets, False, False)
                    if len(test_for_3) == 3:
                        #print("Bingo found 3!")
                        colours = []
                        for _ in test_for_3:
                            #print("And the colours are diag:.. ", _.colour)
                            colours.append(_.colour)
                        colour_set = set(colours)
                        if len(colour_set) == 1:
                            #print("ALL THE COLOURS ARE THE SAME")
                            # As the colours match mark them for destruction
                            for _ in test_for_3:
                                _.match = True
                                # _.kill()
                    self.targets.empty()

                    #Repeat for diagonal this way \\\
                    # Test for 3 matching horizontal blocks of the same colour
                    t1.x = x
                    t2.x = x - self.block_width
                    t3.x = x - self.block_width - self.block_width
                    t1.y = y
                    t2.y = y - self.block_height
                    t3.y = y - self.block_height - self.block_height
                    # print("t1 etc", t1.x, t1.y)
                    self.targets.add(t1, t2, t3)
                    self.targets.update()
                    # print("Targets are now", self.targets)
                    self.static_blocks.update()
                    #self.targets.draw(self.screen)
                    #pygame.display.flip()

                    test_for_3 = pygame.sprite.groupcollide(self.static_blocks, self.targets, False, False)
                    if len(test_for_3) == 3:
                        #print("Bingo found 3!")
                        colours = []
                        for _ in test_for_3:
                            #print("And the colours are diag:.. ", _.colour)
                            colours.append(_.colour)
                        colour_set = set(colours)
                        if len(colour_set) == 1:
                            #print("ALL THE COLOURS ARE THE SAME")
                            # As the colours match mark them for destruction
                            for _ in test_for_3:
                                _.match = True
                                # _.kill()
                    self.targets.empty()
            bonus = 0
            for _ in self.static_blocks:
                if _.match == True:
                    self.score += 1
                    _.colour = 3
                    _.update_colour()
                    bonus += 1
                    # Need to pause the main loop and then destroy them
                    self.show_matching = True
            if self.show_matching == True:
                # Add bonus if you match more that 3
                bonus_multiplier = int(bonus / 3)
                #print("Bonus", bonus, "Mult", bonus_multiplier)
                #print("Bonus Mult", bonus_multiplier)
                #print("Bonus2", bonus % 3)
                self.score += (bonus * bonus_multiplier) + bonus % 3








if __name__ == '__main__':
    pygame.init()
    match3 = Game()
    donePlaying = False
    match3.level_playing = "menu"
    while not donePlaying:
        # open main menu
        print("level_playing1" , match3.level_playing)
        if match3.level_playing == "menu":
            match3.menu()
        # open level to play
        print("level_playing2", match3.level_playing)
        print(match3.level_playing[:5])
        if match3.level_playing[:5] == "level":
            level_num = int(match3.level_playing[5:])
            match3.level(level_num)
        print("level_playing3", match3.level_playing)
        if match3.level_playing == "finish":
            donePlaying = True

    # Done! Time to quit.
    pygame.quit()

# Done! Time to quit.
pygame.quit()