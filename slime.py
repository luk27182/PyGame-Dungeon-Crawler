import pygame
from settings import *
from character import *


class Slime(Charector):
    def __init__(self, game, groups, pos, collision_groups, time_before_attack):
        super().__init__(game = game, type="slime", groups=groups, animations_names=SLIME_ANIMATION_NAMES,
                         animation_speed=SLIME_ANIMATION_SPEED, graphics_path=SLIME_GRAPHICS_PATH,
                         graphics_scaling=TILE_DIM, starting_graphic="./graphics/slime/slime_animation/enemy0.png",
                         status="slime_animation", hitbox_scaling=(-4 * (TILE_DIM[0] / 16), -8 * (TILE_DIM[1] / 16)),
                         pos=pos, speed=SLIME_WALK_SPEED, health=SLIME_HEALTH, damage_cooldown=SLIME_DAMAGE_COOLDOWN,
                         collision_groups=collision_groups, spawn_immunity_time=time_before_attack)
        self.player = self.game.player
        self.time_before_attack = time_before_attack
        self.hitbox.center = pos
        self.rect.center = self.hitbox.center
        self.move()

    def calculate_motion(self):
        if abs(self.rect.centerx - self.player.rect.centerx) < self.speed:
            self.direction.x = 0
        elif self.rect.centerx < self.player.rect.centerx:
            self.direction.x = 1
        else:
            self.direction.x = -1

        if abs(self.rect.centery - self.player.rect.centery) < self.speed:
            self.direction.y = 0
        elif self.rect.centery < self.player.rect.centery:
            self.direction.y = 1
        else:
            self.direction.y = -1

        if self.direction != (0,0):
            self.direction = self.direction.normalize()

    def check_player_collision(self):
        if self.player.rect.colliderect(self.hitbox):
            self.player.take_damage(1)

    def check_if_dead(self):
        if self.is_dead:
            self.game.score_counter.add_to_score(100)
            self.game.enemies_remaining -= 1
            self.health_counter.health_bar.kill()
            self.health_counter.kill()
            self.kill()

    def update(self):
        if time.time()-self.time_of_creation >= self.time_before_attack:
            self.calculate_motion()
            self.move()
            self.check_player_collision()
            self.check_if_dead()
        self.animate()