import pygame
import os
import json
import sys
import time
from random import randint
import arabic_reshaper
from bidi.algorithm import get_display

pygame.init()

WIDTH, HEIGHT = 960, 640
FPS = 60

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
TURQUOISE = (0, 255, 255)
RED = (255, 80, 80)
GREEN = (80, 255, 80)
GRAY = (80, 80, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("حدس عدد | Number Guess")
clock = pygame.time.Clock()

font_path_regular = "fonts/Vazir-Regular.ttf"
font_path_bold = "fonts/Vazir-Bold.ttf"

font = pygame.font.Font(font_path_regular, 28)
large_font = pygame.font.Font(font_path_bold, 48)

LANG = 'fa'

TEXTS = {
    'fa': {
        'start': "شروع بازی",
        'note': "یادداشت",
        'about': "درباره بازی",
        'fullscreen': "تمام‌صفحه",
        'exit': "خروج",
        'title': "حدس عدد",
        'input_hint': "عدد ۵ رقمی وارد کن:",
        'time_left': "زمان باقی‌مانده:",
        'guesses_left': "تعداد حدس باقی‌مانده:",
        'clue': "سرنخ:",
        'correct': "تبریک! عدد درست حدس زدی!",
        'wrong': "حدس اشتباه است",
        'game_over': "بازی تمام شد! عدد درست:",
        'try_again': "دوباره بازی کن",
        'language_toggle': "تغییر زبان"
    },
    'en': {
        'start': "Start Game",
        'note': "Note",
        'about': "About Game",
        'fullscreen': "Full Screen",
        'exit': "Exit",
        'title': "Number Guess",
        'input_hint': "Enter 5-digit number:",
        'time_left': "Time Left:",
        'guesses_left': "Guesses Left:",
        'clue': "Clue:",
        'correct': "Congrats! Correct guess!",
        'wrong': "Wrong guess",
        'game_over': "Game Over! The number was:",
        'try_again': "Play Again",
        'language_toggle': "Toggle Language"
    }
}

buttons_rects = {}

def reshape_text(text):
    """برای اتصال و راست‌چین درست متن فارسی"""
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    return bidi_text

def render_text(text, font_obj, color):
    if LANG == 'fa':
        text = reshape_text(text)
    return font_obj.render(text, True, color)

def draw_text_right(text, font_obj, color, right_x, y):
    surf = render_text(text, font_obj, color)
    rect = surf.get_rect()
    rect.topright = (right_x, y)
    screen.blit(surf, rect)
    return rect

def draw_text_left(text, font_obj, color, left_x, y):
    surf = render_text(text, font_obj, color)
    rect = surf.get_rect()
    rect.topleft = (left_x, y)
    screen.blit(surf, rect)
    return rect

def toggle_language():
    global LANG
    LANG = 'en' if LANG == 'fa' else 'fa'




def draw_menu():
    screen.fill(BLACK)
    texts = TEXTS[LANG]

    # عنوان وسط صفحه
    if LANG == 'fa':
        draw_text_right(texts['title'], large_font, TURQUOISE, WIDTH//2 + large_font.size(texts['title'])[0]//2, 80)
    else:
        surf = render_text(texts['title'], large_font, TURQUOISE)
        rect = surf.get_rect(center=(WIDTH//2, 80))
        screen.blit(surf, rect)

    buttons = ['start', 'note', 'about', 'fullscreen', 'exit', 'language_toggle']
    spacing = 70
    buttons_rects.clear()

    for i, key in enumerate(buttons):
        y = 200 + i * spacing
        color = WHITE
        text = texts[key]

        if LANG == 'fa':
            rect = draw_text_right(text, font, color, WIDTH - 100, y)
        else:
            rect = draw_text_left(text, font, color, 100, y)

        buttons_rects[key] = rect

    pygame.display.flip()

def load_note():
    try:
        with open("note.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(LANG, "")
    except Exception as e:
        print(f"Error loading note: {e}")
        return "یادداشت در دسترس نیست." if LANG == 'fa' else "Note unavailable."


def show_note():
    note_text = load_note()
    running = True

    while running:
        screen.fill(BLACK)
        lines = note_text.split('\n')
        start_y = 100

        for line in lines:
            if LANG == 'fa':
                draw_text_right(line, font, WHITE, WIDTH - 40, start_y)
            else:
                draw_text_left(line, font, WHITE, 40, start_y)
            start_y += 40

        # دکمه برگشت
        back_text = "بازگشت" if LANG == 'fa' else "Back"
        if LANG == 'fa':
            back_rect = draw_text_right(back_text, font, RED, WIDTH - 40, HEIGHT - 60)
        else:
            back_rect = draw_text_left(back_text, font, RED, 40, HEIGHT - 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if back_rect.collidepoint(mx, my):
                    running = False

        clock.tick(FPS)

def show_about():
    about_text = load_about()
    running = True

    while running:
        screen.fill(BLACK)
        lines = about_text.split('\n')
        start_y = 100

        for line in lines:
            if LANG == 'fa':
                draw_text_right(line, font, WHITE, WIDTH - 40, start_y)
            else:
                draw_text_left(line, font, WHITE, 40, start_y)
            start_y += 40

        # دکمه برگشت
        back_text = "بازگشت" if LANG == 'fa' else "Back"
        if LANG == 'fa':
            back_rect = draw_text_right(back_text, font, RED, WIDTH - 40, HEIGHT - 60)
        else:
            back_rect = draw_text_left(back_text, font, RED, 40, HEIGHT - 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if back_rect.collidepoint(mx, my):
                    running = False

        clock.tick(FPS)

def load_about():
    try:
        with open("about.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(LANG, "")
    except Exception as e:
        print(f"Error loading about text: {e}")
        return "درباره بازی در دسترس نیست." if LANG == 'fa' else "About text unavailable."


def get_clue(secret, guess):
    # سرنخ پایه: تعداد ارقام درست در جای درست + تعداد ارقام درست در جای اشتباه
    bulls = sum(s == g for s, g in zip(secret, guess))  # درست و سرجای خودش
    cows = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - bulls  # درست ولی جای اشتباه
    return f"{bulls} رقم در جای درست، {cows} رقم در جای اشتباه"

def game_loop():
    secret = ''.join(str(randint(0,9)) for _ in range(5))
    guesses_left = 15
    time_limit = 510  # ثانیه
    start_time = time.time()
    input_text = ""
    clues = []
    game_over = False
    won = False

    while True:
        elapsed = time.time() - start_time
        remaining = max(0, int(time_limit - elapsed))
        texts = TEXTS[LANG]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT, screen
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(input_text) == 5 and input_text.isdigit():
                        guess = input_text
                        input_text = ""
                        guesses_left -= 1

                        if guess == secret:
                            game_over = True
                            won = True
                        else:
                            clue = get_clue(secret, guess)
                            clues.append((guess, clue))
                            if guesses_left <= 0 or remaining <= 0:
                                game_over = True
                    else:
                        # نپذیرفتن حدس نامعتبر
                        pass
                elif event.unicode.isdigit() and len(input_text) < 5:
                    input_text += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # برگشت به منو از صفحه بازی
                if 'exit' in buttons_rects and buttons_rects['exit'].collidepoint(mx, my):
                    return
                if 'language_toggle' in buttons_rects and buttons_rects['language_toggle'].collidepoint(mx, my):
                    toggle_language()

        screen.fill(BLACK)

        # نمایش عنوان بازی بالای صفحه
        if LANG == 'fa':
            draw_text_right(texts['title'], large_font, TURQUOISE, WIDTH - 40, 20)
        else:
            surf = render_text(texts['title'], large_font, TURQUOISE)
            screen.blit(surf, (40, 20))

        # نمایش تایمر
        time_text = f"{texts['time_left']} {remaining}s"
        if LANG == 'fa':
            draw_text_right(time_text, font, WHITE, WIDTH - 40, 100)
        else:
            draw_text_left(time_text, font, WHITE, 40, 100)

        # نمایش تعداد حدس باقی‌مانده
        guess_text = f"{texts['guesses_left']} {guesses_left}"
        if LANG == 'fa':
            draw_text_right(guess_text, font, WHITE, WIDTH - 40, 140)
        else:
            draw_text_left(guess_text, font, WHITE, 40, 140)

        # نمایش ورودی عدد
        hint_text = texts['input_hint']
        if LANG == 'fa':
            draw_text_right(hint_text, font, GRAY, WIDTH - 40, 180)
            draw_text_right(input_text + ("|" if int(time.time() * 2) % 2 == 0 else ""), font, WHITE, WIDTH - 40, 220)
        else:
            draw_text_left(hint_text, font, GRAY, 40, 180)
            draw_text_left(input_text + ("|" if int(time.time() * 2) % 2 == 0 else ""), font, WHITE, 40, 220)

        # نمایش سرنخ‌ها
        if clues:
            clue_title = texts['clue']
            if LANG == 'fa':
                draw_text_right(clue_title, font, TURQUOISE, WIDTH - 40, 260)
                start_y = 300
                for guess, clue in reversed(clues[-5:]):  # ۵ سرنخ آخر
                    line = f"{guess}: {clue}"
                    draw_text_right(line, font, WHITE, WIDTH - 40, start_y)
                    start_y += 30
            else:
                draw_text_left(clue_title, font, TURQUOISE, 40, 260)
                start_y = 300
                for guess, clue in reversed(clues[-5:]):
                    line = f"{guess}: {clue}"
                    draw_text_left(line, font, WHITE, 40, start_y)
                    start_y += 30

        # اگر بازی تموم شده
        if game_over:
            if won:
                msg = texts['correct']
                color = GREEN
            else:
                msg = f"{texts['game_over']} {secret}"
                color = RED
            if LANG == 'fa':
                draw_text_right(msg, large_font, color, WIDTH//2 + large_font.size(msg)[0]//2, HEIGHT//2 - 60)
                # دکمه دوباره بازی کن وسط صفحه
                play_again_rect = draw_text_right(texts['try_again'], font, TURQUOISE, WIDTH//2 + font.size(texts['try_again'])[0]//2, HEIGHT//2 + 20)
            else:
                surf = render_text(msg, large_font, color)
                rect = surf.get_rect(center=(WIDTH//2, HEIGHT//2 - 60))
                screen.blit(surf, rect)
                play_again_rect = render_text(texts['try_again'], font, TURQUOISE).get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
                screen.blit(render_text(texts['try_again'], font, TURQUOISE), play_again_rect)

            # کلیک روی دکمه "دوباره بازی کن"
            mx, my = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if click[0] and play_again_rect.collidepoint(mx, my):
                time.sleep(0.2)  # جلوگیری از چند بار کلیک سریع
                return game_loop()

        pygame.display.flip()
        clock.tick(FPS)

def main_menu():
    global WIDTH, HEIGHT, screen
    while True:
        draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for key, rect in buttons_rects.items():
                    if rect.collidepoint(mx, my):
                        if key == 'start':
                            game_loop()
                        elif key == 'exit':
                            pygame.quit()
                            sys.exit()
                        elif key == 'language_toggle':
                            toggle_language()
                        elif key == 'fullscreen':
                            pygame.display.toggle_fullscreen()
                        elif key == 'note':
                            show_note()
                        elif key == 'about':
                            show_about()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    toggle_language()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        clock.tick(FPS)



if __name__ == '__main__':
    main_menu()
