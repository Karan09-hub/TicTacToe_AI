import sys
import pygame
import numpy as np
import random
import copy

from Constants import *

#SETUP
pygame.init()
Screen=pygame.display.set_mode((Width,Height))
pygame.display.set_caption("TicTacToe_AI")
Screen.fill(Bg_Color)

#BOARD CONFIGURATIONSse
class Board():
    def __init__(self):
        self.Squares=np.zeros((Rows,Cols))
        self.Empty_Sqrs=self.Squares
        self.Marked_Squares=0
    
    #AI FUNCTIONS
    def Final_State(self,show=False):
        #returns 0 if no win yet,1 if player 1 wins,2 if player 2 wins
        for row in range(Rows):
            if self.Squares[row][0]==self.Squares[row][1]==self.Squares[row][2]!=0:
                if show:
                    color=Circle_Color if self.Squares[row][0]==1 else Cross_Color
                    i_pos=(20,row*Sqsize+Sqsize//2)
                    f_pos=(Width-20,row*Sqsize+Sqsize//2) 
                    pygame.draw.line(Screen,color,i_pos,f_pos,Line_Width)
                return self.Squares[row][0]
            
        for col in range(Cols):
            if self.Squares[0][col]==self.Squares[1][col]==self.Squares[2][col]!=0:
                if show:
                    color=Circle_Color if self.Squares[0][col]==1 else Cross_Color
                    i_pos=(col*Sqsize+Sqsize//2,20)
                    f_pos=(col*Sqsize+Sqsize//2,Height-20) 
                    pygame.draw.line(Screen,color,i_pos,f_pos,Line_Width)
                return self.Squares[0][col]
            
        if self.Squares[0][0]==self.Squares[1][1]==self.Squares[2][2]!=0:
            if show:
                color=Circle_Color if self.Squares[0][0]==1 else Cross_Color
                i_pos=(20,20)
                f_pos=(Width-20,Height-20)
                pygame.draw.line(Screen,color,i_pos,f_pos,Line_Width)
            return self.Squares[1][1]
            
        if self.Squares[2][0]==self.Squares[1][1]==self.Squares[0][2]!=0:
            if show:
                color=Circle_Color if self.Squares[2][0]==1 else Cross_Color
                i_pos=(20,Height-20)
                f_pos=(Width-20,20)
                pygame.draw.line(Screen,color,i_pos,f_pos,Line_Width)
            return self.Squares[1][1]
        
        return 0
    
    def Is_Board_full(self):
        return self.Marked_Squares==9
    
    def Is_board_Empty(self):
        return self.Marked_Squares==0

    def Get_Empty_Squares(self):
        self.Empty_Sqrs=[]

        for row in range(Rows):
            for col in range(Cols):
                if(self.Is_Empty(row,col)):
                    self.Empty_Sqrs.append( (row,col) )

        return self.Empty_Sqrs
    
    #GAME FUNCTIONS
    def Mark_Sqrs(self,row,col,player):
        self.Squares[row][col]=player
        self.Marked_Squares+=1
    def Is_Empty(self,row,col):
        return self.Squares[row][col]==0

class AI():
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def Rnd_AI(self,board):
        empty_sqrs=board.Get_Empty_Squares()
        index=random.randrange(0,len(empty_sqrs))

        return empty_sqrs[index]

    def minmax(self,board,maximizing):
        case=board.Final_State()

        if case==1:
            return 1,None
        elif case==2:
            return -1,None
        elif board.Is_Board_full():
            return 0,None
        

        if maximizing:
            max_eval=-10
            best_move=None
            empty_sqrs=board.Get_Empty_Squares()

            for(row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.Mark_Sqrs(row,col,1)
                eval=self.minmax(temp_board,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)
            return max_eval,best_move
        else:
            min_eval=10
            best_move=None
            empty_sqrs=board.Get_Empty_Squares()

            for(row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.Mark_Sqrs(row,col,self.player)
                eval=self.minmax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
            return min_eval,best_move

    def eval(self,Main_board):
        if self.level==0:
            #RANDOM_AI
            eval='random'
            move=self.Rnd_AI(Main_board)
            
        else:
            #MINMAX_AI
            eval,move=self.minmax(Main_board,False)

        return move

#GAME CONFIGURATIONS
class Game:
    def __init__(self):
        self.board=Board()
        self.ai=AI()
        self.player=1 #1->circle 2->cross
        self.Game_Mode='ai'# 2 player or 1 player
        self.running=True   
        self.Show_Lines()

    def restart(self):
        self.__init__()

    def Change_GameMode(self):
        self.Game_Mode='ai' if self.Game_Mode=='pvp' else 'pvp'

    def Make_Move(self,row,col):
        self.board.Mark_Sqrs(row,col,self.player)
        self.Draw_Fig(row,col)
        self.Next_turn()


    def Show_Lines(self):
        Screen.fill( Bg_Color)
        pygame.draw.line(Screen,Line_Color,(Sqsize,0),(Sqsize,Height),Line_Width)
        pygame.draw.line(Screen,Line_Color,(Width-Sqsize,0),(Width-Sqsize,Height),Line_Width)

        pygame.draw.line(Screen,Line_Color,(0,Sqsize),(Width,Sqsize),Line_Width)
        pygame.draw.line(Screen,Line_Color,(0,Height-Sqsize),(Width,Height-Sqsize),Line_Width)
    
    def Draw_Fig(self,row,col):
        if self.player==1:
            center=(col*Sqsize+Sqsize//2,row*Sqsize+Sqsize//2)
            #DRAW CIRCLE
            pygame.draw.circle(Screen,Circle_Color,center,Circle_Radius,Circle_Width)
        else:
            #DRAW CROSS
            Start_L_R=(col*Sqsize+Offset,row*Sqsize+Offset)
            End_L_R=(col*Sqsize+Sqsize-Offset,row*Sqsize+Sqsize-Offset)
            pygame.draw.line(Screen,Cross_Color,Start_L_R,End_L_R,Cross_Width)
            Start_R_L=(col*Sqsize+Offset,row*Sqsize+Sqsize-Offset)
            End_R_L=(col*Sqsize+Sqsize-Offset,row*Sqsize+Offset)
            pygame.draw.line(Screen,Cross_Color,Start_R_L,End_R_L,Cross_Width)
    #1->2,2->1
    def Next_turn(self):
        self.player=self.player%2+1

    def Is_Over(self):
        return self.board.Final_State(show=True)!=0 or self.board.Is_Board_full()

#MAIN FUNCTIOIN
def Main():
    game=Game()
    board=game.board
    ai=game.ai

    while True:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:
                    game.Change_GameMode()

                if event.key==pygame.K_r:
                    game.restart()
                    board=game.board
                    ai=game.ai

                #RANDOMAI
                if event.key==pygame.K_0:
                    ai.level=0

                #MINMAXAI
                if event.key==pygame.K_1:
                    ai.level=1

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//Sqsize
                col=pos[0]//Sqsize

                if board.Is_Empty(row,col):
                    game.Make_Move(row,col)

                    if game.Is_Over():
                        game.running=False
   
        if game.Game_Mode=='ai' and game.player==ai.player and game.running:
            pygame.display.update() 

            row,col=ai.eval(board)
            game.Make_Move(row,col)

            if game.Is_Over():
                game.running=False

        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
               
        pygame.display.update()            

#CALLS
Main()