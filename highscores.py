import pygame

SCORE_FILE = "scores.txt"
MAX_RECORDS = 10

_score_font = None
_title_font = None

player_name = ""
entering_name = False

def init_ui():
    global _score_font, _title_font
    _score_font = pygame.font.SysFont("consolas", 26)
    _title_font = pygame.font.SysFont("consolas", 48, bold=True)

def save_score(name, value):
    scores = load_scores()
    scores.append((name, value))
    scores.sort(key=lambda x: x[1], reverse=True)
    scores = scores[:MAX_RECORDS]

    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        for n, v in scores:
            f.write(f"{n};{v}\n")

def load_scores():
    scores = []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name, val = line.strip().split(";")
                scores.append((name, int(val)))
    except FileNotFoundError:
        pass
    return scores

def start_name_input():
    global player_name, entering_name
    if not entering_name:
        player_name = ""
        entering_name = True

def handle_event(event, score):
    global player_name, entering_name

    if not entering_name or event.type != pygame.KEYDOWN:
        return False

    if event.key == pygame.K_RETURN:
        save_score(player_name or "PLAYER", score)
        entering_name = False
        return True

    elif event.key == pygame.K_BACKSPACE:
        player_name = player_name[:-1]

    else:
        if len(player_name) < 12:
            player_name += event.unicode

    return False

def draw_name_input(surface):
    w, h = surface.get_size()

    title = _title_font.render("ENTER YOUR NAME", True, (240, 240, 240))
    name  = _score_font.render(player_name + "_", True, (255, 255, 255))

    surface.blit(title, title.get_rect(center=(w//2, h//2 + 140)))
    surface.blit(name,  name.get_rect(center=(w//2, h//2 + 190)))

def draw_highscores(surface):
    scores = load_scores()
    w = surface.get_width()
    y = 180

    title = _title_font.render("HIGHSCORES", True, (240, 240, 240))
    surface.blit(title, title.get_rect(center=(w//2, 120)))

    for i, (name, val) in enumerate(scores):
        line = _score_font.render(f"{i+1}. {name} — {val}", True, (200, 200, 200))
        surface.blit(line, (w//2 - 150, y))
        y += 30