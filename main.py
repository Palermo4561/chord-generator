'''
Creted by Grayson Palermo 
1/1/2024
A basic chord generator in pygame intended for internet (async) use 
'''


"""
TODO:
make background screen better 
add typehints and comments 
correct variable names 
add better logic for chord creation 
organize code 
basic polish
"""


"""
Credits: 
Font - https://www.1001freefonts.com/lato.font 

"""

import asyncio, sys
import pygame as pg
from random import randint
from variables import *
from enum import Enum


async def main():
    
    pg.init()

    win = pg.display.set_mode((size + side_size, size), flags=pg.NOFRAME)
    win_rect = pg.Rect(0, 0, size, size)
    side_rect = pg.Rect(size, 0, side_size, size)
    pg.display.set_caption('Chord Generator')
    pg.display.set_icon(pg.image.load('icon.png').convert_alpha())
    
    font = pg.font.Font('Lato-Bold.ttf', 40)

    create_new_chords = True
    chords = []
    difficulty = Difficulty(3)

    running = True
    while running:
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

            if event.type == pg.MOUSEBUTTONUP:
                if difficulty.up_button.collides_with_mouse():
                    difficulty.add()
                elif difficulty.down_button.collides_with_mouse():
                    difficulty.sub()
                elif win_rect.collidepoint(pg.mouse.get_pos()):
                    create_new_chords = True
                elif pg.mouse.get_pos()[0] >= size + side_size//2 and pg.mouse.get_pos()[1] <= size//8:
                    running = False

        if create_new_chords:
            chords = get_chords(font, difficulty)
            create_new_chords = False

        draw(win, difficulty, chords, win_rect, side_rect)
        
        pg.display.update()
        await asyncio.sleep(0)

    win.fill('black')
    exit_program()


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'


