import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        running = True
        end_message = None

        while running:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # quit application
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # key press
                elif event.type == pygame.KEYDOWN:
                    # changing themes
                    if event.key == pygame.K_t:
                        game.change_theme()
                    # reset
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                # click
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    # if clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color) ?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show methods 
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        # Only allow moves that are in piece.moves (legal moves)
                        if move in dragger.piece.moves:
                            # normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            board.set_true_en_passant(dragger.piece)
                            # sounds
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            # next turn
                            game.next_turn()
                            # check for end
                            color = game.next_player
                            if board.is_checkmate(color):
                                end_message = f"Checkmate! {color} loses. Press R to restart."
                                running = False
                            elif board.is_stalemate(color):
                                end_message = "Stalemate! Draw. Press R to restart."
                                running = False
                        else:
                            # Illegal move, do nothing (ignore)
                            pass
                    dragger.undrag_piece()

            pygame.display.update()

        # Show end message and winner animation
        if end_message:
            font = pygame.font.SysFont(None, 48)
            text = font.render(end_message, True, (255,0,0))
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, rect)
            pygame.display.update()

            # Winner animation for checkmate
            if "Checkmate" in end_message:
                winner = "white" if "black loses" in end_message else "black"
                anim_font = pygame.font.SysFont(None, 72)
                for _ in range(60):  # 60 frames ~1 second
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    screen.fill((0,0,0))
                    # Draw the end message
                    screen.blit(text, rect)
                    # Draw the winner animation
                    color = (0,255,0) if winner == "white" else (0,0,255)
                    anim_text = anim_font.render(f"{winner.upper()} WINS!", True, color)
                    anim_rect = anim_text.get_rect(center=(WIDTH//2, HEIGHT//2-80))
                    screen.blit(anim_text, anim_rect)
                    pygame.display.update()
                    pygame.time.delay(16)
                # Keep winner message on screen until user presses R or quits
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            self.__init__()
                            self.mainloop()
                            return
                    # Redraw winner message
                    screen.fill((0,0,0))
                    screen.blit(text, rect)
                    screen.blit(anim_text, anim_rect)
                    pygame.display.update()

            # Wait for R or quit
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.__init__()
                        self.mainloop()
                        return

main = Main()
main.mainloop()