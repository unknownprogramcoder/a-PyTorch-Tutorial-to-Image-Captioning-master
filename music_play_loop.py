import torch
import pygame
import cv2
import numpy
from caption import network_init, image_captioning
from modify_music import volume_modify, color_modify
from modify_music import interpret_words

def get_camera(screen, capture):
    _, frame = capture.read()
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    flipped = cv2.flip(frame1, 1)
    flipped = numpy.rot90(flipped)
    flipped = pygame.surfarray.make_surface(flipped)
    screen.blit(flipped, (0, 0))
    return frame

def response(Bool):
    if Bool:
        return 1
    elif not Bool:
        return 0

def draw_screen(screen, WIDTH, HEIGHT, caption_sentence, doAddFrac, existingFrac, doChangeInst, InstUnchanged):
    pygame.draw.line(screen, (191, 191, 191), [0, 0], [WIDTH, 0], 96)

    font = pygame.font.SysFont("arial", 32, True, False)
    text_Title = font.render(caption_sentence, True, (0, 0, 0))
    text_Rect = text_Title.get_rect()
    text_Rect.centerx = round(WIDTH / 2)
    text_Rect.centery = round(18)
    screen.blit(text_Title, text_Rect)

    pygame.draw.line(screen, (63, 63, 63), [0, 720], [WIDTH, 720], 8)

    font_button = pygame.font.SysFont('malgungothic', 48, True, False)
    text_button = font_button.render('사진 촬영 버튼', True, (255, 255, 255))
    text_Rect_button = text_button.get_rect()
    text_Rect_button.centerx = round(WIDTH / 2)
    text_Rect_button.centery = round(HEIGHT - 50)
    mouse = pygame.mouse.get_pos()
    if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and \
            text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
        pygame.draw.rect(screen, (127, 127, 127), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                   text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                   text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
        '''
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (255, 255, 127), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                       text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                       text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
        '''
    else:
        pygame.draw.rect(screen, (32, 32, 63), [text_Rect_button.topleft[0], text_Rect_button.topleft[1],
                                                text_Rect_button.bottomright[0] - text_Rect_button.topleft[0],
                                                text_Rect_button.bottomright[1] - text_Rect_button.topleft[1]])
    screen.blit(text_button, text_Rect_button)

    pygame.draw.line(screen, (63, 63, 63), [10, 770], [WIDTH * 3 / 16 - 10, 770], 48)
    pygame.draw.line(screen, (63, 63, 63), [WIDTH * 3 / 16 + 10, 770], [WIDTH * 6 / 16 - 10, 770], 48)
    pygame.draw.line(screen, (63, 63, 63), [WIDTH - 10, 770], [WIDTH - (WIDTH * 3 / 16 - 10), 770], 48)
    pygame.draw.line(screen, (63, 63, 63), [WIDTH - (WIDTH * 3 / 16 + 10), 770], [WIDTH - (WIDTH * 6 / 16 - 10), 770], 48)

    if doAddFrac > 0:
        font1 = pygame.font.SysFont("malgungothic", 24, True, False)
        text_Title1 = font1.render("음악 조각 추가!", True, (0, 0, 255))
        text_Rect1 = text_Title1.get_rect()
        text_Rect1.centerx = round(WIDTH * 3 / 32)
        text_Rect1.centery = round(770)
        screen.blit(text_Title1, text_Rect1)
    if existingFrac > 0:
        font2 = pygame.font.SysFont("malgungothic", 24, True, False)
        text_Title2 = font2.render("연주중인 조각..", True, (255, 0, 0))
        text_Rect2 = text_Title2.get_rect()
        text_Rect2.centerx = round(WIDTH * 9 / 32)
        text_Rect2.centery = round(770)
        screen.blit(text_Title2, text_Rect2)
    if doChangeInst > 0:
        font3 = pygame.font.SysFont("malgungothic", 24, True, False)
        text_Title3 = font3.render("악기 재설정!", True, (0, 255, 0))
        text_Rect3 = text_Title3.get_rect()
        text_Rect3.centerx = round(WIDTH - (WIDTH * 9 / 32))
        text_Rect3.centery = round(770)
        screen.blit(text_Title3, text_Rect3)
    if InstUnchanged > 0:
        font4 = pygame.font.SysFont("malgungothic", 24, True, False)
        text_Title4 = font4.render("똑같은 악기...", True, (255, 0, 0))
        text_Rect4 = text_Title4.get_rect()
        text_Rect4.centerx = round(WIDTH - (WIDTH * 3 / 32))
        text_Rect4.centery = round(770)
        screen.blit(text_Title4, text_Rect4)

    return mouse, text_Rect_button

def attach_words(caption_words):
    caption_sentence = ""
    for i in range(len(caption_words) - 1):
        caption_sentence += caption_words[i + 1]
        caption_sentence += " "
    print(caption_sentence)
    return caption_sentence

vol_top = [0, 0, 0]
vol_chord = [0, 0, 0]
vol_bass = [0, 0, 0]
vol_agrement = 0
vol_pad = 0
vol_percussion = 0
col_top = [0, 0]
col_chord = [0, 0]
col_bass = [0, 0]
col_agrement = [0, 0, 0]
col_pad = [0, 0, 0]
col_percussion = [0, 0, 0]

def apply_volume():
    global vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion
    vol_top = volume_modify[0:3]
    vol_chord = volume_modify[3:6]
    vol_bass = volume_modify[6:9]
    vol_agrement = volume_modify[9]
    vol_pad = volume_modify[10]
    vol_percussion = volume_modify[11]
    col_top = [response(color_modify[0] == 0), response(color_modify[0] == 1)]
    col_chord = [response(color_modify[1] == 0), response(color_modify[1] == 1)]
    col_bass = [response(color_modify[2] == 0), response(color_modify[2] == 1)]
    col_agrement = [response(color_modify[3] == 0), response(color_modify[3] == 1), response(color_modify[3] == 2)]
    col_pad = [response(color_modify[4] == 0), response(color_modify[4] == 1), response(color_modify[4] == 2)]
    col_percussion = [response(color_modify[5] == 0), response(color_modify[5] == 1), response(color_modify[5] == 2)]

def change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion):
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
    for c in range(len(col_bass)):
        if col_bass[c] == 0:
            for f in range(len(vol_bass)):
                fractures_bass[f + len(vol_bass) * c].set_volume(0)
        elif col_bass[c] == 1:
            for f in range(len(vol_bass)):
                fractures_bass[f + len(vol_bass) * c].set_volume(vol_bass[f])
    for c in range(len(col_agrement)):
        if col_agrement[c] == 0:
            for f in range(1):
                fractures_agrement[f + 1 * c].set_volume(0)
        elif col_agrement[c] == 1:
            for f in range(1):
                fractures_agrement[f + 1 * c].set_volume(vol_agrement)
    for c in range(len(col_pad)):
        if col_pad[c] == 0:
            for f in range(1):
                fractures_pad[f + 1 * c].set_volume(0)
        elif col_pad[c] == 1:
            for f in range(1):
                fractures_pad[f + 1 * c].set_volume(vol_pad)
    for c in range(len(col_percussion)):
        if col_percussion[c] == 0:
            for f in range(1):
                fractures_percussion[f + 1 * c].set_volume(0)
        elif col_percussion[c] == 1:
            for f in range(1):
                fractures_percussion[f + 1 * c].set_volume(vol_percussion)