class Button():

    def __init__(self, up_or_down:Direction) -> None:
        self.win = pg.display.get_surface()
        self.font = pg.font.Font('Lato-Bold.ttf', side_size//2)

        match up_or_down:
            case Direction.UP:
                self.rect = pg.Rect(size + side_size//2, size//4, side_size//2, size//4)
                self.text = '+'
            case Direction.DOWN:
                self.rect = pg.Rect(size + side_size//2, 3 * size//4, side_size//2, size//4)
                self.text = '-'
            

    def collides_with_mouse(self):
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def draw(self):
        pg.draw.rect(self.win, colors['button'], self.rect)
        text = self.font.render(self.text, True, colors['button_text'])
        self.win.blit(text, text.get_rect(center=self.rect.center))

        pg.draw.rect(self.win, colors['borders'], self.rect, 3)
 

class Difficulty():

    max_value = 10
    min_value = 1

    def __init__(self, value):
        
        self.value = value

        self.up_button = Button(Direction.UP)
        self.down_button = Button(Direction.DOWN)
        self.win = pg.display.get_surface()

        self.font = pg.font.Font('Lato-Bold.ttf', side_size//2)


    def draw(self):
        self.up_button.draw()        
        self.down_button.draw()
        self.draw_num()
        self.draw_slider_bar()


    def draw_num(self):
        dif_text = self.font.render(str(self.value), True, colors['value_num'])
        self.win.blit(dif_text, dif_text.get_rect(center=(size + 3 * side_size//4, 5 * size//8)))


    def draw_slider_bar(self):

        y_filled_in = int(size - (self.value) * (size / (self.max_value)))

        border_rect = pg.Rect(size, 0, side_size//2, size)
        filled_rect = pg.Rect(size, y_filled_in, side_size//2, size - y_filled_in)

        pg.draw.rect(self.win, colors['difficulty_bar'], filled_rect)
        pg.draw.rect(self.win, colors['borders'], border_rect, 3)


    def add(self):
        if self.value < self.max_value: self.value += 1
        
    
    def sub(self):
        if self.value > self.min_value: self.value -= 1



def exit_program():
    pg.quit()
    sys.exit()



def draw(win, difficulty:Difficulty, chords, win_rect, side_rect):
    draw_grid(win, win_rect, side_rect)
    draw_chords(win, chords)
    draw_exit_button(win)
    difficulty.draw()



def draw_grid(win:pg.Surface, win_rect, side_rect):

    win.blit(pg.transform.scale(pg.image.load('Background.png').convert_alpha(), (size + side_size, size)), (0, 0))

    pg.draw.line(win, colors['grid'], (size//2, 0), (size//2, size), 2)
    for n in range(1, 8):
        y = (size//8) * n
        pg.draw.line(win, colors['grid'], (0, y), (size, y))
    
    pg.draw.rect(win, colors['grid'], win_rect, 2)
    pg.draw.rect(win, colors['borders'], win_rect, 3)

    pg.draw.rect(win, colors['grid'], side_rect, 2)
    pg.draw.rect(win, colors['borders'], side_rect, 3)

    pg.draw.line(win, colors['borders'], (size + side_size//2, 0), (size + side_size//2, size), 3)



def random(iterable):
    return iterable[randint(0, len(iterable)-1)]



def check_accidental(note, accidental):
    if accidental == 'b' and note in ('C', 'F'): return ''
    elif accidental == '#' and note in ('B', 'E'): return ''
    return accidental

def get_chords(font:pg.font.Font, difficulty:Difficulty):

    chords = []

    for n in range(16):
        chords.append([font.render(get_chord(difficulty.value), True, colors['chords'])]) 
        chords[n].append(chords[n][0].get_rect(center=(size//4 + (size//2) * (n % 2), size//16 + (size//8) * (n // 2))))
    
    return chords



def get_chord(difficulty:int):

    base_note = random(notes)
    triad = 'maj'
    base_accidental = ''
    extension = ''
    slash_note = ''
    slash_accidental = ''

    if difficulty > 1:
        triad = random(basic_triads)

    if difficulty > 2:
        extension = random(basic_extensions) if randint(0, 3) != 0 and triad not in ('5', '6') else ''

    if difficulty > 3:
        base_accidental = random(accidentals) if randint(0, 3) != 0 else ''
        base_accidental = check_accidental(base_note, base_accidental)

    if difficulty > 4:
        all_triads = basic_triads + adv_triads
        triad = random(all_triads)
        extension = extension if triad not in (adv_triads + ('5', '6')) else ''

    if difficulty > 5:
        slash_note = random(notes)
        triad = random(basic_triads)
        extension = ''
    
    if difficulty > 6:
        extension = random(basic_extensions) if randint(0, 3) != 0 and triad not in ('5', '6') else ''
    
    if difficulty > 7:
        slash_accidental = random(accidentals) if randint(0, 3) != 0 else ''
        slash_accidental = check_accidental(slash_note, slash_accidental)

    if difficulty > 8:
        all_triads = basic_triads + adv_triads
        triad = random(all_triads)
        extension = extension if triad not in (adv_triads + ('5', '6')) else ''

    if difficulty > 9:
        all_extensions = basic_extensions + adv_extensions
        extension = random(all_extensions)
        extension = extension if triad not in (adv_triads + ('5', '6')) else ''
        if extension == 'm7b5': triad = '' 


    return f"{base_note}{base_accidental}{triad}{extension}{'/' if slash_note != '' else ''}{slash_note}{slash_accidental}"


def draw_chords(win, chord_details):
    for chord in chord_details:
            win.blit(*chord)


def draw_exit_button(win):
    rect = pg.Rect(size + side_size//2, 0, side_size//2, size // 8)
    
    pg.draw.rect(win, colors['exit_button'], rect)

    pg.draw.line(win, 'black', (size + 5*side_size//8, size//32), (size + 7*side_size//8, 3 * size//32), 4)
    pg.draw.line(win, 'black', (size + 5*side_size//8, 3 * size//32), (size + 7*side_size//8, size//32), 4)

    pg.draw.rect(win, colors['borders'], rect, 3)



if __name__ == '__main__':
    asyncio.run(main())
