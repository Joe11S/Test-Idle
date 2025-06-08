import pygame
import sys
import time
import json
import os   # for checking file existence

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
GRAY = (180, 180, 180)

# Tier base RPS and base cost
TIER_RPS_FLAT = [
    0.01, 0.08, 0.6,
    4, 33, 150,
    940, 8700, 64000,
    510000, 44*(10**5), 32*(10**6),
    24*(10**7), 11*(10**8), 90*(10**8),
    62*(10**9), 32*(10**10), 13*(10**11),
    84*(10**11), 63*(10**12), 34*(10**13),
    21*(10**14), 19*(10**15), 93*(10**15),

    #NEXT PAGE
    63*(10**16), 42*(10**17), 32*(10**18),
    29*(10**19), 21*(10**20), 11*(10**21),
    94*(10**21), 74*(10**22), 56*(10**23),
    20*(10**27), 20*(10**32), 20*(10**37),
    20*(10**42), 20*(10**47), 20*(10**57),
    20*(10**67), 20*(10**77), 20*(10**87),
    20*(10**97), 20*(10**117), 20*(10**137),
    20*(10**157), 20*(10**177), 20*(10**197),
]

# Example unique names for each tier (customize as desired)
TIER_NAMES_FLAT = [
    "Bottle Cap", "Empty Glass Bottle", "Toblerone Bar", 
    "Coca-Cola Bottle", "Breakfast Package", "Stove", 
    "IPhone 15", "Toyota Camry", "Steinway Grand Piano",
    "Simple Townhouse", "Supercar", "Small Private Island",
    "Holiday House", "Twitter", "Meta",
    "Elon Musk", "Vatican", "France",
    "Russia", "US", "Australia",
    "Asia", "Earth", "Mars",

    #NEXT PAGE
    "Inner Solar System", "Jupiter", "Outer Solar System",
    "Sun", "Heliosphere", "Proxima Centauri",
    "A Cen System", "Sirius System", "55 Cancri e",
    "Solar Neighborhood", "Kepler 452b", "Kepler 22b",
    "TRAPPIST-1d", "TRAPPIST-1 System", "Pistol Star",
    "Betelgeuse", "Stephenson 2-18", "Orion Arm",
    "Milky Way", "Messier 87", "IC 1101",
    "Local Group", "Laniakea Supercluster", "Singularity",
]

