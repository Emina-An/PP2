import pygame
import os
import sys

pygame.init()
pygame.mixer.init()

music_files = ['Улыбайся.mp3', 'Do I Wanna Know.mp3', 'Mi Gente.mp3']
current_track = 0

def load_music(track):
    if os.path.isfile(music_files[track]):
        pygame.mixer.music.load(music_files[track])
        print(f"Now playing: {music_files[track]}")
    else:
        print(f"File {music_files[track]} not found.")
        sys.exit()


load_music(current_track)

WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

pygame.mixer.music.set_volume(1.0)

def play_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)

def stop_music():
    pygame.mixer.music.stop()

def next_music():
    global current_track
    current_track = (current_track + 1) % len(music_files)
    load_music(current_track)
    play_music()

def previous_music():
    global current_track
    current_track = (current_track - 1) % len(music_files)
    load_music(current_track)
    play_music()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # p to play music
                play_music()
            elif event.key == pygame.K_s:  # s to stop music
                stop_music()
            elif event.key == pygame.K_n:  # n for next track
                next_music()
            elif event.key == pygame.K_b:  # b previous track
                previous_music()

    pygame.display.flip()

pygame.quit()
sys.exit()
