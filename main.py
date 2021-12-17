#!/usr/bin/python3
from typing import Dict, List, Tuple, Union
import GUI
from PyQt5 import QtCore, QtGui, QtWidgets

# from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import random
import ast
import time
import notify2


class UI_handler(GUI.Ui_window, QtWidgets.QMainWindow, QtWidgets.QDialog):

    def __init__(self) -> None:
        super(UI_handler, self).__init__()

    
    def initialise_game(self) -> None:
        """
        This function initialises all the necessary settings and variables and 
        flags required in algorithms of this game to play it smoothly and to make
        sure it will run correctly without any issue.
        """
        
        self.change_score("")
        self.initial_coordinates()
        self.new_game: bool = False

        # Initiaising variables for sending notification
        notify2.init("Snakes And Ladders")
        self.notificationobj = notify2.Notification(None)
        self.notificationobj.set_urgency(notify2.URGENCY_NORMAL)
        self.notificationobj.set_timeout(10000)

    
    def initialise_buttons(self) -> None:
        """
        This function initialised all the click listeners on the buttons we have
        in our GUI game.
        """
        
        self.startButton.clicked.connect(lambda: self.startGame())
        self.play_chance.clicked.connect(lambda: self._play_players_chance())

    
    def initial_coordinates(self) -> None:
        """
        Function to get the players goti's initial co-ordinates to 
        """
        self.p1_x, self.p1_y = self._get_players_initial_coordinates(first = True)
        self.p2_x, self.p2_y = self._get_players_initial_coordinates(first = False)
        
        print("Player 1 initial coordinates: ", self.p1_x, self.p1_y)
        print("Player 2 initial coordinates: ", self.p2_x, self.p2_y)


    def startGame(self):
        """
        This function initialises all the necessary settings and variables and 
        flags as per requirements when the game actually starts.
        """
        
        # Moving the players position to origin.
        self.reset_position()

        # Resetting all requied parameters
        self.change_player2_color_fade()
        self.change_player1_color_fade()
        self.change_score("")



        print("Game Started...")
        self.new_game: bool = True
        self.show_notification("Snakes and Ladders", "New Game Has Started")
    

        # initialising which player's turn is now to play.
        self.p1_turn: bool = True
        self.change_player1_color_solid()
        self.change_player2_color_fade()


        # Initialising Each players position between 1 and 100
        self.p1_position: int = 0
        self.p2_position: int = 0

        
        # Variables for determining the player is unlocked to play initially or not.
        self.p1_unlocked: bool = False
        self.p2_unlocked: bool = False


        # self._play_players_chance()



    def _play_players_chance(self):
        """
        This function is heart of this game. Contains all the neccessary algorithms to
        make the dice and players move across the board game, and calculates the position
        of each player when dice throw event is simulated. This function simulates all the
        things which happens in reality after the dice is thrown by one person until there
        comes the chance of other player to throw a dice.
        """
        
        # Checking if the game is started or not.
        if not self.new_game:
            self.show_notification("Snakes and Ladders", "Please start the game first.")
            return

        # Simulating rolling dice event.
        random_number = self.generate_number()
        
        # Handling error if self.p1_turn is not initialised yet.
        try:
            # Highlighting which player's turn is now.
            if self.p1_turn:
                self.change_score(random_number)
                self.toggle_active_player_color(True)

                if not self.p1_unlocked:
                    if random_number == 6:
                        print("Player 1 Unlocked Now")
                        self.p1_unlocked: bool = True
                        self.p1_turn: bool = True

                        # Now Moving player to posiiton 1
                        self.p1_position: int = 1
                        posiiton_obj = self._get_position_object(str(self.p1_position))
                        self.move_player1(posiiton_obj.x(), posiiton_obj.y())

                    else:
                        time.sleep(0.7)
                        self.p1_turn: bool = False
                        self.toggle_active_player_color(False)
                    
                    return

            else:
                self.change_score(random_number)
                self.toggle_active_player_color(False)

                if not self.p2_unlocked:
                    if random_number == 6:
                        print("Player 2 Unlocked Now")
                        self.p2_unlocked: bool = True 
                        self.p1_turn: bool = False

                        # Now Moving player to posiiton 1
                        self.p2_position: int = 1
                        posiiton_obj = self._get_position_object(str(self.p2_position))
                        self.move_player2(posiiton_obj.x(), posiiton_obj.y())

                    else:
                        time.sleep(0.7)
                        self.p1_turn: bool = True
                        self.toggle_active_player_color(True)

                    return

            if self.p1_turn:
                temp_pos: int = self.p1_position + random_number
                if temp_pos > 100:
                    pass

                elif temp_pos == 100:
                    posiiton_obj = self._get_position_object("100")
                    self.move_player2(posiiton_obj.x(), posiiton_obj.y())
                    self.show_notification("Snakes and Ladders", "Congratulations, Player 1 Wins")
                    self.new_game: bool = False

                else:
                    self.p1_position: int = self.p1_position + random_number
                    # print("positions are", self.p1_unlocked, self.p2_position)
                    posiiton_obj = self._get_position_object(str(self.p1_position))
                    self.move_player1(posiiton_obj.x(), posiiton_obj.y())

                    # Checking if posiiton is checkpoint or not.
                    _checkpoint = self.checkpoints_map(int(self.p1_position))
                    if _checkpoint is not None:
                        self.p1_position: int = _checkpoint
                        posiiton_obj = self._get_position_object(str(_checkpoint))
                        time.sleep(2)
                        self.move_player1(posiiton_obj.x(), posiiton_obj.y())
                        
                        # Checking if the checkpoint reached is ladde or snake
                        '''
                        If checkpoint will be ladder then user gets another chance to play.
                        If checkpoint will be snake then user will not get another chance to play.
                        '''
                        if _checkpoint > self.p1_position:
                            return

            else:
                temp_pos: int = self.p2_position + random_number
                if temp_pos > 100:
                    pass

                elif temp_pos == 100:
                    posiiton_obj = self._get_position_object("100")
                    self.move_player2(posiiton_obj.x(), posiiton_obj.y())
                    self.show_notification("Snakes and Ladders", "Congratulations, Player 2 Wins")
                    self.new_game: bool = False


                else:
                    self.p2_position: int = self.p2_position + random_number
                    # print("positions are", self.p1_unlocked, self.p2_position)
                    posiiton_obj = self._get_position_object(str(self.p2_position))
                    self.move_player2(posiiton_obj.x(), posiiton_obj.y())

                    # Checking if posiiton is checkpoint or not.
                    _checkpoint = self.checkpoints_map(int(self.p2_position))
                    if _checkpoint is not None:
                        self.p2_position: int = _checkpoint
                        posiiton_obj = self._get_position_object(str(_checkpoint))
                        time.sleep(2)
                        self.move_player2(posiiton_obj.x(), posiiton_obj.y())
                        
                        # Checking if the checkpoint reached is ladde or snake
                        '''
                        If checkpoint will be ladder then user gets another chance to play.
                        If checkpoint will be snake then user will not get another chance to play.
                        '''
                        if _checkpoint > self.p1_position:
                            return


            # print("something", ast.literal_eval("self.f46.x()"))
            if random_number != 6:
                self.toggle_players_chance()
                self.toggle_active_player_color(self.p1_turn)
        
        except:
            self.show_notification("Snakes and Ladders", "Game has not started yet. Please Start the game first")
            print("Game has not started yet. Please Start the game first")


    
    def reset_position(self) -> None:
        """
        This function resets the player's goti position to their starting place. 
        """
        self.player2.move(10, 750)
        self.player1.move(10, 800)


    def _get_players_initial_coordinates(self, first: bool = True) -> Tuple[int]:
        """
        This function gives the player's initial co-ordinates when the window just opens.
        @params:
            first: flag to identify wheather the request for co-ordinates is for player1
                    or player2

        @return: tuple of two integer points representing x & y co-ordinates of players
                    respectively. 
        """

        if first:
            return (self.player1.x(), self.player1.y())
        else:
            return (self.player2.x(), self.player2.y())


    def show_notification(self, title: str, body: str) -> None:
        """

        Function responsible for showing all GUI based desktop notifications.
        @params:
            title: Takes title string for notification popup.
            body: Takes body string for notification popup.

        """

        self.notificationobj.update(title, body)
        self.notificationobj.show()


    def generate_number(self) -> int:
        """
        This function generates any random number between 1 to 6 including
        both numbers. Used for simulating rolling dice event.
        """

        return random.randint(1,6)


    def toggle_active_player_color(self, player1: bool) -> None:
        """
        This function changes the css of player1 or player2 indicators, thereby 
        informing us about which player's turn is currently going on. 

        @params:
            player1: flag to identify player1 or player2 for which the notification
                        of alertess will be generated.
        """
        
        if player1:
            self.change_player1_color_solid()
            self.change_player2_color_fade()
        else:
            self.change_player1_color_fade()
            self.change_player2_color_solid()


    def toggle_players_chance(self) -> None:
        """
        Toggles the player's chance variable indicating which player's turn is
        currently going to be. This is helper function to support the exsisting 
        algorithm to work properly.
        """
        if self.p1_turn:
            self.p1_turn: bool = False
            return
      
        self.p1_turn: bool = True


    def doAnim(self, QtObjects: QtWidgets.QLabel, x: int, y: int) -> None:
        """
        This function actually animates the movement of player's positions
        across the board.
        @params:
            QtObjects: The object which you want to move in the window.
                        Generally it would be of type QLabel.
            x: The final x co-ordinate of the location where the object has to go.
            y: The final y co-ordinate of the location where the object has to go.
        """
        
        self.anim = QPropertyAnimation(QtObjects, b"pos")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QtObjects.pos())
        self.anim.setEndValue(QPoint(x, y))
        self.anim.start()


    def change_score(self, score: str) -> None:
        """
        This function used to display the current outcome of dice rolling
        event. 
        @params:
            Score: String variable which is used for displaying current outcome result 
                    between 1 & 6. 
        """
        
        self._translate = QtCore.QCoreApplication.translate
        self.diceResult.setHtml(self._translate("window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                    "p, li { white-space: pre-wrap; }\n"
                                    "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                    f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:48pt; color:#ffffff;\">{score}</span></p></body></html>"
                                                )
                                )
        self.startButton.setText(self._translate("window", "Start Game"))


    def change_player1_color_solid(self) -> None:
        """
        This function changes the flag color to solid to indicate that now is
        player 1's turn.
        """
        self.player1_label.setStyleSheet("QWidget[objectName=\"player1_label\"]{\n"
            "background: 3px solid red;\n"
            "border-radius: 20px;\n"
            "}")    


    def change_player2_color_solid(self):
        """
        This function changes the flag color to solid to indicate that now is
        player 2's turn.
        """
        self.player2_label.setStyleSheet("QWidget[objectName=\"player2_label\"]{\n"
            "background: 3px solid blue;\n"
            "border-radius: 20px;\n"
            "}")

    
    def change_player1_color_fade(self) -> None:
        """
        This function changes the flag color to solid to indicate that there
        is not a turn for player 1 to play.
        """
        self.player1_label.setStyleSheet("QWidget[objectName=\"player1_label\"]{\n"
            "background: 3px #3c1c0b;\n"
            "border-radius: 20px;\n"
            "}")    


    def change_player2_color_fade(self):
        """
        This function changes the flag color to solid to indicate that there
        is not a turn for player 1 to play.
        """
        self.player2_label.setStyleSheet("QWidget[objectName=\"player2_label\"]{\n"
            "background: 3px #3a1b08;\n"
            "border-radius: 20px;\n"
            "}")

    
    def move_player1(self, x: int, y: int) -> None:
        """
        This function used to move the player1's goti to some
        given x & y co-ordinate in the canvas/board game.
        @params:
            x: x co-ordinate of final position.
            y: y co-ordinate of final position.
        """
        
        # Calling the animation function to animate the moverment across board/canvas
        self.doAnim(self.player1, int(x), int(y))

    
    def move_player2(self, x: int, y: int) -> None:
        """
        This function used to move the player1's goti to some
        given x & y co-ordinate in the canvas/board game.
        @params:
            x: x co-ordinate of final position.
            y: y co-ordinate of final position.
        """

        self.doAnim(self.player2, int(x), int(y))


    def checkpoints_map(self, pos: int) -> Union[int, None]:
        """
        Contains all the key-value pairs of checkpoints that we have in game.
        Checkpoints includes the snake-biting positions to go down and ladder 
        rising positions to rise up.

        @params: 
            pos: required for getting final co-ordinates/place of the players 
                    when the particular checkpoint position is reached.

        @returns: final corresponding position in 1-100 grid game board when 
                    some checkpoint is reached.
        """
        
        checkpoints: Dict[int, int] = {
            9: 53,
            23: 59,
            44: 94,
            67: 6,
            88: 31,
            99: 4
        }

        return checkpoints.get(int(pos), None)


    def _get_position_object(self, index: str) -> Union[QtWidgets.QFrame, None]:
        """
        This functino gives the corresponding QWidget objects that are mapped to each 
        position from 1-100 in GUI. This objects helps to identify the position of particular 
        position between 0-100 thereby making us easy for moving the player's goti within the game.

        @params:
            index: this is the position of any player's goti

        @returns: corresponding QFrame object that is present at that particular geometrical
                    location, or None in case the position doesn't exsists i.e. if position > 100.
        """
        
        positions: Dict[str, QtWidgets.QFrament] = {
            "1": self.f1, "2": self.f2, "3": self.f3, "4": self.f4, "5": self.f5,
            "6": self.f6, "7": self.f7, "8": self.f8, "9": self.f9, "10": self.f10,
            "11": self.f11, "12": self.f12, "13": self.f13, "14": self.f14, "15": self.f15,
            "16": self.f16, "17": self.f17, "18": self.f18, "19": self.f19, "20": self.f20,
            "21": self.f21, "22": self.f22, "23": self.f23, "24": self.f24, "25": self.f25,
            "26": self.f26, "27": self.f27, "28": self.f28, "29": self.f29, "30": self.f30,
            "31": self.f31, "32": self.f32, "33": self.f33, "34": self.f34, "35": self.f35,
            "36": self.f36, "37": self.f37, "38": self.f38, "39": self.f39, "40": self.f40,
            "41": self.f41, "42": self.f42, "43": self.f43, "44": self.f44, "45": self.f45,
            "46": self.f46, "47": self.f47, "48": self.f48, "49": self.f49, "50": self.f50,
            "51": self.f51, "52": self.f52, "53": self.f53, "54": self.f54, "55": self.f55,
            "56": self.f56, "57": self.f57, "58": self.f58, "59": self.f59, "60": self.f60,
            "61": self.f61, "62": self.f62, "63": self.f63, "64": self.f64, "65": self.f65,
            "66": self.f66, "67": self.f67, "68": self.f68, "69": self.f69, "70": self.f70,
            "71": self.f71, "72": self.f72, "73": self.f73, "74": self.f74, "75": self.f75,
            "76": self.f76, "77": self.f77, "78": self.f78, "79": self.f79, "80": self.f80,
            "81": self.f81, "82": self.f82, "83": self.f83, "84": self.f84, "85": self.f85,
            "86": self.f86, "87": self.f87, "88": self.f88, "89": self.f89, "90": self.f90,
            "91": self.f91, "92": self.f92, "93": self.f93, "94": self.f94, "95": self.f95,
            "96": self.f96, "97": self.f97, "98": self.f98, "99": self.f99, "100": self.f100,
        }

        return positions.get(str(index), None)


if __name__ == "__main__":
    # Initialising our GUI app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    # Instantialting the UI class
    ui = UI_handler()

    # Handling the app to show the main desined UI from UI_handler class
    ui.setupUi(MainWindow)

    # Displaying the game window. 
    MainWindow.show()

    # For setting up the basic configuratino required for playing this game.
    ui.initialise_buttons()
    ui.initialise_game()

    # Silently Exits when window closed.
    sys.exit(app.exec_())