TOOLTIPS = {
    "Bottle Cap": "Once lost beneath your couch cushions, now the seed of an empire. Every fortune starts somewhere.",
    "Empty Glass Bottle": "The Bottle Cap is useless itself, unless it was integrated into this slightly more useful bottle. A symbol of potential, still empty, but its real value is what's inside it.",
    "Toblerone Bar": "A tiny little mountain-shaped chocolate bar. Sweet and tasty. Humble in essence.",
    "Coca-Cola Bottle": "The Bottle has finally found its purpose here. With sugar, fizz and branding, an iconic drink loved by fast-food lovers.",
    "Breakfast Package": "Bacon and Eggs. The dynamic duo. Every household has them.",
    "Stove": "This is where food is made, including the Breakfast Package you bought previously.",
    "IPhone 15": "This tiny little thingamajig makes them addicted, scrolling for hours on end... and this accidentally gives you income out of addiction. Questionable, isn't it?",
    "Toyota Camry": "A standard-body sedan to bring you everyday. Nothing special about it.",
    "Steinway Grand Piano": "Now you're making a statement! This large instrument plays 'rich vibes' to the entire living room!",
    "Simple Townhouse": "Real Estate has a very high income potential. You made your first move investing there. Tiny, but wait for its returns.",
    "Supercar": "This powerful car doesn't just bring you anywhere fast. Its engine, top speed and bodywork commands attention and prestige. [Unlocks Luxuries Arc]",
    "Small Private Island": "Why rent an apartment when you can own this chunk of land? Now you don't have to pay rent! The rent pays you!",
    "Holiday House": "Rebekah Harkness sold this house to Taylor Swift and referenced it in 'The Last Great American Dynasty'. Later, you bought this house, and your real estate inflow skyrocketed.",
    "Twitter": "This large social media network also happens to be one of the most notorious echo chambers — filtering out all other opinions to ensure that only what is seen as correct passes through.",
    "Meta": "This Tech Titan owns both Instagram and Facebook. Known for Instagram and Facebook reels. A technological powerhouse that competes with Twitter.",
    "Elon Musk": "Your dream has finally come to this moment — out-earning the richest person in the world. You out-earned so hard that you 'bought' him. Now he generates income for you.",
    "Vatican": "However, your hunger for income becomes so insatiable that you proceeded to 'buy' countries now, and this tiny little country inside Rome is the first victim of your relentless pursuit. Now the church bends to your will. [Unlocks Power Arc]",
    "France": "A country of beautiful fashion, really good food and of course, baguettes. Not the biggest country, but the richest in culture.",
    "Russia": "The biggest country, and it's really cold — so cold that it thwarted invaders twice. Even though it is not the richest country today, it used to be the USSR, and that's why you invest on it.",
    "US": "The richest country overall, has Fort Knox, New York and has the most advanced military and technology in the world. A global influence, it exerts power through its interventions. The other side of the Cold War, and way richer than the USSR.",
    "Australia": "Filled with spiders, kangaroos and emus, this is your first continental acquisition yet.",
    "Asia": "With this acquisition, you owned half of civilization itself. The biggest of all continents, this sets the stage of what would be your best acquisition yet.",
    "Earth": "Your best acquisition yet. The Blue Marble and everything inside it, all yours.",
    "Mars": "Musk dreamed of going to the Red Marble, and you didn't just take it, but made it earn for you. [Unlocks Solar Neighborhood Arc]",
    "Inner Solar System": "Venus and Mercury joined your investment portfolio. At this point, you transcended Earth and are now acquiring planets.",
    "Jupiter": "Jupiter is the largest planet in the Solar System... and it's now earning for you.",
    "Outer Solar System": "Saturn, Uranus and Neptune joined your portfolio. Now you have all the planets within reach, earning for you.",
    "Sun": "The very center of the solar system now earns for you. People dream of owning the stars, and you made it real... literally.",
    "Heliosphere": "You now own everything inside the solar system — dwarf planets, asteroids, Kuiper Belt, and the Oort Cloud. Everything earns for you now.",
    "Proxima Centauri": "Your investment portfolio now extends to stars too, and being the closest one, it becomes the first victim of your infinitely relentless acquisitions.",
    "A Cen System": "Why own Proxima when you can own its entire system?",
    "Sirius System": "The brightest star in the sky, that is slightly further out than A Cen, is white and hot, and also has a husk of a massive star, is yours now.",
    "55 Cancri e": "This is an interesting exoplanet because it happens to be made of highly compressed carbon. And compressed carbon = DIAMONDS. Since this planet is diamonds, you want to make it earn for you — which is really immense if you think about it. [Unlocks Ascension]",
    "Solar Neighborhood": "Every star within 100 light years of you, now yours to earn. [Unlocks Galactic Structures Arc]",
    "Kepler 452b": "Earth 2.0. You decided to acquire 'Earth' again — this time, older, wiser, and orbiting a sun that's 1.5 billion years older.",
    "Kepler 22b": "This is basically Earth Pro™. 2x the size of Earth, 4 times heavier, and yes, a lot more ocean.",
    "TRAPPIST-1d": "Earth-sized exoplanet, part of a mini-solar-system. Although it is in the habitable zone, it is tidally locked — which means that daytime is a desert and nighttime is a frozen wasteland.",
    "TRAPPIST-1 System": "Why own a single planet when you can own an entire solar system?",
    "Pistol Star": "A stellar titan. Blue and bright.",
    "Betelgeuse": "This iconic supergiant is visible as a red dot on the upper left shoulder of Orion. This star is a senior, being near the end of its life.",
    "Stephenson 2-18": "This supergiant makes Betelgeuse look like a baseball. This beast is bigger than Saturn's orbit.",
    "Orion Arm": "You now own a full segment of the Milky Way, your home galaxy. Every star in it, now earns for you.",
    "Milky Way": "Why own a segment when you can own the ENTIRE galaxy? Now every single star and Sagittarius A now bows down to you.",
    "Messier 87": "Your portfolio now extends to whole galaxies too, and Messier 87 is one of them... being the site of the first black hole pictured. [Unlocks Beyond Comprehension Arc]",
    "IC 1101": "You acquire a titan of galaxies. Being a really large elliptical galaxy consisting of some of the Universe's oldest stars ever.",
    "Local Group": "Every nearby galaxy: Andromeda, Triangulum, Large and Small Magellanic Clouds — all now earn for you.",
    "Laniakea Supercluster": "Your home cluster of over 100,000 galaxies spanning 520 million light years. So unfathomably big that its paycheck is also unfathomable as well — and you now own it.",
    "Singularity": "Everything in this universe... is now owned by you. You transcended everything below it, and don’t just own everything itself — you become economy itself. Good job. [Unlock it to finish the game!]"
}

