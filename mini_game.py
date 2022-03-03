import pygame
import os

pygame.init() #un-checked-python> linting: Enable from Setting

#setting screen size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

#screen title 
pygame.display.set_caption("Mini Game")

#FPS
clock = pygame.time.Clock()

#background
current_path = os.path.dirname(__file__) #current file location
image_path = os.path.join(current_path, "images") #image location

background = pygame.image.load(os.path.join(image_path, "background.png"))

#stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] #put character on the stage

#character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size #image size
character_width = character_size[0] #size of width
character_height = character_size[1] #size of height
character_x_pos = screen_width / 2 - (character_width / 2) #half size of width position
character_y_pos = screen_height - character_height - stage_height 

character_to_x = 0

character_speed = 5


#weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size #image size
weapon_width = weapon_size[0] #size of width

weapons = []

weapon_speed = 10

#ball (4 sizes)
ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]

#ball speed
ball_speed_y = [-18, -15, -12, -19] #index 0,1,2,3

#balls
balls = []

balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0, #ball's image index
    "to_x": 3, #direction of movement -> -: left +:right
    "to_y": -6,
    "init_spd_y": ball_speed_y[0] #initial speed of y
})

weapon_to_remove = -1
ball_to_remove = -1

#font
game_font = pygame.font.Font(None, 40)
total_time = 40
start_ticks = pygame.time.get_ticks() #start time

game_result = "GAME OVER"

running = True 
while running:
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if close
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #move to left
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: #move to right
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: #use weapon 
                weapon_x_pos = character_x_pos + (character_width/2) - (weapon_width/2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos =  screen_width - character_width

    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] #

    weapons = [[w[0], w[1]] for w in weapons if w[1]>0]

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]


        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1


        if ball_pos_y >= screen_height - stage_height - ball_height: 
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    #collision
    charact_rect = character.get_rect()
    charact_rect.left = character_x_pos
    charact_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]


        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y


        if charact_rect.colliderect(ball_rect):
            running = False
            break

        #ball and weapon's collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #update weapons's rect info
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx 
                ball_to_remove = ball_idx

        
                if ball_img_idx <3 :
                    
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #divided balls' info
                    small_ball_rect = ball_images[ball_img_idx +1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #bounce to left 
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y +(ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1, #ball's image index
                        "to_x": -3, #direction of movement -> -: left +:right
                        "to_y": -6,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1] #initial speed of y
                    })
                    #bounce to right
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y +(ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1, #ball's image index
                        "to_x": 3, #direction of movement -> -: left +:right
                        "to_y": -6,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1] #initial speed of y
                    })
                break


    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    if len(balls) == 0:
        game_result = "MISSION COMPLETE"
        running = False


    screen.blit(background,(0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage,(0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    #time left
    elapsed_time = (pygame.time.get_ticks() - start_ticks) /1000
    timer = game_font.render("Time: {}".format(int(total_time-elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10, 10))

    if total_time - elapsed_time <= 0:
        game_result = "TIME OVER"
        running = False

    pygame.display.update()

msg = game_font.render(game_result, True, (255,255,0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)
#end game
pygame.quit()