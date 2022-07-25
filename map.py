from dataclasses import dataclass

import pygame
import pytmx
import pyscroll

from player import NPC, Player
from dialog import DialogBox
from music import Music


@dataclass
class Portal:
    origin_world: str
    origin_point: str
    target_world: str
    target_point: str


@dataclass # Permet l'initialisation de l'élément class qui suit
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict() # Liste des cartes
        self.screen = screen
        self.player = player
        self.current_map = "house_player2"
        self.music = Music()

        # Référencement des cartes dispos + portails + PNJ
        self.register_map("world", portals=[
            Portal(origin_world="world", origin_point="enter_house1",
                   target_world = "house_player1", target_point = "spawn_house1"),
            Portal(origin_world="world", origin_point="enter_dungeon",
                   target_world="dungeon", target_point="spawn_dungeon"),
            Portal(origin_world="world", origin_point="enter_surmoi",
                   target_world="surmoi", target_point="spawn_player_moi")
        ], npcs = [
            NPC("paul", nb_points=6),
            NPC("robin", nb_points=4),
            NPC("chat", nb_points=4)
        ])
        self.register_map("house_player1", portals = [
            Portal(origin_world="house_player1", origin_point="exit_house1",
                   target_world="world", target_point="spawn_house1_exit"),
            Portal(origin_world="house_player1", origin_point="house_player_up",
                   target_world="house_player2", target_point="spawn_house_player_stage2")
        ], npcs = [])
        self.register_map("house_player2", portals=[
            Portal(origin_world="house_player2", origin_point="house_player_down",
                   target_world="house_player1", target_point="spawn_house_player_stage1")
        ], npcs=[]),
        self.register_map("surmoi", portals=[
            Portal(origin_world="surmoi", origin_point="exit_moi",
                   target_world="world", target_point="spawn_player_surmoi_exit")
        ], npcs=[
            NPC("spartan", nb_points=2),
            NPC("garde2", nb_points=2),
            NPC("nevrose1", nb_points=4),
            NPC("nevrose2", nb_points=1),
            NPC("jacky", nb_points=1)
        ])
        self.register_map("dungeon", portals=[
            Portal(origin_world="dungeon", origin_point="exit_dungeon",
                   target_world="world", target_point="spawn_dungeon")
        ], npcs = [
            NPC("boss", nb_points=4)
        ])

        # Spawn de départ
        self.spawn_player("pop_player")
        self.teleport_npcs()


    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            sprite.stop_rect = pygame.Rect(sprite.position[0] - 2, sprite.position[1] - 2, 36, 36)
            if sprite.stop_rect.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        # Portails
        for portal in self.get_map().portals:
            if portal.origin_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.spawn_player(copy_portal.target_point)
                    self.music.music_play(origin_world=portal.origin_world, target_world=portal.target_world)

        # Collision avec les murs + NPC
        for sprite in self.get_group().sprites():

            if type(sprite) is NPC:

                sprite.stop_rect = pygame.Rect(sprite.position[0] - 2, sprite.position[1] - 2, 36, 36)
                if sprite.stop_rect.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

        for npc in self.get_map().npcs:
            for sprite in self.get_group().sprites():
                if type(sprite) is Player:
                    if sprite.rect.colliderect(npc.rect):
                        sprite.move_back()


    def spawn_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()


    def register_map(self, name, portals=[], npcs=[]):

        # Charger la carte tmx
        tmx_data = pytmx.util_pygame.load_pygame(f"assets/maps/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # Définir les collisions
        walls = []
        for obj in tmx_data.objects:
            if obj.name == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calques (dont niveau du player)
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        # Récupération des PNJ (NPC) pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Créer un objet map (selon la carte)
        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs

            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for npc in self.get_map().npcs:
            npc.move_npc()



