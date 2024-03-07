import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion :
    """Class to manage game assets and behaviours"""

    def __init__(self):
        """intitialize the game """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self) #self is the ai_game object
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet() 


    def run_game(self):
        
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
    
    def _check_events(self):
        """Respond to keypresses and mouse clicks"""
        #watch for keyboard and mouse events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self,event):
        """ Responds to key presses """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:    
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            #enter q to exit the game
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """ Responds to key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        """Create the fleet of aliens"""
        # create an alien and find the no of aliens in a row
        # spacing between each alien is to one alien width
        alien = Alien(self)
        alien_width , alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows that fit inside the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_of_rows = available_space_y // (2 * alien_height)


        # Create the first fleet of aliens

        for row_number in range(number_of_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _check_fleet_edges(self):
        """ Respond appropriately if any aliens have reached an edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the field direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self,alien_number,row_number):
        #create an alien and place it in the row
            alien = Alien(self)
            alien_width,alien_height = alien.rect.size
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            self.aliens.add(alien)

    def _update_aliens(self):
        """ Check if the fleet is at the edge and then update the positions of the aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullet group"""
        if len(self.bullets) < self.settings.bullets_allowed :
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _update_bullets(self):
        """ update the position of the bullets and get rid of old bullets """
        self.bullets.update()
        # get rid of bullets that disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                #even == 0 works coordinate system has (0,0)at the top left corner
                self.bullets.remove(bullet)

        # check for any bullets that hit alien, if so, then get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

    def _update_screen(self):
        """Update images on the screen and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible creating the illusion of smooth movement
        pygame.display.flip()

if __name__ == '__main__':
    #Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()

