from collections import namedtuple

import pygame
from pygame.locals import *
from pygame.time import Clock
from typing import NamedTuple, Tuple, List, Callable


class Scene:
    def __init__(self, context: NamedTuple):
        self.running = True
        self.context = context
        self.clock = Clock()

    def on_destroy(self):
        pass

    def on_mouse_down(self, button: Tuple, position: Tuple):
        pass

    def on_mouse_move(self, position: Tuple):
        pass

    def on_mouse_up(self, button: Tuple, position: Tuple):
        pass

    def on_animation_begin(self, timeline_id: int):
        pass

    def on_animation_end(self, timeline_id: int):
        pass

    def update(self, ticks: int):
        pass

    def render(self):
        pass

    def mainloop(self):
        while self.running:
            ticks = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()
                    self.on_mouse_down(buttons, position)
                elif event.type == MOUSEMOTION:
                    position = pygame.mouse.get_pos()
                    self.on_mouse_move(position)
                elif event.type == MOUSEBUTTONUP:
                    buttons = pygame.mouse.get_pressed()
                    position = pygame.mouse.get_pos()
                    self.on_mouse_up(buttons, position)
                elif event.type == ANIMATION_BEGIN:
                    timeline_id = event.timeline_id
                    self.on_animation_begin(timeline_id)
                elif event.type == ANIMATION_END:
                    timeline_id = event.timeline_id
                    self.on_animation_end(timeline_id)
            self.update(ticks)
            self.render()
            pygame.display.update()
            self.clock.tick(30)
        self.on_destroy()


Animation = namedtuple("Animation",
                       ["begin_state", "end_state", "delay", "duration", "setter"])

ANIMATION_BEGIN = pygame.event.custom_type()
ANIMATION_END = pygame.event.custom_type()


class Timeline:
    def __init__(self, timeline_id: int):
        self.timeline_id = timeline_id
        self.animations = []
        self.begin_tick = 0

    def add_animation(self, animation: Animation):
        self.animations.append(animation)

    def get_last_time(self) -> int:
        animation_time = [animation.delay + animation.duration for animation in self.animations]
        if len(animation_time) > 0:
            return max(animation_time)
        else:
            return 0

    def animation_begin(self, ticks: int):
        self.begin_tick = ticks

    def update(self, ticks: int):
        ms = ticks - self.begin_tick
        for animation in self.animations:
            if ms < animation.delay:
                pass
            elif animation.delay <= ms <= animation.delay + animation.duration:
                progress = (ms - animation.delay) / animation.duration
                animation.setter(animation.begin_state, animation.end_state, progress)
            elif ms > animation.delay + animation.duration:
                animation.setter(animation.begin_state, animation.end_state, 1.0)
                self.animations.remove(animation)
        if len(self.animations) == 0:
            event = pygame.event.Event(ANIMATION_END, dict(timeline_id=self.timeline_id))
            pygame.event.post(event)
            self.reset_clock()

    def reset_clock(self):
        self.begin_tick = 0


class Play:
    def __init__(self, target: List[int], moves: int, on_win: Callable, on_lose: Callable):
        kind_count = len(target)
        self.target = target.copy()
        self.moves = moves
        self.picked_counts = [0] * kind_count
        self.on_win = on_win
        self.on_lose = on_lose

    def update(self, kind: int, count: int) -> (bool, bool):
        self.picked_counts[kind] = min(self.picked_counts[kind] + count, self.target[kind])
        self.moves -= 1
        fulfilled = [self.target[i] == count for i, count in enumerate(self.picked_counts)]
        won = all(fulfilled)
        lost = not all(fulfilled) and self.moves < 1
        if won:
            self.on_win(self.picked_counts)
        if lost:
            self.on_lose(self.picked_counts)
        return won, lost
