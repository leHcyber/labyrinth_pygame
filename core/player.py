import pygame


class Entity:
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def take_damage(self, dmg):
        self.hp = max(0, int(self.hp - dmg))

    def is_dead(self):
        return self.hp <= 0
    
    def set_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration
    
# -------------------------

class Player(Entity):
    def __init__(self):
        super().__init__(hp=5, damage=1)

        self.x = 1
        self.y = 1

        self.inventaire = []
        self.score = 0

        self.message = ""
        self.message_timer = 0

        self.amulette_charges = 0
        self.bouclier_charges = 0

        self.equipment_bonus = {
        "Épée": 1,
        "Grande Épée": 2,
        "Massue": 3
    }

        self.objets = {
            "K": ("Clé", self._add_key),
            "P": ("Potion", lambda: self.add_item("Potion")),
            "B": ("Bouclier", self.add_bouclier),
            "E": ("Épée", lambda: self.add_item("Épée")),
            "E2": ("Grande Épée", lambda: self.add_item("Grande Épée")),
            "E3": ("Massue", lambda: self.add_item("Massue")),
            "T": ("Trésor", self._add_score),
            "!": ("Amulette", self._add_amulette)
        }

    # -------------------------
    # AMULETTE
    def _add_amulette(self):
        self.add_item("Amulette")
        self.amulette_charges = 2

    # -------------------------
    # BOUCLIER
    def add_bouclier(self):
        self.add_item("Bouclier")
        self.bouclier_charges = 5
        self.set_message("Bouclier activé (5 charges)", 60)
    # -------------------------
    # DAMAGE

    def get_damage(self):
        dmg = self.damage

        for item in self.inventaire:
            dmg += self.equipment_bonus.get(item, 0)

        return dmg

    def take_damage(self, dmg):

        if self.bouclier_charges > 0:
            self.bouclier_charges -= 1
            self.set_message(f"Bouclier bloque ({self.bouclier_charges})", 60)
            return

        if self.amulette_charges > 0:
            self.amulette_charges -= 1
            self.set_message(f"Amulette bloque ({self.amulette_charges})", 60)
            return

        super().take_damage(dmg)

    # -------------------------
    # INVENTAIRE

    def add_item(self, item):
        self.inventaire.append(item)

    def remove_item(self, item):
        if item in self.inventaire:
            self.inventaire.remove(item)

    def has_item(self, item):
        return item in self.inventaire

    # -------------------------
    # POTION

    def use_potion(self):
        if self.has_item("Potion"):
            self.inventaire.remove("Potion")
            self.hp += 2
            return "+2 HP"
        return "Pas de potion"

    # -------------------------
    # MAP INTERACTION

    def interact(self, case):
        obj = self.objets.get(case)

        if not obj:
            return None

        name, effect = obj
        effect()

        return f"{name} récupéré !"

    # -------------------------
    # EVENTS

    def _add_key(self):
        self.add_item("Clé")

    def _add_score(self):
        self.score += 10