TOOLTIPS["Ascend"] = (
    "Resets your upgrades. Adds Ascension Points per upgrade level.\n"
    "1 Ascension Point = +0.01x Ascension Power"
)

TOOLTIPS["Transcend"] = (
    "Resets your upgrades, Ascension Points, and Ascension Power.\n"
    "1 Ascension Point = +0.001TP"
)

NUMBER_FORMAT_TOOLTIP = (
    "K = Thousand\n"
    "M = Million\n"
    "B = Billion\n"
    "T = Trillion\n"
    "q = Quadrillion\n"
    "Q = Quintillion\n"
    "s = Sextillion\n"
    "S = Septillion\n"
    "O = Octillion\n"
    "N = Nonillion\n"
    "d = Decillion\n"
    "U = Undecillion\n"
    "D = Duodecillion\n"
    "! = Tredecillion\n"
    "@ = Quattuordecillion\n"
    "# = Quindecillion\n"
    "$ = Sexdecillion\n"
    "% = Septendecillion\n"
    "^ = Octodecillion\n"
    "& = Novemdecillion\n"
    "* = Vigintillion\n"
    "e+XX = Scientific Notation"
)


# Group into pages (e.g., 24 per page)
def group_into_pages(flat_list, per_page=24):
    return [flat_list[i:i + per_page] for i in range(0, len(flat_list), per_page)]

TIER_RPS = group_into_pages(TIER_RPS_FLAT)
TIER_COSTS = group_into_pages([rps * 50 for rps in TIER_RPS_FLAT])
TIER_NAMES = group_into_pages(TIER_NAMES_FLAT)

# Format large numbers

def format_number(n):
    if n >= 1e68:
        return f"{n:.3e}"
    elif n >= 1e65:
        return f"{n/1e63:,.0f}*"
    elif n >= 1e62:
        return f"{n/1e60:,.0f}&"
    elif n >= 1e59:
        return f"{n/1e57:,.0f}^"
    elif n >= 1e56:
        return f"{n/1e54:,.0f}%"
    elif n >= 1e53:
        return f"{n/1e51:,.0f}$"
    elif n >= 1e50:
        return f"{n/1e48:,.0f}#"
    elif n >= 1e47:
        return f"{n/1e45:,.0f}@"
    elif n >= 1e44:
        return f"{n/1e42:,.0f}!"
    elif n >= 1e41:
        return f"{n/1e39:,.0f}D"
    elif n >= 1e38:
        return f"{n/1e36:,.0f}U"
    elif n >= 1e35:
        return f"{n/1e33:,.0f}d"
    elif n >= 1e32:
        return f"{n/1e30:,.0f}N"
    elif n >= 1e29:
        return f"{n/1e27:,.0f}O"
    elif n >= 1e26:
        return f"{n/1e24:,.0f}S"
    elif n >= 1e23:
        return f"{n/1e21:,.0f}s"
    elif n >= 1e20:
        return f"{n/1e18:,.0f}Q"
    elif n >= 1e17:
        return f"{n/1e15:,.0f}q"
    elif n >= 1e14:
        return f"{n/1e12:,.0f}T"
    elif n >= 1e11:
        return f"{n/1e9:,.0f}B"
    elif n >= 1e8:
        return f"{n/1e6:,.0f}M"
    elif n >= 1e5:
        return f"{n/1e3:,.0f}K"
    elif n >= 1e2:
        return f"{n:,.0f}"
    else:
        return f"{n:,.2f}"

