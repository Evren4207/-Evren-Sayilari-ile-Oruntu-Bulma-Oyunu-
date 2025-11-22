import pygame
import random
import sys

# --- Proje Kural Fonksiyonları ---

def calculate_pattern_value(number):
    """Verilen bir sayıyı birler basamağı ve geri kalan kısım olarak ayırıp toplar."""
    last_digit = number % 10
    remaining_part = number // 10
    return remaining_part + last_digit

PRIMES_ENDING_IN_ONE = [11, 31, 41, 61, 71, 101, 131, 151, 181, 191]

def generate_question():
    """Yeni bir soru ve doğru cevabı üretir."""
    chosen_prime = random.choice(PRIMES_ENDING_IN_ONE)
    multiplier = random.randint(2, 25)
    number_to_ask = chosen_prime * multiplier
    correct_answer = calculate_pattern_value(number_to_ask)
    
    question_text = f"Soru: '{chosen_prime}' asalının {multiplier}. katı olan '{number_to_ask}' için değer nedir?"
    return {"text": question_text, "answer": correct_answer, "number": number_to_ask}

# --- Pygame Ayarları ---
pygame.init()
pygame.font.init()

# Ekran Ayarları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Evren Sayıları İle Örüntü Oyunu")

# Renkler
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (30, 30, 30)
COLOR_BLUE = (0, 120, 255)
COLOR_GREEN = (40, 167, 69)
COLOR_RED = (220, 53, 69)
COLOR_GREY = (100, 100, 100)
COLOR_LIGHT_GREY = (200, 200, 200) # Boş can rengi

# Yazı Tipleri
try:
    font_large = pygame.font.Font(None, 54) 
    font_medium = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
except:
    font_large = pygame.font.SysFont('Arial', 54)
    font_medium = pygame.font.SysFont('Arial', 32)
    font_small = pygame.font.SysFont('Arial', 24)


def draw_text(text, font, color, surface, x, y, center=False):
    """Ekrana yazı yazmak için yardımcı fonksiyon"""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# --- Kaynakları Yükle (Sadece Kalp) ---
heart_image = None
try:
    # heart.png dosyasının aynı dizinde olduğunu varsayıyoruz
    heart_image = pygame.image.load("heart.png").convert_alpha() 
    heart_image = pygame.transform.scale(heart_image, (30, 30)) # Kalp boyutunu ayarla
except pygame.error:
    # Resim yüklenemezse None olarak kalır ve uyarı verir
    print("UYARI: 'heart.png' dosyası yüklenemedi. Can barı daire olarak gösterilecektir.")


# --- Can Barı Çizme Fonksiyonu (Kalpli / Dairesel Yedek) ---
def draw_health_bar(surface, current_health, max_health, heart_img):
    """Sağ üst köşeye canları çizer (kalp resmi olarak, resim yoksa daire olarak)"""
    if heart_img is None: 
        # Resim yüklenemediyse Daire çizimi (Yedek)
        radius = 12
        spacing = 10
        start_x = SCREEN_WIDTH - 30 
        y_pos = 35 
        for i in range(max_health):
            x = start_x - i * (radius * 2 + spacing)
            if i < current_health:
                pygame.draw.circle(surface, COLOR_RED, (x, y_pos), radius)
            else:
                pygame.draw.circle(surface, COLOR_LIGHT_GREY, (x, y_pos), radius)
                pygame.draw.circle(surface, COLOR_GREY, (x, y_pos), radius, 2)
        return

    # Resim yüklenebildiyse Kalp çizimi
    heart_width = heart_img.get_width()
    spacing = 5 # Kalpler arası boşluk
    start_x = SCREEN_WIDTH - heart_width - 15 # Sağdan boşluk
    y_pos = 15 # Yukarıdan boşluk
    
    for i in range(max_health):
        x = start_x - i * (heart_width + spacing)
        
        # Sadece dolu kalpleri çiziyoruz
        if i < current_health:
            surface.blit(heart_img, (x, y_pos))


# --- Buton Tanımlamaları ---
BUTTON_WIDTH = 220
BUTTON_HEIGHT = 70
button_start_rect = pygame.Rect(
    (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2), 
    250, 
    BUTTON_WIDTH, 
    BUTTON_HEIGHT
)
button_quit_rect = pygame.Rect(
    (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2), 
    350, 
    BUTTON_WIDTH, 
    BUTTON_HEIGHT
)

