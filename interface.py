import pygame
import subprocess
import sys

# Function to read text from file
def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def run_script(script_name):
    # Execute the script using subprocess
    print("run ", script_name)
    subprocess.Popen([sys.executable, f'{script_name}.py'])

def main():
    pygame.init()
    
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), flags=pygame.RESIZABLE)
    
    # Set up colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    TURQUOISE = (0, 153, 153)
    
    # Set up font
    font = pygame.font.Font(None, 24)
    font2 = pygame.font.Font(None, 42)
    
    clock = pygame.time.Clock()
    
    running = True
    write_txt = False
    clicked1 = False
    clicked2 = False
    clicked3 = False
    while running:
        clicked1 = False
        clicked2 = False
        clicked3 = False
        for event in pygame.event.get():
            # Button positions and sizes
            size = pygame.display.get_window_size()
            height = size[1]*(1/10)
            width = size[0]*(2/3)
            header = pygame.Rect(0, 0, size[0], height*(3/2))
            button1_rect = pygame.Rect(size[0]/2 - width/2, height*3, width, height)
            button2_rect = pygame.Rect(size[0]/2 - width/2, height*5, width, height)
            button3_rect = pygame.Rect(size[0]/2 - width/2, height*7, width, height)
            
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button1_rect.collidepoint(x, y):
                    run_script('code/check_completed')
                    clicked1 = True
                elif button2_rect.collidepoint(x, y):
                    run_script('code/create_files_and_convert')
                    clicked2 = True
                elif button3_rect.collidepoint(x, y):
                    run_script('code/SlurmIter')
                    clicked3 = True
                    
            #elif event.type == pygame.MOUSEBUTTONUP:
              #clicked1 = False
              #clicked2 = False
              #clicked3 = False
                    
        screen.fill(WHITE)  # Fill the screen with black color
        
        
        button_scale1 = 1.1 if clicked1 else 1.0
        button_scale2 = 1.1 if clicked2 else 1.0
        button_scale3 = 1.1 if clicked3 else 1.0
        button1_scaled_rect = button1_rect.inflate((width * button_scale1 - width, height * button_scale1 - height))
        button2_scaled_rect = button2_rect.inflate((width * button_scale2 - width, height * button_scale2 - height))
        button3_scaled_rect = button3_rect.inflate((width * button_scale3 - width, height * button_scale3 - height))
        
        
        pygame.draw.rect(screen, TURQUOISE, header)
        pygame.draw.rect(screen, TURQUOISE, button1_scaled_rect)
        pygame.draw.rect(screen, TURQUOISE, button2_scaled_rect)
        pygame.draw.rect(screen, TURQUOISE, button3_scaled_rect)
        
        button1_center = button1_scaled_rect.center
        button2_center = button2_scaled_rect.center
        button3_center = button3_scaled_rect.center
        header_center = header.center
        
        
        # Draw buttons and text
        button1_text = font.render("Check study state", False, WHITE)
        button2_text = font.render("Conversion and study creation", False, WHITE)
        button3_text = font.render("Launch analysis", False, WHITE)
        header_text = font2.render("Graphic Interface", False, WHITE)
        
        
        button1_text_pos = button1_text.get_rect(center=button1_center)
        button2_text_pos = button2_text.get_rect(center=button2_center)
        button3_text_pos = button3_text.get_rect(center=button3_center)
        header_text_pos = header_text.get_rect(center=header_center)
        
        
        screen.blit(button1_text, button1_text_pos)
        screen.blit(button2_text, button2_text_pos)
        screen.blit(button3_text, button3_text_pos)
        screen.blit(header_text, header_text_pos)
        
        
        pygame.display.flip()
        
        clock.tick(60)  # Limit the frame rate to 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()