class FloatingText:
    def __init__(self, x, y, text, color=(0, 100, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.alpha = 255
        self.lifetime = 1.0  # seconds
        self.creation_time = time.time()

    def update(self):
        elapsed = time.time() - self.creation_time
        if elapsed > self.lifetime:
            return False
        self.y -= 0.5  # Move upward slowly
        self.alpha = max(0, 255 - int((elapsed / self.lifetime) * 255))
        return True

    def draw(self, screen, font):
        surface = font.render(self.text, True, self.color)
        surface.set_alpha(self.alpha)
        screen.blit(surface, (self.x, self.y))

class UpgradeButton:
    def __init__(self, x, y, width, height, index, rps_base, cost_base, name):
        self.rect = pygame.Rect(x, y, width, height)
        self.index = index
        self.rps_base = rps_base
        self.cost_base = cost_base
        self.level = 0
        self.name = name  # unique name for this tier
        self.parent_game = None  # set by IdleGame before use

    def is_unlocked(self, game):
        if self.index == 0:
            return True
        elif self.index % 24 == 0:
            prev_tier_index = self.index - 1
            if 0 <= prev_tier_index < len(game.all_buttons):
                return game.all_buttons[prev_tier_index].level > 0
            return False
        else:
            return game.all_buttons[self.index - 1].level > 0

    def get_cost(self):
        return self.cost_base * (1.15 ** self.level)

    def get_rps(self):
        rps = self.rps_base * self.level
        if self.level >= 200:
            bonus = 1
            capped_level = min(self.level, 8000)
            bonus *= 4
            bonus *= 4 ** ((capped_level - 200) // 25)
            bonus *= 100 ** ((capped_level - 200) // 1000)
            rps *= bonus
        rps *= self.get_prestige_multiplier()
        return rps

    def get_prestige_multiplier(self):
        return self.parent_game.prestige_multiplier if self.parent_game else 1.0

    def draw(self, screen, font, resources, game):
        unlocked = self.is_unlocked(game)
        affordable = resources >= self.get_cost()
        mouse_hover = self.rect.collidepoint(pygame.mouse.get_pos())

        color = GRAY if not unlocked else GREEN if affordable else RED
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Render basic info
        name_text = f"{self.name}"
        level_text = f"Lv {self.level}"
        rps_text = f"${format_number(self.get_rps()) if self.level > 0 else format_number(self.rps_base*self.get_prestige_multiplier())}/s"
        cost_text = f"Cost: ${format_number(self.get_cost())}"

        screen.blit(font.render(name_text, True, BLACK), (self.rect.x + 5, self.rect.y + 3))
        screen.blit(font.render(level_text, True, BLACK), (self.rect.x + 5, self.rect.y + 25))
        screen.blit(font.render(rps_text, True, BLACK), (self.rect.x + 175, self.rect.y + 3))
        screen.blit(font.render(cost_text, True, BLACK), (self.rect.x + 120, self.rect.y + 25))

        # Draw tooltip if hovered
        if mouse_hover:
            tooltip = TOOLTIPS.get(self.name, "")
            if tooltip:
                self.draw_tooltip(screen, tooltip, font)


    def handle_event(self, event, game, _):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.is_unlocked(game):
                cost = self.get_cost()
                if game.resource >= cost:
                    multiplier = game.get_purchase_multiplier()
                    for _ in range(multiplier):
                        cost = self.get_cost()
                        if game.resource >= cost:
                            game.resource -= cost
                            prev_rps = self.get_rps()
                            self.level += 1
                            new_rps = self.get_rps()
                            game.total_rps += (new_rps - prev_rps)
                        else:
                            break

    def draw_tooltip(self, screen, text, font):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            if font.size(line + word)[0] < 300:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        width = 320
        height = 20 + 20 * len(lines)
        x, y = pygame.mouse.get_pos()
        x = min(x + 10, SCREEN_WIDTH - width - 10)
        y = min(y + 10, SCREEN_HEIGHT - height - 10)

        tooltip_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (255, 255, 200), tooltip_rect)
        pygame.draw.rect(screen, BLACK, tooltip_rect, 2)

        for i, line in enumerate(lines):
            rendered = font.render(line.strip(), True, BLACK)
            screen.blit(rendered, (x + 5, y + 5 + i * 20))



class IdleGame:
    SAVE_FILE = "save.json"

    def __init__(self):
        # --- Purchase and pagination setup ---
        self.purchase_multipliers = [1, 10, 25, 100, 1000]
        self.current_multiplier_index = 0
        self.multiplier_button = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 190, 160, 35)

        pygame.display.set_caption("Investment Simulator")
        self.current_page = 0
        self.total_pages = len(TIER_RPS)
        self.next_button = pygame.Rect(SCREEN_WIDTH - 150, 30, 120, 40)
        self.prev_button = pygame.Rect(SCREEN_WIDTH - 300, 30, 120, 40)

        # --- Pygame setup ---
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 22)
        self.big_font = pygame.font.SysFont(None, 36)

        # --- Core game variables ---
        self.prestige_points = 0
        self.prestige_multiplier = 1.0
        self.super_multiplier = 1.0      # NEW: cumulative super multiplier
        self.total_rps = 0.0
        self.resource = 0.0
        self.last_update = time.time()
        self.floating_texts = []
        self.resource_info_rect = pygame.Rect(50, 30, 50, 20)

        # --- All upgrade buttons and the subset for the current page ---
        self.all_buttons = self.create_all_buttons()
        self.buttons = self.get_current_page_buttons()

        # --- Click area (bottom panel) ---
        self.click_rect = pygame.Rect(0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80)

        # --- Prestige buttons ---
        self.prestige_button = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 140, 160, 40)
        self.super_prestige_button = pygame.Rect(SCREEN_WIDTH - 380, SCREEN_HEIGHT - 190, 160, 40)

        # --- Backgrounds ---

        self.backgrounds = {
            "default": pygame.image.load("piggy_bank.jpg").convert(),
            "mansion": pygame.image.load("mansion.jpg").convert(),
            "earth": pygame.image.load("earth.jpg").convert(),
            "nebula": pygame.image.load("nebula.jpg").convert(),
            "galaxy": pygame.image.load("galaxy.jpg").convert(),
            "supercluster": pygame.image.load("supercluster.jpeg").convert(),
            "black": pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        }
        self.backgrounds["black"].fill((0, 0, 0))  # solid black

        self.current_background = self.backgrounds["default"]
        self.text_color = BLACK

        # --- Arc Titles ---
        
        self.arc_titles = [
            (0, "Personal Items"),
            (10, "Luxuries"),
            (16, "Power"),
            (23, "Solar Neighborhood"),
            (33, "Galactic Structures"),
            (43, "Beyond Comprehension"),
            (47, "The Singularity")
        ]
        self.current_arc_title = "Arc I: Personal Items"
        self.arc_flash_time = 0

        # Load saved state (if any), including offline gain:
        self.load_game()

    def create_all_buttons(self):
        buttons = []
        for page_idx, (rps_page, cost_page, name_page) in enumerate(zip(TIER_RPS, TIER_COSTS, TIER_NAMES)):
            for i in range(len(rps_page)):
                x = 50 + (i % 3) * 300
                y = 120 + (i // 3) * 60
                global_index = i + page_idx * 24
                name = name_page[i] if i < len(name_page) else f"Tier {global_index + 1}"
                btn = UpgradeButton(x, y, 280, 50, global_index, rps_page[i], cost_page[i], name)
                btn.parent_game = self
                buttons.append(btn)
        return buttons

    def get_current_page_buttons(self):
        start = self.current_page * 24
        end = start + 24
        for btn in self.all_buttons[start:end]:
            btn.parent_game = self
        return self.all_buttons[start:end]

    def get_purchase_multiplier(self):
        return self.purchase_multipliers[self.current_multiplier_index]

    def change_page(self, direction):
        new_page = self.current_page + direction
        if 0 <= new_page < self.total_pages:
            self.current_page = new_page
            self.buttons = self.get_current_page_buttons()

    def get_total_rps(self):
        return self.total_rps

    def calculate_prestige_gain(self):
        total_levels = sum(button.level for button in self.all_buttons)
        return int(total_levels * 1)

    def can_prestige(self):
        # Unlock prestige at Tier 33 (index 32)
        return self.all_buttons[32].level > 0

    def apply_prestige(self):
        if not self.can_prestige():
            return
        base_gain = self.calculate_prestige_gain()
        if base_gain == 0:
            return
        # Apply super multiplier to prestige gain
        gained = int(base_gain * self.super_multiplier)
        self.prestige_points += gained
        self.prestige_multiplier = 1.0 + self.prestige_points * 0.01

        # Reset all tiers and resources
        for button in self.all_buttons:
            button.level = 0
        self.total_rps = 0.0
        self.resource = 0.0

    def can_super_prestige(self):
        # Can only super prestige if the player has at least 1 prestige point
        return self.prestige_points >= 1

    def apply_super_prestige(self):
        if not self.can_super_prestige():
            return
        # Each prestige point gives 0.001 to super multiplier
        self.super_multiplier += self.prestige_points * 0.001

        # Reset prestige points and multiplier
        self.prestige_points = 0
        self.prestige_multiplier = 1.0

        # Also fully reset the game state (all tiers, resources, RPS)
        for button in self.all_buttons:
            button.level = 0
        self.total_rps = 0.0
        self.resource = 0.0
    
    def update_background(self):
        previous_title = self.current_arc_title

        if self.all_buttons[47].level > 0:
            self.current_background = self.backgrounds["black"]
            self.text_color = WHITE
            self.current_arc_title = "Arc VII: The Singularity"
        elif self.all_buttons[43].level > 0:
            self.current_background = self.backgrounds["supercluster"]
            self.text_color = WHITE
            self.current_arc_title = "Arc VI: Beyond Comprehension"
        elif self.all_buttons[33].level > 0:
            self.current_background = self.backgrounds["galaxy"]
            self.text_color = WHITE
            self.current_arc_title = "Arc V: Galactic Structures"
        elif self.all_buttons[23].level > 0:
            self.current_background = self.backgrounds["nebula"]
            self.text_color = WHITE
            self.current_arc_title = "Arc IV: Solar Neighborhood"
        elif self.all_buttons[16].level > 0:
            self.current_background = self.backgrounds["earth"]
            self.text_color = WHITE
            self.current_arc_title = "Arc III: Power"
        elif self.all_buttons[10].level > 0:
            self.current_background = self.backgrounds["mansion"]
            self.text_color = BLACK
            self.current_arc_title = "Arc II: Luxuries"
        else:
            self.current_background = self.backgrounds["default"]
            self.text_color = BLACK
            self.current_arc_title = "Arc I: Personal Items"

        # Trigger arc title flash on change
        if self.current_arc_title != previous_title:
            self.arc_flash_time = time.time()



    def update(self):
        current_time = time.time()
        elapsed = current_time - self.last_update
        self.resource += self.total_rps * elapsed
        self.last_update = current_time
        # Remove expired texts
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]
        self.update_background()

    def draw_multiline_tooltip(self, screen, text, font, color):
        lines = text.split("\n")
        width = 220
        height = 20 + 20 * len(lines)
        x, y = pygame.mouse.get_pos()
        x = min(x + 10, SCREEN_WIDTH - width - 10)
        y = min(y + 10, SCREEN_HEIGHT - height - 10)

        tooltip_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (255, 255, 200), tooltip_rect)
        pygame.draw.rect(screen, BLACK, tooltip_rect, 2)

        for i, line in enumerate(lines):
            rendered = font.render(line.strip(), True, color)
            screen.blit(rendered, (x + 5, y + 5 + i * 20))

    def draw(self):
        self.screen.blit(pygame.transform.scale(self.current_background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
        self.hovered_button = None
        mouse_pos = pygame.mouse.get_pos()

        # Resource display
        res_text = self.big_font.render(f"${format_number(self.resource)}", True, self.text_color)
        rps_text = self.font.render(f"${format_number(self.get_total_rps())}/s", True, self.text_color)
        self.screen.blit(res_text, (50, 30))
        self.screen.blit(rps_text, (50, 70))

        # Prestige displays
        points_text = self.font.render(f"Ascension Points: {format_number(self.prestige_points)} Points", True, self.text_color)
        prestige_mult_text = self.font.render(f"Ascension Power: {format_number(self.prestige_multiplier)}x", True, self.text_color)
        super_mult_text = self.font.render(f"Transcendent Power: {format_number(self.super_multiplier)}TP", True, self.text_color)
        self.screen.blit(points_text, (50, 85))
        self.screen.blit(prestige_mult_text, (50, 100))
        self.screen.blit(super_mult_text, (300, 70))

        # Page navigation UI
        pygame.draw.rect(self.screen, GRAY, self.next_button)
        pygame.draw.rect(self.screen, GRAY, self.prev_button)
        pygame.draw.rect(self.screen, BLACK, self.next_button, 2)
        pygame.draw.rect(self.screen, BLACK, self.prev_button, 2)

        next_text = self.font.render("Next Page", True, BLACK)
        prev_text = self.font.render("Prev Page", True, BLACK)
        page_text = self.font.render(f"Page {self.current_page + 1}/{self.total_pages}", True, self.text_color)

        self.screen.blit(next_text, (self.next_button.x + 10, self.next_button.y + 10))
        self.screen.blit(prev_text, (self.prev_button.x + 10, self.prev_button.y + 10))
        self.screen.blit(page_text, (SCREEN_WIDTH // 2 - 40, 30))

        # Draw upgrade buttons
        for button in self.buttons:
            button.draw(self.screen, self.font, self.resource, self)
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                self.hovered_button = button
            # Check if hovering over Ascend or Transcend buttons
            if self.prestige_button.collidepoint(mouse_pos):
                self.hovered_button = "Ascend"
            elif self.super_prestige_button.collidepoint(mouse_pos):
                self.hovered_button = "Transcend"
                

        # Draw click panel
        pygame.draw.rect(self.screen, (200, 230, 255), self.click_rect)
        pygame.draw.rect(self.screen, BLACK, self.click_rect, 2)

        click_value = 0.01
        if self.all_buttons[0].level > 0:
            click_value += self.get_total_rps() * 0.1

        click_text = self.big_font.render("CLICK HERE TO EARN", True, BLACK)
        click_info = self.font.render(
            f"Click Value: ${format_number(click_value)} ($0.01 + 10% RPS)", True, BLACK
        )
        text_rect = click_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 55))
        info_rect = click_info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 25))
        self.screen.blit(click_text, text_rect)
        self.screen.blit(click_info, info_rect)

        # Prestige button
        pygame.draw.rect(self.screen, RED, self.prestige_button)
        pygame.draw.rect(self.screen, BLACK, self.prestige_button, 2)
        prestige_text = self.font.render("Ascend", True, BLACK)
        gain = self.calculate_prestige_gain() if self.can_prestige() else 0
        hint_text = self.font.render(f"+{format_number(int(gain * self.super_multiplier))} Points", True, BLACK)
        self.screen.blit(prestige_text, (self.prestige_button.x + 10, self.prestige_button.y + 5))
        self.screen.blit(hint_text, (self.prestige_button.x + 10, self.prestige_button.y + 22))

        # Super Prestige button
        pygame.draw.rect(self.screen, (150, 50, 150), self.super_prestige_button)
        pygame.draw.rect(self.screen, BLACK, self.super_prestige_button, 2)
        super_text = self.font.render("Transcend", True, BLACK)
        super_hint = self.font.render(f"+{format_number(self.prestige_points * 0.001)}TP", True, BLACK)
        self.screen.blit(super_text, (self.super_prestige_button.x + 5, self.super_prestige_button.y + 5))
        self.screen.blit(super_hint, (self.super_prestige_button.x + 5, self.super_prestige_button.y + 22))

        # Multiplier button (x1, x10, x25, etc.)
        pygame.draw.rect(self.screen, (200, 200, 255), self.multiplier_button)
        pygame.draw.rect(self.screen, BLACK, self.multiplier_button, 2)
        mult_text = self.font.render(f"Buy x{self.get_purchase_multiplier()}", True, BLACK)
        self.screen.blit(mult_text, (self.multiplier_button.x + 25, self.multiplier_button.y + 8))

        if isinstance(self.hovered_button, UpgradeButton):
            tooltip = TOOLTIPS.get(self.hovered_button.name, "")
            if tooltip:
                self.hovered_button.draw_tooltip(self.screen, tooltip, self.font)
        elif isinstance(self.hovered_button, str):
            tooltip = TOOLTIPS.get(self.hovered_button, "")
            if tooltip:
                # Use a temporary dummy UpgradeButton to draw the tooltip
                dummy_button = UpgradeButton(0, 0, 0, 0, -1, 0, 0, self.hovered_button)
                dummy_button.draw_tooltip(self.screen, tooltip, self.font)

        for ft in self.floating_texts:
            ft.draw(self.screen, self.font)

        # Draw arc title if recently changed
        if time.time() - self.arc_flash_time < 3:  # display for 3 seconds
            alpha = 255
            elapsed = time.time() - self.arc_flash_time
            if elapsed > 2.5:
                alpha = int(255 * (1 - (elapsed - 2.5) / 0.5))  # fade out last 0.5s

            arc_surface = self.big_font.render(self.current_arc_title, True, self.text_color)
            arc_surface.set_alpha(alpha)
            arc_rect = arc_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            self.screen.blit(arc_surface, arc_rect)

        if self.resource_info_rect.collidepoint(pygame.mouse.get_pos()):
            self.draw_multiline_tooltip(self.screen, NUMBER_FORMAT_TOOLTIP, self.font, self.text_color)


        pygame.display.flip()

    def handle_click(self):
        click_value = 0.01
        if self.all_buttons[0].level > 0:
            click_value += self.get_total_rps() * 0.1

        self.resource += click_value

        # Create visual feedback text
        self.floating_texts.append(FloatingText(
            SCREEN_WIDTH // 2 - 20,
            SCREEN_HEIGHT - 90,
            f"+${format_number(click_value)}"
        ))

    # —————— JSON SAVE/LOAD WITH OFFLINE GAIN ——————

    def save_game(self, filename=None):
        """
        Save:
          - resource
          - total_rps
          - prestige_points, prestige_multiplier
          - super_multiplier
          - current page & multiplier index
          - every button’s level
          - current timestamp ("save_time")
        """
        if filename is None:
            filename = self.SAVE_FILE

        data = {
            "resource": self.resource,
            "total_rps": self.total_rps,
            "prestige_points": self.prestige_points,
            "prestige_multiplier": self.prestige_multiplier,
            "super_multiplier": self.super_multiplier,
            "current_multiplier_index": self.current_multiplier_index,
            "current_page": self.current_page,
            "button_levels": [button.level for button in self.all_buttons],
            "save_time": time.time()
        }
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"Game saved to {filename}")
        except Exception as e:
            print("Error saving game:", e)

    def load_game(self, filename=None):
        """
        Load and immediately award offline gains. Steps:
        1. Read JSON. If missing, just return.
        2. Parse saved resource, saved_rps, and saved_time.
        3. Compute elapsed = now - saved_time, then break that into days, hours, minutes, seconds.
        4. Add offline_gain = saved_rps * elapsed to resource.
        5. Restore button levels, prestige, super multiplier, then recompute total_rps.
        6. Print exactly how many days/hours/minutes/seconds the game was offline.
        """
        if filename is None:
            filename = self.SAVE_FILE

        if not os.path.exists(filename):
            return

        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except Exception as e:
            print("Error loading save file:", e)
            return

        # 1) Extract saved scalars and arrays
        saved_resource = data.get("resource", 0.0)
        saved_rps = data.get("total_rps", 0.0)
        saved_prestige_points = data.get("prestige_points", 0)
        saved_prestige_multiplier = data.get("prestige_multiplier", 1.0)
        saved_super_multiplier = data.get("super_multiplier", 1.0)
        saved_multiplier_index = data.get("current_multiplier_index", 0)
        saved_page = data.get("current_page", 0)
        saved_levels = data.get("button_levels", [])
        saved_time = data.get("save_time", time.time())

        # 2) Compute offline gain
        now = time.time()
        elapsed = max(0.0, now - saved_time)

        # Break elapsed seconds into days, hours, minutes, seconds:
        days = int(elapsed // 86400)
        hours = int((elapsed % 86400) // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)

        offline_gain = saved_rps * elapsed

        # 3) Apply values to self
        self.resource = saved_resource + offline_gain
        self.prestige_points = saved_prestige_points
        self.prestige_multiplier = saved_prestige_multiplier
        self.super_multiplier = saved_super_multiplier
        self.current_multiplier_index = saved_multiplier_index
        self.current_page = saved_page

        # 4) Restore button levels if they match
        if len(saved_levels) == len(self.all_buttons):
            for button, lvl in zip(self.all_buttons, saved_levels):
                button.level = lvl
            # Recompute total_rps now that levels are back
            self.total_rps = sum(btn.get_rps() for btn in self.all_buttons)
        else:
            print("Saved button count does not match current button count; skipping level restore.")
            self.total_rps = 0.0

        # 5) Finally, make sure we show the correct page
        self.buttons = self.get_current_page_buttons()

        # 6) Print breakdown
        print(
            f"Loaded save: +${format_number(offline_gain)} from "
            f"{days}d {hours}h {minutes}m {seconds}s offline."
        )

    # —————— END JSON SECTION ——————

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Save on quit
                    self.save_game()
                    running = False

                # Forward events to each button
                for button in self.buttons:
                    button.parent_game = self
                    button.handle_event(event, self, self)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.click_rect.collidepoint(event.pos):
                        self.handle_click()
                    elif self.next_button.collidepoint(event.pos):
                        self.change_page(1)
                    elif self.prev_button.collidepoint(event.pos):
                        self.change_page(-1)
                    elif self.prestige_button.collidepoint(event.pos):
                        self.apply_prestige()
                    elif self.super_prestige_button.collidepoint(event.pos):
                        self.apply_super_prestige()
                    elif self.multiplier_button.collidepoint(event.pos):
                        self.current_multiplier_index = (self.current_multiplier_index + 1) % len(self.purchase_multipliers)

            self.update()
            self.draw()

        pygame.quit()
        sys.exit()


# Run the game
if __name__ == "__main__":
    pygame.init()
    game = IdleGame()
    game.run()