# YENİ BUTON TANIMI: OYUN EKRANINDAN MENÜYE DÖNME BUTONU
button_to_menu_rect = pygame.Rect(
    (SCREEN_WIDTH // 2) - (BUTTON_WIDTH // 2), # Merkezde
    480, # Sonuç mesajının altına
    BUTTON_WIDTH, 
    BUTTON_HEIGHT - 20 # Biraz daha küçük
)


# --- Oyun Değişkenleri ---
clock = pygame.time.Clock()
running = True
game_state = "MENU"  

# Oyun değişkenleri (Oyuna başlandığında sıfırlanır)
user_input_text = ""
current_question = generate_question()
result_message = ""
result_color = COLOR_BLACK
player_health = 3 
MAX_HEALTH = 3    


# --- Ana Oyun Döngüsü ---

while running:
    
    # 1. Olay (Event) Yönetimi
    
    if game_state == "MENU":
        # --- MENÜ EKRANI ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                
                if button_start_rect.collidepoint(mouse_pos):
                    game_state = "GAME" 
                    user_input_text = ""
                    current_question = generate_question()
                    result_message = ""
                    player_health = MAX_HEALTH 
                
                if button_quit_rect.collidepoint(mouse_pos):
                    running = False 
                    pygame.quit()
                    sys.exit()

        # Ekranı Çiz (Menü için)
        screen.fill(COLOR_WHITE)
        draw_text("Evren Sayıları İle Örüntü Oyunu", font_large, COLOR_BLUE, screen, SCREEN_WIDTH // 2, 100, center=True)
        pygame.draw.rect(screen, COLOR_GREEN, button_start_rect, border_radius=10)
        draw_text("Başla", font_medium, COLOR_WHITE, screen, button_start_rect.centerx, button_start_rect.centery, center=True)
        pygame.draw.rect(screen, COLOR_RED, button_quit_rect, border_radius=10)
        draw_text("Oyundan Çık", font_medium, COLOR_WHITE, screen, button_quit_rect.centerx, button_quit_rect.centery, center=True)

    
    elif game_state == "GAME":
        # --- OYUN EKRANI ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN: # YENİ: Buton Tıklama Kontrolü
                mouse_pos = event.pos
                if button_to_menu_rect.collidepoint(mouse_pos):
                    game_state = "MENU" # Lobbye yönlendir
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: 
                    if user_input_text: 
                        try:
                            user_answer = int(user_input_text)
                            correct_answer = current_question["answer"]
                            
                            if user_answer == correct_answer:
                                
                                if player_health < MAX_HEALTH:
                                    result_message = f"🎉 Tebrikler! Doğru cevap {correct_answer} idi. +1 Can"
                                else:
                                    result_message = f"🎉 Tebrikler! Doğru cevap {correct_answer} idi."
                                    
                                result_color = COLOR_GREEN
                                player_health = min(player_health + 1, MAX_HEALTH)
                                
                                current_question = generate_question()
                                user_input_text = ""

                            else: # Yanlış cevap
                                player_health -= 1 
                                result_message = f"Maalesef... Doğru cevap {correct_answer} olacaktı. -1 Can 😔"
                                result_color = COLOR_RED
                                
                                if player_health <= 0:
                                    game_state = "GAME_OVER" 
                                else:
                                    current_question = generate_question()
                                    user_input_text = ""
                            
                        except ValueError:
                            result_message = "Lütfen sadece sayı girin."
                            result_color = COLOR_RED
                            user_input_text = ""

                elif event.key == pygame.K_BACKSPACE:
                    user_input_text = user_input_text[:-1] 
                
                elif event.unicode.isdigit(): 
                    user_input_text += event.unicode
                    
                elif event.key == pygame.K_ESCAPE:
                    game_state = "MENU"

        # Ekranı Çiz (Oyun için)
        screen.fill(COLOR_WHITE) 
        
        # Can Barını Kalp Resmiyle Çiz
        draw_health_bar(screen, player_health, MAX_HEALTH, heart_image)
        
        draw_text("Evren Sayıları İle Örüntü Oyunu", font_large, COLOR_BLUE, screen, SCREEN_WIDTH // 2, 50, center=True)
        draw_text("Kural: Sayının son basamağını ve kalan kısmını topla. (Örn: 124 -> 12 + 4 = 16)", 
                  font_small, COLOR_GREY, screen, SCREEN_WIDTH // 2, 110, center=True)
        draw_text(current_question["text"], font_medium, COLOR_BLACK, screen, SCREEN_WIDTH // 2, 200, center=True)
        draw_text("Cevabınız:", font_medium, COLOR_BLACK, screen, SCREEN_WIDTH // 2 - 100, 300, center=True)
        draw_text(user_input_text, font_medium, COLOR_BLUE, screen, SCREEN_WIDTH // 2 + 30, 300, center=True)
        pygame.draw.rect(screen, COLOR_BLACK, (SCREEN_WIDTH // 2 - 50, 325, 160, 4), 2) 
        draw_text(result_message, font_medium, result_color, screen, SCREEN_WIDTH // 2, 400, center=True) # Yüksekliği ayarladık (450 -> 400)
        
        # YENİ BUTON ÇİZİMİ
        pygame.draw.rect(screen, COLOR_BLUE, button_to_menu_rect, border_radius=10)
        draw_text("Menüye Dön", font_medium, COLOR_WHITE, screen, button_to_menu_rect.centerx, button_to_menu_rect.centery, center=True)
        
        draw_text("Cevaplamak için ENTER'a basın.", 
                  font_small, COLOR_GREY, screen, SCREEN_WIDTH // 2, 550, center=True)
        

    # --- OYUN BİTTİ EKRANI ---
    elif game_state == "GAME_OVER":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = "MENU"
        
        # Ekranı Çiz (Oyun Bitti için)
        screen.fill(COLOR_WHITE)
        draw_text("Oyun Bitti", font_large, COLOR_RED, screen, SCREEN_WIDTH // 2, 250, center=True)
        draw_text("Tüm canlarını kaybettin.", font_medium, COLOR_BLACK, screen, SCREEN_WIDTH // 2, 310, center=True)
        draw_text("Menüye dönmek için ENTER'a basın.", font_medium, COLOR_GREY, screen, SCREEN_WIDTH // 2, 400, center=True)


    # !!! --- SİYAH EKRAN ÇÖZÜMÜ --- !!!
    # Çizilen her şeyi ekrana yansıt
    pygame.display.flip()
    
    # Oyunu 60 FPS'e sabitle
    clock.tick(60)