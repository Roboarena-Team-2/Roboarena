import pygame


class Sounds:
    def __init__(self, effect_volume=1.0, music_volume=1.0):
        pygame.mixer.init()
        # load sounds
        self.sounds = {
            "wall_hit_sound": pygame.mixer.Sound("../resources/sounds/wall_hit.ogg"),
            "lava_sound": pygame.mixer.Sound("../resources/sounds/lava.wav"),
            "ice_sound": pygame.mixer.Sound(
                "../resources/sounds/cartoon-slide-whistle-down-1-176647.mp3"
            ),
            "sand_sound": pygame.mixer.Sound("../resources/sounds/sand.wav"),
            "bush_sound": pygame.mixer.Sound("../resources/sounds/bush.ogg"),
            "shot_sound": pygame.mixer.Sound("../resources/sounds/shoot.ogg"),
            "drive_sound": pygame.mixer.Sound("../resources/sounds/drive.mp3"),
            "player_hit_sound": pygame.mixer.Sound(
                "../resources/sounds/player_hit.ogg"
            ),
            "spider_sound": pygame.mixer.Sound(
                "../resources/sounds/bs-_swarm-of-roacheswav-14442.mp3"
            ),
            "countdown_sound": pygame.mixer.Sound("../resources/sounds/countdown.ogg"),
            "gameover_sound": pygame.mixer.Sound(
                "../resources/sounds/game_over_bad_chest.wav"
            ),
            "win_sound": pygame.mixer.Sound("../resources/sounds/tadaa-47995.mp3"),
            "powerup_sound": pygame.mixer.Sound(
                "../resources/sounds/power_up_sound_v1.ogg"
            ),
            "background_sound": pygame.mixer.Sound(
                "../resources/sounds/FutureAmbient_3.wav"
            ),
        }

        # different channels fot different sound categories
        self.channel_move = pygame.mixer.Channel(1)
        self.channel_move.set_volume(effect_volume)
        self.channel_loop = pygame.mixer.Channel(2)
        self.channel_loop.set_volume(effect_volume)
        self.channel_single_texture = pygame.mixer.Channel(3)
        self.channel_single_texture.set_volume(effect_volume)
        self.channel_shooting = pygame.mixer.Channel(4)
        self.channel_shooting.set_volume(effect_volume)
        self.channel_other = pygame.mixer.Channel(5)
        self.channel_other.set_volume(effect_volume)
        self.channel_music = pygame.mixer.Channel(6)
        self.channel_music.set_volume(music_volume * 0.1)
        self.loops = {"bush_sound", "sand_sound"}
        self.single_textures = {"wall_hit_sound", "lava_sound", "ice_sound"}
        self.shooting = {"shot_sound", "player_hit_sound"}
        self.other = {"gameover_sound", "win_sound", "countdown_sound", "powerup_sound"}
        self.current_loop = None
        self.move_playing = False
        self.drive = False
        self.spider = False

        self.sounds["drive_sound"].set_volume(0.6)
        self.sounds["countdown_sound"].set_volume(0.3)
        self.sounds["player_hit_sound"].set_volume(0.3)

    def play_sound(self, action: str):
        if action == "drive_sound" and not self.move_playing:
            self.channel_move.play(self.sounds["drive_sound"], loops=-1)
            self.move_playing = True
            self.drive = True
        if action == "spider_sound" and not self.move_playing:
            self.channel_move.play(self.sounds["spider_sound"], loops=-1)
            self.move_playing = True
            self.spider = True
        if action in self.loops:
            if action != self.current_loop:
                self.stop_loop(self.current_loop)
                if self.move_playing:
                    if self.drive:
                        self.sounds["drive_sound"].set_volume(
                            0.4
                        )  # make drive sound quieter while other loop sound is playing
                    if self.spider:
                        self.sounds["spider_sound"].set_volume(
                            0.7
                        )  # make spider sound quieter while other loop sound is playing
                if not self.channel_loop.get_busy():
                    self.channel_loop.play(self.sounds[action], loops=-1)
                self.current_loop = action
        if action in self.single_textures:
            if (
                not self.channel_single_texture.get_busy()
                and not self.channel_single_texture.get_sound == self.sounds[action]
            ):
                self.channel_single_texture.play(self.sounds[action], loops=0)
        if action in self.shooting:
            if not self.channel_shooting.get_busy():
                self.channel_shooting.play(self.sounds[action], loops=0)
        if action in self.other:
            if not self.channel_other.get_busy():
                self.channel_other.play(self.sounds[action], loops=0)
        if action == "background_sound":
            if not self.channel_music.get_busy():
                self.channel_music.play(self.sounds[action], loops=-1)

    def stop_loop(self, action: str | None):
        if action is None:
            return
        if action == "drive_sound":
            self.move_playing = False
            self.drive = False
            if self.channel_move.get_busy():
                self.channel_move.stop()
        if action == "spider_sound":
            self.move_playing = False
            self.spider = False
            if self.channel_move.get_busy():
                self.channel_move.stop()
        if action in self.loops:
            if self.channel_loop.get_busy():
                self.sounds[action].stop()
            self.current_loop = None
            if self.drive:
                self.sounds["drive_sound"].set_volume(0.6)
            if self.spider:
                self.sounds["spider_sound"].set_volume(1.0)

    def stop_all_sounds(self):
        for sound in self.sounds:
            if sound == "drive_sound" or sound == "spider_sound":
                if self.channel_move.get_busy():
                    self.channel_move.stop()
            if sound in self.loops and self.channel_loop.get_busy():
                self.channel_loop.stop()
            if sound in self.single_textures and self.channel_single_texture.get_busy():
                self.channel_single_texture.stop()
            if sound in self.shooting and self.channel_shooting.get_busy():
                self.channel_shooting.stop()
            if sound in self.other and self.channel_other.get_busy():
                self.channel_other.stop()
            if sound == "background_sound" and self.channel_music.get_busy():
                self.channel_music.stop()
            self.current_loop = None
            self.move_playing = False
            self.drive = False
            self.spider = False
