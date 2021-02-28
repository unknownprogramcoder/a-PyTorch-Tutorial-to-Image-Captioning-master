import torch
import pygame
import random
import cv2
from caption import network_init, image_captioning
from modify_music import volume_modify, color_modify
from modify_music import interpret_words

#출처: https://kkamikoon.tistory.com/135 [컴퓨터를 다루다]

def response(Bool):
    if Bool:
        return 1
    elif not Bool:
        return 0

def playsound():

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(128)
    WIDTH = 800
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Art Bus 13 : Gathering Music Fractures using Images ")
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))

    caption_sentence = "Caption of the Image Here"
    font = pygame.font.SysFont("arial", 32, True, False)
    text_Title = font.render(caption_sentence, True, (0, 0, 0))
    text_Rect = text_Title.get_rect()
    text_Rect.centerx = round(WIDTH / 2)
    text_Rect.centery = round(HEIGHT / 4)
    screen.blit(text_Title, text_Rect)

    pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT / 2], [WIDTH, HEIGHT / 2], 16)
    pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT * 5 / 8], [WIDTH, HEIGHT * 5 / 8], 16)

    font_quit = pygame.font.SysFont("Corbel", 36, True, False)
    text_Title_quit = font_quit.render("Esc to Quit", True, (0, 0, 0))
    text_Rect_quit = text_Title_quit.get_rect()
    text_Rect_quit.centerx = round(WIDTH * 7 / 8)
    text_Rect_quit.centery = round(HEIGHT * 15 / 16)
    screen.blit(text_Title_quit, text_Rect_quit)

    font_film = pygame.font.SysFont("Corbel", 36, True, False)
    text_Title_film = font_film.render("or press Spacebar", True, (0, 0, 0))
    text_Rect_film = text_Title_film.get_rect()
    text_Rect_film.centerx = round(WIDTH / 4)
    text_Rect_film.centery = round(HEIGHT * 7 / 8)
    screen.blit(text_Title_film, text_Rect_film)

    font_button = pygame.font.SysFont('Corbel', 48, True, False)
    text_button = font_button.render('Take-Picture', True, (255, 255, 255))
    text_Rect_button = text_button.get_rect()
    text_Rect_button.centerx = round(WIDTH / 4)
    text_Rect_button.centery = round(HEIGHT * 3 / 4)
    mouse = pygame.mouse.get_pos()
    if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and \
            text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
        pygame.draw.rect(screen, (127, 127, 127), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
    else:
        pygame.draw.rect(screen, (63, 63, 63), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
    screen.blit(text_button, text_Rect_button)


    pygame.display.flip()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    encoder, decoder, word_map, rev_word_map = network_init(device)
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fractures_top = []
    fractures_chord = []
    fractures_bass = []
    fractures_agrement = []
    fractures_pad = []
    fractures_percussion = []
    fractures_top.append(pygame.mixer.Sound('fractures/top ww frac1.wav'))
    fractures_top.append(pygame.mixer.Sound('fractures/top ww frac2.wav'))
    fractures_top.append(pygame.mixer.Sound('fractures/top ww frac3.wav'))
    fractures_top.append(pygame.mixer.Sound('fractures/top bell frac1.wav'))
    fractures_top.append(pygame.mixer.Sound('fractures/top bell frac2.wav'))
    fractures_top.append(pygame.mixer.Sound('fractures/top bell frac3.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord harp frac1.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord harp frac2.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord harp frac3.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord epiano frac1.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord epiano frac2.wav'))
    fractures_chord.append(pygame.mixer.Sound('fractures/chord epiano frac3.wav'))

    vol_top = [0, 1, 0]
    vol_chord = [0, 0, 1]
    vol_bass = [0, 0, 0]
    vol_agrement = [0]
    vol_pad = [0]
    vol_percussion = [0,0,0]
    col_top = [1,0]
    col_chord = [1,0]
    col_bass = [1,0,0]
    col_agrement = [1,0,0]
    col_pad = [1,0,0]
    col_percussion = [1,0,0]

    Running = True
    doAddFrac = 0
    existingFrac = 0
    doChangeInst = 0

    while Running:
        for f in fractures_top:
            f.play(0)
        for f in fractures_chord:
            f.play(0)
        '''
        for f in fractures_bass:
            f.play(0)
        for f in fractures_agrement:
            f.play(0)
        for f in fractures_pad:
            f.play(0)
        for f in fractures_percussion:
            f.play(0)
        '''
        for c in range(len(col_top)):
            if col_top[c] == 0:
                for f in range(len(vol_top)):
                    fractures_top[f + len(vol_top) * c].set_volume(0)
            elif col_top[c] == 1:
                for f in range(len(vol_top)):
                    fractures_top[f + len(vol_top) * c].set_volume(vol_top[f])
        for c in range(len(col_chord)):
            if col_chord[c] == 0:
                for f in range(len(vol_chord)):
                    fractures_chord[f + len(vol_chord) * c].set_volume(0)
            elif col_chord[c] == 1:
                for f in range(len(vol_chord)):
                    fractures_chord[f + len(vol_chord) * c].set_volume(vol_chord[f])
        '''
        for c in range(len(col_bass)):
            if col_bass[c] == 0:
                for f in range(len(vol_bass)):
                    fractures_bass[f + len(vol_bass) * c].set_volume(0)
            elif col_bass[c] == 1:
                for f in range(len(vol_bass)):
                    fractures_bass[f + len(vol_bass) * c].set_volume(vol_bass[f])
        for c in range(len(col_agrement)):
            if col_agrement[c] == 0:
                for f in range(len(vol_agrement)):
                    fractures_agrement[f + len(vol_agrement) * c].set_volume(0)
            elif col_agrement[c] == 1:
                for f in range(len(vol_agrement)):
                    fractures_agrement[f + len(vol_agrement) * c].set_volume(vol_agrement[f])
        for c in range(len(col_pad)):
            if col_pad[c] == 0:
                for f in range(len(vol_pad)):
                    fractures_pad[f + len(vol_pad) * c].set_volume(0)
            elif col_pad[c] == 1:
                for f in range(len(vol_pad)):
                    fractures_pad[f + len(vol_pad) * c].set_volume(vol_pad[f])
        for c in range(len(col_percussion)):
            if col_percussion[c] == 0:
                for f in range(len(vol_percussion)):
                    fractures_percussion[f + len(vol_percussion) * c].set_volume(0)
            elif col_percussion[c] == 1:
                for f in range(len(vol_percussion)):
                    fractures_percussion[f + len(vol_percussion) * c].set_volume(vol_percussion[f])
        '''
        screen.fill((255, 255, 255))

        font = pygame.font.SysFont("arial", 32, True, False)
        text_Title = font.render(caption_sentence, True, (0, 0, 0))
        text_Rect = text_Title.get_rect()
        text_Rect.centerx = round(WIDTH / 2)
        text_Rect.centery = round(HEIGHT / 4)
        screen.blit(text_Title, text_Rect)

        pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT / 2], [WIDTH, HEIGHT / 2], 16)
        pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT * 5 / 8], [WIDTH, HEIGHT * 5 / 8], 16)

        font_quit = pygame.font.SysFont("Corbel", 36, True, False)
        text_Title_quit = font_quit.render("Esc to Quit", True, (0, 0, 0))
        text_Rect_quit = text_Title_quit.get_rect()
        text_Rect_quit.centerx = round(WIDTH * 7 / 8)
        text_Rect_quit.centery = round(HEIGHT * 15 / 16)
        screen.blit(text_Title_quit, text_Rect_quit)

        font_film = pygame.font.SysFont("Corbel", 36, True, False)
        text_Title_film = font_film.render("or press Spacebar", True, (0, 0, 0))
        text_Rect_film = text_Title_film.get_rect()
        text_Rect_film.centerx = round(WIDTH / 4)
        text_Rect_film.centery = round(HEIGHT * 7 / 8)
        screen.blit(text_Title_film, text_Rect_film)

        font_button = pygame.font.SysFont('Corbel', 48, True, False)
        text_button = font_button.render('Take-Picture', True, (255, 255, 255))
        text_Rect_button = text_button.get_rect()
        text_Rect_button.centerx = round(WIDTH / 4)
        text_Rect_button.centery = round(HEIGHT * 3 / 4)
        mouse = pygame.mouse.get_pos()
        if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and text_Rect_button.topleft[1] <= \
                mouse[1] <= text_Rect_button.bottomright[1]:
            pygame.draw.rect(screen, (127, 127, 127), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                       text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                       text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
        else:
            pygame.draw.rect(screen, (63, 63, 63), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                    text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                    text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
        screen.blit(text_button, text_Rect_button)

        if doAddFrac > 0:
            font1 = pygame.font.SysFont("malgungothic", 36, True, False)
            text_Title1 = font1.render("음악 조각 추가!", True, (0, 0, 255))
            text_Rect1 = text_Title1.get_rect()
            text_Rect1.centerx = round(WIDTH / 4)
            text_Rect1.centery = round(HEIGHT * 9 / 16)
            screen.blit(text_Title1, text_Rect1)
        if existingFrac > 0:
            font2 = pygame.font.SysFont("malgungothic", 36, True, False)
            text_Title2 = font2.render("이미 연주 중..", True, (255, 0, 0))
            text_Rect2 = text_Title2.get_rect()
            text_Rect2.centerx = round(WIDTH / 2)
            text_Rect2.centery = round(HEIGHT * 9 / 16)
            screen.blit(text_Title2, text_Rect2)
        if doChangeInst > 0:
            font3 = pygame.font.SysFont("malgungothic", 36, True, False)
            text_Title3 = font3.render("악기 재설정!", True, (255, 0, 255))
            text_Rect3 = text_Title3.get_rect()
            text_Rect3.centerx = round(WIDTH * 3 / 4)
            text_Rect3.centery = round(HEIGHT * 9 / 16)
            screen.blit(text_Title3, text_Rect3)
        pygame.display.flip()

        ret, frame = capture.read()
        flipped = cv2.flip(frame, 1)
        cv2.imshow("VideoFrame", flipped)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and \
                        text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
                    # str = Network.forward(image)

                    # change volume setting
                    # interpret_words(text_slice(str[random.randint(0, 1)]))
                    caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                    doAddFrac, existingFrac, doChangeInst = interpret_words(caption_words)
                    caption_sentence = ""
                    for i in range(len(caption_words) - 1):
                        caption_sentence += caption_words[i + 1]
                        caption_sentence += " "
                    print(caption_sentence)
                    # divide volume settings into different score parts
                    vol_top = volume_modify[0:3]
                    vol_chord = volume_modify[3:6]
                    vol_bass = volume_modify[6:9]
                    vol_agrement = volume_modify[9]
                    vol_pad = volume_modify[10]
                    vol_percussion = volume_modify[11:14]
                    col_top = [response(color_modify[0] == 0), response(color_modify[0] == 1)]
                    col_chord = [response(color_modify[1] == 0), response(color_modify[1] == 1)]
                    col_bass = [response(color_modify[2] == 0), response(color_modify[2] == 1),
                                response(color_modify[2] == 2)]
                    col_agrement = [response(color_modify[3] == 0), response(color_modify[3] == 1),
                                    response(color_modify[3] == 2)]
                    col_pad = [response(color_modify[4] == 0), response(color_modify[4] == 1),
                               response(color_modify[4] == 2)]
                    col_percussion = [response(color_modify[5] == 0), response(color_modify[5] == 1),
                                      response(color_modify[5] == 2)]
                    # actually change volume
                    for c in range(len(col_top)):
                        if col_top[c] == 0:
                            for f in range(len(vol_top)):
                                fractures_top[f + len(vol_top) * c].set_volume(0)
                        elif col_top[c] == 1:
                            for f in range(len(vol_top)):
                                fractures_top[f + len(vol_top) * c].set_volume(vol_top[f])
                    for c in range(len(col_chord)):
                        if col_chord[c] == 0:
                            for f in range(len(vol_chord)):
                                fractures_chord[f + len(vol_chord) * c].set_volume(0)
                        elif col_chord[c] == 1:
                            for f in range(len(vol_chord)):
                                fractures_chord[f + len(vol_chord) * c].set_volume(vol_chord[f])
                    '''
                    for c in range(len(col_bass)):
                        if col_bass[c] == 0:
                            for f in range(len(vol_bass)):
                                fractures_bass[f + len(vol_bass) * c].set_volume(0)
                        elif col_bass[c] == 1:
                            for f in range(len(vol_bass)):
                                fractures_bass[f + len(vol_bass) * c].set_volume(vol_bass[f])
                    for c in range(len(col_agrement)):
                        if col_agrement[c] == 0:
                            for f in range(len(vol_agrement)):
                                fractures_agrement[f + len(vol_agrement) * c].set_volume(0)
                        elif col_agrement[c] == 1:
                            for f in range(len(vol_agrement)):
                                fractures_agrement[f + len(vol_agrement) * c].set_volume(vol_agrement[f])
                    for c in range(len(col_pad)):
                        if col_pad[c] == 0:
                            for f in range(len(vol_pad)):
                                fractures_pad[f + len(vol_pad) * c].set_volume(0)
                        elif col_pad[c] == 1:
                            for f in range(len(vol_pad)):
                                fractures_pad[f + len(vol_pad) * c].set_volume(vol_pad[f])
                    for c in range(len(col_percussion)):
                        if col_percussion[c] == 0:
                            for f in range(len(vol_percussion)):
                                fractures_percussion[f + len(vol_percussion) * c].set_volume(0)
                        elif col_percussion[c] == 1:
                            for f in range(len(vol_percussion)):
                                fractures_percussion[f + len(vol_percussion) * c].set_volume(vol_percussion[f])
                    '''
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Running = False
                if event.key == pygame.K_SPACE:
                    # str = Network.forward(image)

                    # change volume setting
                    #interpret_words(text_slice(str[random.randint(0, 1)]))
                    caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                    doAddFrac, existingFrac, doChangeInst = interpret_words(caption_words)
                    caption_sentence = ""
                    for i in range(len(caption_words) - 1):
                        caption_sentence += caption_words[i + 1]
                        caption_sentence += " "
                    print(caption_sentence)
                    # divide volume settings into different score parts
                    vol_top = volume_modify[0:3]
                    vol_chord = volume_modify[3:6]
                    vol_bass = volume_modify[6:9]
                    vol_agrement = volume_modify[9]
                    vol_pad = volume_modify[10]
                    vol_percussion = volume_modify[11:14]
                    col_top = [response(color_modify[0] == 0), response(color_modify[0] == 1)]
                    col_chord = [response(color_modify[1] == 0), response(color_modify[1] == 1)]
                    col_bass = [response(color_modify[2] == 0), response(color_modify[2] == 1),
                                response(color_modify[2] == 2)]
                    col_agrement = [response(color_modify[3] == 0), response(color_modify[3] == 1),
                                    response(color_modify[3] == 2)]
                    col_pad = [response(color_modify[4] == 0), response(color_modify[4] == 1),
                               response(color_modify[4] == 2)]
                    col_percussion = [response(color_modify[5] == 0), response(color_modify[5] == 1),
                                      response(color_modify[5] == 2)]

        if doAddFrac > 0:
            doAddFrac -= 1
        if existingFrac > 0:
            existingFrac -= 1
        if doChangeInst > 0:
            doChangeInst -= 1

        # 재생 루프
        while Running and pygame.mixer.get_busy():
            screen.fill((255, 255, 255))

            font = pygame.font.SysFont("arial", 32, True, False)
            text_Title = font.render(caption_sentence, True, (0, 0, 0))
            text_Rect = text_Title.get_rect()
            text_Rect.centerx = round(WIDTH / 2)
            text_Rect.centery = round(HEIGHT / 4)
            screen.blit(text_Title, text_Rect)

            pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT / 2], [WIDTH, HEIGHT / 2], 16)
            pygame.draw.line(screen, (191, 127, 127), [0, HEIGHT * 5 / 8], [WIDTH, HEIGHT * 5 / 8], 16)

            font_quit = pygame.font.SysFont("Corbel", 36, True, False)
            text_Title_quit = font_quit.render("Esc to Quit", True, (0, 0, 0))
            text_Rect_quit = text_Title_quit.get_rect()
            text_Rect_quit.centerx = round(WIDTH * 7 / 8)
            text_Rect_quit.centery = round(HEIGHT * 15 / 16)
            screen.blit(text_Title_quit, text_Rect_quit)

            font_film = pygame.font.SysFont("Corbel", 36, True, False)
            text_Title_film = font_film.render("or press Spacebar", True, (0, 0, 0))
            text_Rect_film = text_Title_film.get_rect()
            text_Rect_film.centerx = round(WIDTH / 4)
            text_Rect_film.centery = round(HEIGHT * 7 / 8)
            screen.blit(text_Title_film, text_Rect_film)

            font_button = pygame.font.SysFont('Corbel', 48, True, False)
            text_button = font_button.render('Take-Picture', True, (255, 255, 255))
            text_Rect_button = text_button.get_rect()
            text_Rect_button.centerx = round(WIDTH / 4)
            text_Rect_button.centery = round(HEIGHT * 3 / 4)
            mouse = pygame.mouse.get_pos()
            if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and text_Rect_button.topleft[
                1] <= mouse[1] <= text_Rect_button.bottomright[1]:
                pygame.draw.rect(screen, (127, 127, 127), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                           text_Rect_button.bottomright[0] - text_Rect_button.topleft[
                                                               0],
                                                           text_Rect_button.bottomright[1] - text_Rect_button.topleft[
                                                               1]])
            else:
                pygame.draw.rect(screen, (63, 63, 63), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                        text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                        text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
            screen.blit(text_button, text_Rect_button)

            if doAddFrac > 0:
                font1 = pygame.font.SysFont("malgungothic", 36, True, False)
                text_Title1 = font1.render("음악 조각 추가!", True, (0, 0, 255))
                text_Rect1 = text_Title1.get_rect()
                text_Rect1.centerx = round(WIDTH / 4)
                text_Rect1.centery = round(HEIGHT * 9 / 16)
                screen.blit(text_Title1, text_Rect1)
            if existingFrac > 0:
                font2 = pygame.font.SysFont("malgungothic", 36, True, False)
                text_Title2 = font2.render("이미 연주 중..", True, (255, 0, 0))
                text_Rect2 = text_Title2.get_rect()
                text_Rect2.centerx = round(WIDTH / 2)
                text_Rect2.centery = round(HEIGHT * 9 / 16)
                screen.blit(text_Title2, text_Rect2)
            if doChangeInst > 0:
                font3 = pygame.font.SysFont("malgungothic", 36, True, False)
                text_Title3 = font3.render("악기 재설정!", True, (255, 0, 255))
                text_Rect3 = text_Title3.get_rect()
                text_Rect3.centerx = round(WIDTH * 3 / 4)
                text_Rect3.centery = round(HEIGHT * 9 / 16)
                screen.blit(text_Title3, text_Rect3)
            pygame.display.flip()

            ret, frame = capture.read()
            flipped = cv2.flip(frame, 1)
            cv2.imshow("VideoFrame", flipped)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
                        # str = Network.forward(image)

                        # change volume setting
                        # interpret_words(text_slice(str[random.randint(0, 1)]))
                        caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                        doAddFrac, existingFrac, doChangeInst = interpret_words(caption_words)
                        caption_sentence = ""
                        for i in range(len(caption_words) - 1):
                            caption_sentence += caption_words[i + 1]
                            caption_sentence += " "
                        print(caption_sentence)
                        # divide volume settings into different score parts
                        vol_top = volume_modify[0:3]
                        vol_chord = volume_modify[3:6]
                        vol_bass = volume_modify[6:9]
                        vol_agrement = volume_modify[9]
                        vol_pad = volume_modify[10]
                        vol_percussion = volume_modify[11:14]
                        col_top = [response(color_modify[0] == 0), response(color_modify[0] == 1)]
                        col_chord = [response(color_modify[1] == 0), response(color_modify[1] == 1)]
                        col_bass = [response(color_modify[2] == 0), response(color_modify[2] == 1),
                                    response(color_modify[2] == 2)]
                        col_agrement = [response(color_modify[3] == 0), response(color_modify[3] == 1),
                                        response(color_modify[3] == 2)]
                        col_pad = [response(color_modify[4] == 0), response(color_modify[4] == 1),
                                   response(color_modify[4] == 2)]
                        col_percussion = [response(color_modify[5] == 0), response(color_modify[5] == 1),
                                          response(color_modify[5] == 2)]
                        # actually change volume
                        for c in range(len(col_top)):
                            if col_top[c] == 0:
                                for f in range(len(vol_top)):
                                    fractures_top[f + len(vol_top) * c].set_volume(0)
                            elif col_top[c] == 1:
                                for f in range(len(vol_top)):
                                    fractures_top[f + len(vol_top) * c].set_volume(vol_top[f])
                        for c in range(len(col_chord)):
                            if col_chord[c] == 0:
                                for f in range(len(vol_chord)):
                                    fractures_chord[f + len(vol_chord) * c].set_volume(0)
                            elif col_chord[c] == 1:
                                for f in range(len(vol_chord)):
                                    fractures_chord[f + len(vol_chord) * c].set_volume(vol_chord[f])
                        '''
                        for c in range(len(col_bass)):
                            if col_bass[c] == 0:
                                for f in range(len(vol_bass)):
                                    fractures_bass[f + len(vol_bass) * c].set_volume(0)
                            elif col_bass[c] == 1:
                                for f in range(len(vol_bass)):
                                    fractures_bass[f + len(vol_bass) * c].set_volume(vol_bass[f])
                        for c in range(len(col_agrement)):
                            if col_agrement[c] == 0:
                                for f in range(len(vol_agrement)):
                                    fractures_agrement[f + len(vol_agrement) * c].set_volume(0)
                            elif col_agrement[c] == 1:
                                for f in range(len(vol_agrement)):
                                    fractures_agrement[f + len(vol_agrement) * c].set_volume(vol_agrement[f])
                        for c in range(len(col_pad)):
                            if col_pad[c] == 0:
                                for f in range(len(vol_pad)):
                                    fractures_pad[f + len(vol_pad) * c].set_volume(0)
                            elif col_pad[c] == 1:
                                for f in range(len(vol_pad)):
                                    fractures_pad[f + len(vol_pad) * c].set_volume(vol_pad[f])
                        for c in range(len(col_percussion)):
                            if col_percussion[c] == 0:
                                for f in range(len(vol_percussion)):
                                    fractures_percussion[f + len(vol_percussion) * c].set_volume(0)
                            elif col_percussion[c] == 1:
                                for f in range(len(vol_percussion)):
                                    fractures_percussion[f + len(vol_percussion) * c].set_volume(vol_percussion[f])
                        '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Running = False
                    if event.key == pygame.K_SPACE:
                        #str = Network.forward(image)

                        #change volume setting
                        #interpret_words(text_slice(str[random.randint(0, 1)]))
                        caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                        doAddFrac, existingFrac, doChangeInst = interpret_words(caption_words)
                        caption_sentence = ""
                        for i in range(len(caption_words) - 1):
                            caption_sentence += caption_words[i+1]
                            caption_sentence += " "
                        print(caption_sentence)
                        #divide volume settings into different score parts
                        vol_top = volume_modify[0:3]
                        vol_chord = volume_modify[3:6]
                        vol_bass = volume_modify[6:9]
                        vol_agrement = volume_modify[9]
                        vol_pad = volume_modify[10]
                        vol_percussion = volume_modify[11:14]
                        col_top = [response(color_modify[0]==0), response(color_modify[0]==1)]
                        col_chord = [response(color_modify[1]==0), response(color_modify[1]==1)]
                        col_bass = [response(color_modify[2]==0), response(color_modify[2]==1), response(color_modify[2]==2)]
                        col_agrement = [response(color_modify[3]==0), response(color_modify[3]==1), response(color_modify[3]==2)]
                        col_pad = [response(color_modify[4]==0), response(color_modify[4]==1), response(color_modify[4]==2)]
                        col_percussion = [response(color_modify[5]==0), response(color_modify[5]==1), response(color_modify[5]==2)]
                        #actually change volume
                        for c in range(len(col_top)):
                            if col_top[c] == 0:
                                for f in range(len(vol_top)):
                                    fractures_top[f + len(vol_top) * c].set_volume(0)
                            elif col_top[c] == 1:
                                for f in range(len(vol_top)):
                                    fractures_top[f + len(vol_top) * c].set_volume(vol_top[f])
                        for c in range(len(col_chord)):
                            if col_chord[c] == 0:
                                for f in range(len(vol_chord)):
                                    fractures_chord[f + len(vol_chord) * c].set_volume(0)
                            elif col_chord[c] == 1:
                                for f in range(len(vol_chord)):
                                    fractures_chord[f + len(vol_chord) * c].set_volume(vol_chord[f])
                        '''
                        for c in range(len(col_bass)):
                            if col_bass[c] == 0:
                                for f in range(len(vol_bass)):
                                    fractures_bass[f + len(vol_bass) * c].set_volume(0)
                            elif col_bass[c] == 1:
                                for f in range(len(vol_bass)):
                                    fractures_bass[f + len(vol_bass) * c].set_volume(vol_bass[f])
                        for c in range(len(col_agrement)):
                            if col_agrement[c] == 0:
                                for f in range(len(vol_agrement)):
                                    fractures_agrement[f + len(vol_agrement) * c].set_volume(0)
                            elif col_agrement[c] == 1:
                                for f in range(len(vol_agrement)):
                                    fractures_agrement[f + len(vol_agrement) * c].set_volume(vol_agrement[f])
                        for c in range(len(col_pad)):
                            if col_pad[c] == 0:
                                for f in range(len(vol_pad)):
                                    fractures_pad[f + len(vol_pad) * c].set_volume(0)
                            elif col_pad[c] == 1:
                                for f in range(len(vol_pad)):
                                    fractures_pad[f + len(vol_pad) * c].set_volume(vol_pad[f])
                        for c in range(len(col_percussion)):
                            if col_percussion[c] == 0:
                                for f in range(len(vol_percussion)):
                                    fractures_percussion[f + len(vol_percussion) * c].set_volume(0)
                            elif col_percussion[c] == 1:
                                for f in range(len(vol_percussion)):
                                    fractures_percussion[f + len(vol_percussion) * c].set_volume(vol_percussion[f])
                        '''
            if doAddFrac > 0:
                doAddFrac -= 1
            if existingFrac > 0:
                existingFrac -= 1
            if doChangeInst > 0:
                doChangeInst -= 1
            clock.tick(1000)
    stopmusic()
    capture.release()
    cv2.destroyAllWindows()

def stopmusic():
    pygame.mixer.music.stop()
    pygame.quit()
def getmixerargs():
    pygame.mixer.init()
    freq, size, chan = pygame.mixer.get_init()
    return freq, size, chan
def initMixer():
    BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
    FREQ, SIZE, CHAN = getmixerargs()
    pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)

try:
    initMixer()
    playsound()
except KeyboardInterrupt:  # to stop playing, press "ctrl-c"
    stopmusic()
print("Done")