def playsound():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(128)
    WIDTH = 1280
    HEIGHT = 820
    BACKGROUND = (32, 127, 191)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("아트버스 13조 : 사진을 찍으며 흩어진 음악 조각 모으기 ")
    clock = pygame.time.Clock()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    encoder, decoder, word_map, rev_word_map = network_init(device)

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    screen.fill(BACKGROUND)

    _f = get_camera(screen, capture)

    caption_sentence = "Caption of the Image Here"
    doAddFrac = 0
    existingFrac = 0
    doChangeInst = 0
    InstUnchanged = 0

    _m, _b = draw_screen(screen, WIDTH, HEIGHT, caption_sentence, doAddFrac, existingFrac, doChangeInst, InstUnchanged)

    pygame.display.flip()

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
    fractures_bass.append(pygame.mixer.Sound('fractures/bass guitar frac1.wav'))
    fractures_bass.append(pygame.mixer.Sound('fractures/bass guitar frac2.wav'))
    fractures_bass.append(pygame.mixer.Sound('fractures/bass guitar frac3.wav'))
    fractures_bass.append(pygame.mixer.Sound('fractures/bass eguitar frac1.wav'))
    fractures_bass.append(pygame.mixer.Sound('fractures/bass eguitar frac2.wav'))
    fractures_bass.append(pygame.mixer.Sound('fractures/bass eguitar frac3.wav'))
    fractures_agrement.append(pygame.mixer.Sound('fractures/agrement dreamy.wav'))
    fractures_agrement.append(pygame.mixer.Sound('fractures/agrement space.wav'))
    fractures_agrement.append(pygame.mixer.Sound('fractures/agrement meta.wav'))
    fractures_pad.append(pygame.mixer.Sound('fractures/pad string.wav'))
    fractures_pad.append(pygame.mixer.Sound('fractures/pad organ.wav'))
    fractures_pad.append(pygame.mixer.Sound('fractures/pad flute.wav'))
    fractures_percussion.append(pygame.mixer.Sound('fractures/percussion1.wav'))
    fractures_percussion.append(pygame.mixer.Sound('fractures/percussion2.wav'))
    fractures_percussion.append(pygame.mixer.Sound('fractures/percussion3.wav'))

    apply_volume()

    Running = True

    while Running:
        for f in fractures_top:
            f.play(0)
        for f in fractures_chord:
            f.play(0)
        for f in fractures_bass:
            f.play(0)
        for f in fractures_agrement:
            f.play(0)
        for f in fractures_pad:
            f.play(0)
        for f in fractures_percussion:
            f.play(0)
        change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion)

        screen.fill(BACKGROUND)

        frame = get_camera(screen, capture)

        mouse, text_Rect_button = draw_screen(screen, WIDTH, HEIGHT, caption_sentence, doAddFrac, existingFrac, doChangeInst, InstUnchanged)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and \
                        text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
                    caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                    doAddFrac, existingFrac, doChangeInst, InstUnchanged = interpret_words(caption_words)
                    caption_sentence = attach_words(caption_words)
                    apply_volume()
                    change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Running = False
                if event.key == pygame.K_SPACE:
                    caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                    doAddFrac, existingFrac, doChangeInst, InstUnchanged = interpret_words(caption_words)
                    caption_sentence = attach_words(caption_words)
                    apply_volume()
                    change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion)

        if doAddFrac > 0:
            doAddFrac -= 1
        if existingFrac > 0:
            existingFrac -= 1
        if doChangeInst > 0:
            doChangeInst -= 1
        if InstUnchanged > 0:
            InstUnchanged -= 1

        while Running and pygame.mixer.get_busy():
            screen.fill(BACKGROUND)

            frame = get_camera(screen, capture)

            mouse, text_Rect_button = draw_screen(screen, WIDTH, HEIGHT, caption_sentence, doAddFrac, existingFrac, doChangeInst, InstUnchanged)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_Rect_button.topleft[0] <= mouse[0] <= text_Rect_button.bottomright[0] and text_Rect_button.topleft[1] <= mouse[1] <= text_Rect_button.bottomright[1]:
                        caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                        doAddFrac, existingFrac, doChangeInst, InstUnchanged = interpret_words(caption_words)
                        caption_sentence = attach_words(caption_words)
                        apply_volume()
                        change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Running = False
                    if event.key == pygame.K_SPACE:
                        caption_words = image_captioning(frame, encoder, decoder, word_map, rev_word_map, device)
                        doAddFrac, existingFrac, doChangeInst, InstUnchanged = interpret_words(caption_words)
                        caption_sentence = attach_words(caption_words)
                        apply_volume()
                        change_volume(fractures_top, fractures_chord, fractures_bass, fractures_agrement, fractures_pad, fractures_percussion, vol_top, vol_chord, vol_bass, vol_agrement, vol_pad, vol_percussion, col_top, col_chord, col_bass, col_agrement, col_pad, col_percussion)

            if doAddFrac > 0:
                doAddFrac -= 1
            if existingFrac > 0:
                existingFrac -= 1
            if doChangeInst > 0:
                doChangeInst -= 1
            if InstUnchanged > 0:
                InstUnchanged -= 1

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
initMixer()
playsound()
print("Done")