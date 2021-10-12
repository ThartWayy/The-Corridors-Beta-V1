### Intialization V1.30 # uses pynput 
import os #only to clear the console
from time import sleep
from pynput import keyboard
import Level_Art as L # Level file
LobbyArt = L.lobbyX # saves it as a local
import pickle # To save the game
import copy # copy.deepcopy()
import random 
from pynput.keyboard import Key, Controller
Text_Clear = Controller()

def ClearConsole(): # Clears console
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def Randomise_Walls(): # Upon every level intialisation, this would make the walls cooler
    global Current_Location
    Wall = {'☴','☵','☷','☱'}
    Walls = ['☴','☵','☷','☱']
    for Row_Num in range(len(Current_Location)):
        for Grid_Num in range(len(Current_Location[Row_Num])):
            x = set(Current_Location[Row_Num][Grid_Num])
            if x.isdisjoint(Wall) == False:
                Temp_Wall = []
                for x in range(6):
                    Temp_Wall.append(random.choice(Walls))
                Join_Wall = "".join(Temp_Wall)
                Current_Location[Row_Num][Grid_Num] = Join_Wall
    return

def Print_Location(): #Prints the levels in joined strings and borders
    global Lobby_State
    global level8Check
    if Lobby_State == True:
        print(L.lobbyborder)
        for row in Current_Location:
           print('|'.join(row))
        print(L.lobbyborder)    
    
    elif level8Check == True:
        print(L.Arena_Addition1X)
        print(L.Arena_BorderX) 
        for row in Current_Location:
           print('|'.join(row))
        print(L.Arena_BorderX) 
        print(L.Arena_Addition2X)

    else:
        print(L.Arena_Addition1)
        print(L.Arena_Border) 
        for row in Current_Location: 
            print('|'.join(row))


        print(L.Arena_Border) 
        print(L.Arena_Addition2)
    return
level8Check = False # Level 8 is unique in size to the lobby and other levels, so requires different borders

def Wait_For_Input(Time):
    with keyboard.Events() as events:
        events.get(Time)

Key1 = None

def Ask_For_Key(CheckList, Type):
    global Key1
    while True:
        with keyboard.Events() as events:
            event = events.get(100)
            if event == None:
                continue
            event = str(event.key).replace("'", "")
            if Type == 0:
                if event == CheckList:
                    Key1 = event
                    break
            elif Type == 1:
                if event in CheckList:
                    Key1 = event
                    break 

### Entities
class Player():
    def __init__(self, name):
        self._XCoordinates = 3
        self._YCoordinates = 6
        self._Name = name
        self._Wins = 0 #0
        self._Deaths = 0
        self._WeaponK = 1 #1
        self._WeaponL = 0 #0
        self._Keys = 1 #1
        self._Deaths = False
        self._Moonerang = True
        self._Status = True
        self._Door_Entry_Value = None
        self._Levels_Cleared = set({})
        self._StatusMessage = None
        self._Respawn = False
        self._Level0 = True

    def Print_Inventory(self): # prints the important player status
        Weapon_Dictionary = {0: "Empty", 1: "🗡️", 2:"🌙", 3:"💨"}
        global Lobby_State
        if Lobby_State == True:
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
            print("                Keys) {}\n".format(self._Keys))      
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        else:
            print("     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")
            print("            K) {}           L)  {}\n".format(Weapon_Dictionary[self._WeaponK], Weapon_Dictionary[self._WeaponL]))
            print("     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n")

    def Print_Statistics(self): # Final endgame statistics
        ClearConsole()
        print("\n"*10)
        sleep(2)
        print("You abruptly woke up sweating")
        sleep(1)
        print("you realise it was dream")
        print(r"""
              ,----,                                                               
            ,/   .`|                                                               
          ,`   .'  :  ,---,                          ,---,.                        
        ;    ;     /,--.' |                        ,'  .' |                  ,---, 
      .'___,/    ,' |  |  :                      ,---.'   |      ,---,     ,---.'| 
      |    :     |  :  :  :                      |   |   .'  ,-+-. /  |    |   | : 
      ;    |.';  ;  :  |  |,--.   ,---.          :   :  |-, ,--.'|'   |    |   | | 
      `----'  |  |  |  :  '   |  /     \         :   |  ;/||   |  ,"' |  ,--.__| | 
          '   :  ;  |  |   /' : /    /  |        |   :   .'|   | /  | | /   ,'   | 
          |   |  '  '  :  | | |.    ' / |        |   |  |-,|   | |  | |.   '  /  | 
          '   :  |  |  |  ' | :'   ;   /|        '   :  ;/||   | |  |/ '   ; |:  | 
          ;   |.'   |  :  :_:,''   |  / |        |   |    \|   | |--'  |   | '/  ' 
          '---'     |  | ,'    |   :    |        |   :   .'|   |/      |   :    :| 
                    `--''       \   \  /         |   | ,'  '---'        \   \  /   
                                 `----'          `----'                  `----'    
                                                                             
        """)
        
        print("Press space to Continue")
        Ask_For_Key(["Key.space"], 1)
            
        if self._Deaths == 0:
            self._Deaths = '0'

        ClearConsole()
        print("\n"*10)

        print("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ")
        print("""
                Name: {}
                Deaths: {}

        """.format(self._Name, self._Deaths))
        print("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ \n\n\n")
        sleep(2)

        print("Press space to Exit")
        Ask_For_Key("Key.space", 0)
        exit()

    def Weapon_Selection(self): # Opens up a keybinding menu
        ClearConsole()
        global Lobby_State
        Lobby_State = False
        self._WeaponK = 0
        self._WeaponL = 0

        #Weapon_Dictionary = {0: "Empty", 1: "🗡️ Rusty Blade", 2:"🌙 Broken Moonerang", 3:"💨 Blink"}
        Weapons_Choices = {'1': '🗡️ Rusty Blade: Slash one square in a direction'}
        CommandCheck = ["1"]

        if self._Wins > 0:
            Weapons_Choices['2'] = "🌙 Broken Moonerang: Throws a crescent rock you need to pick up \n              Nothing except you can walk ontop of the Moonerang"
            CommandCheck.append("2")
        
        if self._Wins > 3:
            Weapons_Choices['3'] = "💨 Blink: Teleport in a direction, simultaneously destroying the destination"
            CommandCheck.append("3")

        sleep(0.5)
        print('\n'*10, 'Sentient Bookshelf - "Oh. Hello again, What weapon would you like?" \n')
           
        sleep(0.5)
        
        print("    ━━━━━━━━━━━━━━━━━━━━━━━━ The Sentient Weapon Shelf ━━━━━━━━━━━━━━━━━━━━━━━━ \n")
        for Number in CommandCheck:
            
            print("        {})  {}\n".format(Number, Weapons_Choices[Number]))
            sleep(0.3)
            
        print("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\n\n Your inventory: \n")
        ThePlayer.Print_Inventory()
        
        print("\n Input a weapon's number:", end = ' ')
        Ask_For_Key(CommandCheck, 1)
        print('\n')
        CommandCheck.remove(Key1)
        self._WeaponK = int(Key1)
        ClearConsole()
        print("\n"*10)
        print("\n\n Your inventory:\n")
        ThePlayer.Print_Inventory()
        sleep(1)
        
                
                   

        if len(CommandCheck) == 0:
            ClearConsole()
            print('\n'*10)
            print("Your inventory: \n")
            ThePlayer.Print_Inventory()
            print('''\nSentient Bookshelf -"I'll see you next time"''')
            Lobby_State = True
            
            Wait_For_Input(5)
            return        
        else:
            ClearConsole()
            print('\n'*10)
            print('Sentient Bookshelf - "I think you should take another weapon.." \n')

      
            sleep(0.2)
                

            print("    ━━━━━━━━━━━━━━━━━━━━━━━━ The Sentient Weapon Shelf ━━━━━━━━━━━━━━━━━━━━━━━━ \n")
            for Number in CommandCheck:
                
                print("        {})  {}\n".format(Number, Weapons_Choices[Number]))
                sleep(0.3)
                
            print("    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("\n\n Your inventory:\n")
            ThePlayer.Print_Inventory()
            print("\n Input weapon number: ", end = ' ')
            Ask_For_Key(CommandCheck, 1)
            self._WeaponL = int(Key1)
            print('\n')
            sleep(0.5)

        ClearConsole()
        print('\n'*10)
        print("Your inventory:\n")
        ThePlayer.Print_Inventory()
        print("Okay, see you next time!")
        sleep(2)
        Lobby_State = True
        return

    def Border_Check(self, direction): # returns false if player moves off the grid except when into a door that is on the lobby border
        global Current_Location
        if self._XCoordinates == 1 and direction == "a":
            if Lobby_State == True:
                if self._YCoordinates == 2:
                    return True
                if self._YCoordinates == 6:
                    return True
                if self._YCoordinates == 10:
                    return True
                if self._YCoordinates == 14:
                    return True
            return False        

        elif self._XCoordinates == len(Current_Location[1])-2 and direction == "d":
            if Lobby_State == True:
                if self._YCoordinates == 2:
                    return True
                if self._YCoordinates == 6:
                    return True
                if self._YCoordinates == 10:
                    return True
                if self._YCoordinates == 14:
                    return True
            return False

        elif self._YCoordinates == 0 and direction == "w":
            return False        
        elif self._YCoordinates == len(Current_Location)-2 and direction == "s": 
            return False
        return True

    def Border_Check_X(self, direction): # returns false if player is going to teleport off the level
        global Current_Location
        if self._XCoordinates <= 2 and direction == "a":
            return False
        elif self._XCoordinates >= len(Current_Location[1])-3 and direction == "d":
            return False
        elif self._YCoordinates <= 2 and direction == "w":
            return False
        elif self._YCoordinates >= len(Current_Location)-4 and direction == "s": 
            return False
        else:
            return True

    def Move_Lobby(self, direction): # Moves the player by editing the pre-set that gets copied over
        global Current_Location
        global level8Check
        level8Check = False
        if self._XCoordinates == 1 and self._YCoordinates == 2:  # Sets the level number before you go into a hole (level entrance)
            self._Door_Entry_Value = 4
        if self._XCoordinates == 1 and self._YCoordinates == 6:
            self._Door_Entry_Value = 3
        if self._XCoordinates == 1 and self._YCoordinates == 10:
            self._Door_Entry_Value = 2
        if self._XCoordinates == 1 and self._YCoordinates == 14:
            self._Door_Entry_Value = 1
        if self._XCoordinates == 5 and self._YCoordinates == 2:
            self._Door_Entry_Value = 5
        if self._XCoordinates == 5 and self._YCoordinates == 6:
            self._Door_Entry_Value = 6
        if self._XCoordinates == 5 and self._YCoordinates == 10:
            self._Door_Entry_Value = 7
        if self._XCoordinates == 5 and self._YCoordinates == 14:
            self._Door_Entry_Value = 8
            level8Check = True
        else:
            if ThePlayer.Border_Check(direction) == False:
                return

        TempCordsX = self._XCoordinates # Holds the new coordinates
        TempCordsY = self._YCoordinates
        
        if direction == "w": # Sets the new coordinates
            TempCordsY -= 2
        if direction == "s":
            TempCordsY += 2
        if direction == "d":
            TempCordsX += 1
        if direction == "a":
            TempCordsX -= 1

        
        New_Grid = Current_Location[TempCordsY][TempCordsX]
        if set(New_Grid).isdisjoint({"\U0001F5DD"}) == False: # The key
            self._XCoordinates = TempCordsX
            self._YCoordinates = TempCordsY
            self._Keys += 1
            LobbyArt[TempCordsY][TempCordsX] = "      "# deletes the key from the pre-set
            print("You picked up a key")
            sleep(0.3)
            Wait_For_Input(5)    
            return            


        elif set(New_Grid).isdisjoint({"\U0001F5A5"}) == False: # The Bookself
            ThePlayer.Weapon_Selection()   


        elif set(New_Grid).isdisjoint({"\U0001F4DA"}) == False: # The Bookstack
            ThePlayer.Hint_Selection()

        elif not set(New_Grid).isdisjoint({"\U0001F6CF"}):
            print("Would you like to exit and save? (It autosaves at the end of every level)")
            sleep(1)

            print("Y / N")
            
            Ask_For_Key(("y", "n"), 1)
            sleep(0.3)    
            if Key1 == "y":
                pickle.dump(ThePlayer, open("PlayerSaveFile", "wb"))
                pickle.dump(LobbyArt, open("MapSaveFile", "wb"))
                ClearConsole()
                print("\n"*10, "You wake up")
                exit()
            elif Key1 == "n":
                print("You refuse to rest")
                sleep(2)
                

        elif Current_Location[TempCordsY][TempCordsX][0] == " " and Current_Location[TempCordsY][TempCordsX][1] == " ": # so empty spaces includes the numbers
            self._XCoordinates = TempCordsX
            self._YCoordinates = TempCordsY
            return
        


        else:
            Tempgrid = set(Current_Location[TempCordsY][TempCordsX])
            



            if not Tempgrid.isdisjoint({"🚪"}):  # if the grid you walk into has a door, turn door to hole
                Tempstring = []
                if self._Keys >= self._Door_Entry_Value:
                    print("You unlock the door to reveal an ominous hole")
                    sleep(0.3)
                    Wait_For_Input(3)
                  
                    for character in Current_Location[TempCordsY][TempCordsX]:
                        if character != "🚪":
                            Tempstring.append(character)
                        else:
                            Tempstring.append(" 🕳️")

                    LobbyArt[TempCordsY][TempCordsX] = ''.join(Tempstring) # hole now in preset
                else:
                    print("You can't seem to unlock it")
                    sleep(0.3)
                    Wait_For_Input(3)

                    
                return
            
            if Tempgrid.isdisjoint({"🕳️"}): # hole transport you to level, the hole's unicode translates to a different image
                Level_Dictionary = {1:copy.deepcopy(L.Level1), 2:copy.deepcopy(L.Level2), 3:copy.deepcopy(L.Level3), 4:copy.deepcopy(L.Level4), 5:copy.deepcopy(L.Level5), 6:copy.deepcopy(L.Level6), 7:copy.deepcopy(L.Level7), 8:copy.deepcopy(L.Level8),}
                Current_Location = Level_Dictionary[self._Door_Entry_Value]
                Randomise_Walls()
                print("You jumped d")
                sleep(0.3)
                print("             o")
                sleep(0.2)
                print("               w")
                sleep(0.15)
                print("                  n")
                sleep(0.1)
                print("                     .")
                sleep(0.05)
                print("                        .\n")
                sleep(0.05)
                if self._Door_Entry_Value == 4:
                    ClearConsole()
                    print("\n"*10)
                    print("Tip: The Shadows move diagonally and each grid is two rows")
                    Wait_For_Input(5)
                    sleep(1)
                    ClearConsole()
                global Lobby_State
                Lobby_State = False
                return
        return

    def MoveArena(self, Command1, Command2): # Completes the player's action in the level
        global Current_Location
        if Command1 == 0:
            return
        if Command1 in ("w","a","s","d"): # if the player moves
            if ThePlayer.Border_Check(Command1) == False:
                return

            TempCordsX = self._XCoordinates # holds the new coordinates
            TempCordsY = self._YCoordinates

            if Command1 == "w": # Sets the new coordinates
                TempCordsY -= 2
            if Command1 == "s":
                TempCordsY += 2
            if Command1 == "d":
                TempCordsX += 1
            if Command1 == "a":
                TempCordsX -= 1
            
            New_Grid = Current_Location[TempCordsY][TempCordsX]
            if New_Grid == "      ":
                Current_Location[self._YCoordinates][self._XCoordinates] = "      " # erases previous location of player
                self._XCoordinates = TempCordsX
                self._YCoordinates = TempCordsY
                Current_Location[self._YCoordinates][self._XCoordinates] = "  🙂  "

            elif not set(New_Grid).isdisjoint({'☴','☵','☷','☱'}):                
                return
            elif not set(New_Grid).isdisjoint({'🦀','🧟', '🦞'}):

                return
            elif not set(New_Grid).isdisjoint({'🦀','🧟', '🦞'}):

                return
            elif not set(New_Grid).isdisjoint({'🚪'}):
                self._StatusMessage = "As you open the door, a blinding flash spills out"
                self.Won()

            elif not set(New_Grid).isdisjoint({'🌙'}):
                Current_Location[self._YCoordinates][self._XCoordinates] = "      " # erases previous location of player
                self._XCoordinates = TempCordsX
                self._YCoordinates = TempCordsY
                Current_Location[self._YCoordinates][self._XCoordinates] = "  🙂  "
                self._Moonerang = True
                return
        
        elif Command1 in ("k", "l"): #if the player uses a weapon
            Player_Weap_Dict = {"k": self._WeaponK,"l": self._WeaponL}

            if Player_Weap_Dict[Command1] == 0: # Empty Weapon Slot
                print("You used nothing")
                sleep(0.7)
                return
            
            AttackCordsX = self._XCoordinates # holds the new coordinates
            AttackCordsY = self._YCoordinates

            if Player_Weap_Dict[Command1] == 1: # Rusty Sword
                if self.Border_Check(Command2) == False:
                    return
                elif Command2 == "w":
                    AttackCordsY -= 2
                elif Command2 == "s":
                    AttackCordsY += 2
                elif Command2 == "d":
                    AttackCordsX += 1
                elif Command2 == "a":
                    AttackCordsX -= 1

                New_Grid1 = Current_Location[AttackCordsY][AttackCordsX]
                New_Grid2 = Current_Location[AttackCordsY+1][AttackCordsX]
                if set(New_Grid1).isdisjoint({'☴','☵','☷','☱'}) == False:
                    return
                elif New_Grid1 == "      " and New_Grid2 == "      ":
                    return

                elif New_Grid1 == "      " and New_Grid2 == "  👤  ":
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "
                elif not set(New_Grid1).isdisjoint({'🦀','🧟', '🦞'}) and New_Grid2 == "      ":
                    Current_Location[AttackCordsY][AttackCordsX] = "      "
                elif not set(New_Grid1).isdisjoint({'🦀','🧟', '🦞'}) and New_Grid2 == "  👤  ":
                    Current_Location[AttackCordsY][AttackCordsX] = "      "
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "
                elif not set(New_Grid1).isdisjoint({'🚪'}):
                    return

                elif not set(New_Grid1).isdisjoint({'🌙'}):
                    return

                else:
                    print(".. what did you just slice?")
                    sleep(0.7)
                
            if Player_Weap_Dict[Command1] == 2: # Broken Moonerang
                if self._Moonerang == False:
                    return
                
                if not self.Border_Check(Command2):
                    return

                for num in range(3):
                    if Command2 == "w":
                        AttackCordsY -= 2
                    elif Command2 == "s":
                        AttackCordsY += 2
                    elif Command2 == "d":
                        AttackCordsX += 1
                    elif Command2 == "a":
                        AttackCordsX -= 1

                    try:
                        New_Grid1 = Current_Location[AttackCordsY][AttackCordsX]
                        if AttackCordsY < 0 or AttackCordsX < 0:
                            if num == 0:
                                pass
                            else:
                                Current_Location[oldAttackCordsY][oldAttackCordsX] = "  🌙  "
                                self._Moonerang = False
                            return
                    except IndexError:
                        
                        Current_Location[oldAttackCordsY][oldAttackCordsX] = "  🌙  "
                        self._Moonerang = False
                        sleep(0.7)
                        return

                    if num == 0:
                        if not set(New_Grid1).isdisjoint({'☴','☵','☷','☱','🚪', '(', ')'}): # If it immediately hits a wall
                            return

                    if num > 0:
                        if not set(New_Grid1).isdisjoint({'☴','☵','☷','☱','🚪', '(', ')'}): 
                            Current_Location[oldAttackCordsY][oldAttackCordsX] = "  🌙  "
                            self._Moonerang = False
                            return
                        if AttackCordsY == len(Current_Location)-2 and Command2 == "s":
                            Current_Location[AttackCordsY][AttackCordsX] = "  🌙  "
                            self._Moonerang = False
                            return
                        if AttackCordsY == 0 and Command2 == "w":
                            Current_Location[AttackCordsY][AttackCordsX] = "  🌙  "
                            self._Moonerang = False
                            return

                    if not set(New_Grid1).isdisjoint({'🦀','🧟', '🦞'}):
                        Current_Location[AttackCordsY][AttackCordsX] = "  🌙  "
                        self._Moonerang = False
                        return

                    if num == 2:
                        if New_Grid1 == "      ":
                            Current_Location[AttackCordsY][AttackCordsX] = "  🌙  "
                            self._Moonerang = False
                            return

                    oldAttackCordsY = AttackCordsY
                    oldAttackCordsX = AttackCordsX
                    
            if Player_Weap_Dict[Command1] == 3: # Blink
                if self.Border_Check_X(Command2) == False:
                    return
                elif Command2 == "w":
                    AttackCordsY -= 4
                elif Command2 == "s":
                    AttackCordsY += 4
                elif Command2 == "d":
                    AttackCordsX += 2
                elif Command2 == "a":
                    AttackCordsX -= 2

                New_Grid1 = Current_Location[AttackCordsY][AttackCordsX]
                New_Grid2 = Current_Location[AttackCordsY+1][AttackCordsX]

                if not set(New_Grid1).isdisjoint({'🦀','🧟', '🦞'}) and not set(New_Grid2).isdisjoint({'👤'}):
                    Current_Location[self._YCoordinates][self._XCoordinates] = "      "
                    self._XCoordinates = AttackCordsX
                    self._YCoordinates = AttackCordsY
                    Current_Location[AttackCordsY][AttackCordsX] = "  🙂  "
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "

                elif not set(New_Grid1).isdisjoint({'🦀','🧟', '🦞'}) and New_Grid2 == "      ":
                    Current_Location[self._YCoordinates][self._XCoordinates] = "      "
                    self._XCoordinates = AttackCordsX
                    self._YCoordinates = AttackCordsY
                    Current_Location[AttackCordsY][AttackCordsX] = "  🙂  "
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "

                elif New_Grid1 == "      " and not set(New_Grid2).isdisjoint({'👤'}):
                    Current_Location[self._YCoordinates][self._XCoordinates] = "      "
                    self._XCoordinates = AttackCordsX
                    self._YCoordinates = AttackCordsY
                    Current_Location[AttackCordsY][AttackCordsX] = "  🙂  "
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "
                
                elif New_Grid1 == "      ":
                    Current_Location[self._YCoordinates][self._XCoordinates] = "      "
                    self._XCoordinates = AttackCordsX
                    self._YCoordinates = AttackCordsY
                    Current_Location[AttackCordsY][AttackCordsX] = "  🙂  "

                elif not set(New_Grid1).isdisjoint({'🌙'}):
                    Current_Location[self._YCoordinates][self._XCoordinates] = "      "
                    self._XCoordinates = AttackCordsX
                    self._YCoordinates = AttackCordsY
                    self._Moonerang = True
                    Current_Location[AttackCordsY][AttackCordsX] = "  🙂  "
                    Current_Location[AttackCordsY+1][AttackCordsX] = "      "
                
                elif not set(New_Grid1).isdisjoint({'☴','☵','☷','☱','🚪', '(', ')'}):
                    pass
                
                return

                
        
        return
    
    def Status_Check(self): #Checks if the player is dead and ends the level if it is
        global Current_Location
        Grid = Current_Location[self._YCoordinates][self._XCoordinates]
        if set(Grid).isdisjoint({"🙂"}) == True:
            self._Status = False
            self._Deaths += 1
            sleep(1)
            ClearConsole()
            print("\n"*5)
            Print_Location()
            print("Press anything to continue")
            Wait_For_Input(5)
            self._Respawn = True
            
            #Lobby_State = False
            return False
        if self._Status == False:
            return False
        return True

    def Won(self): #Makes sure the player doesn't get the same win twice
        self._Status = False
        self._Respawn = False
        if self._Door_Entry_Value == None: #Level0, the turtorial 
            self._Level0 = False
            self._StatusMessage = """
 Congrats on finishing the turtorial!
            
 You'll continue to unlock new weapons. Remember to use the right ones!

 And get used to the fact that each grid has two rows...
            """
            return
        if self._Door_Entry_Value not in self._Levels_Cleared:
            self._Wins += 1
            LobbyArt[4][3] ="  🗝️   "
            self._Levels_Cleared.add(self._Door_Entry_Value)
            if self._Door_Entry_Value == 1 or self._Door_Entry_Value == 4:
                ClearConsole()
                self._StatusMessage = ("As you open the door, a blinding flash spills out"+"\n\n"+"New weapon Unlocked! (Equip it at the bookshelf)")
                sleep(0.2)
            elif self._Door_Entry_Value == 8:
                self.Print_Statistics()
                  
class Zombie():
    def __init__(self, Xcord, Ycord):
        self._Xcord = Xcord
        self._Ycord = Ycord
        self._Status = True
        self._Moved = "False" # if it didn't move, this is false

    def First_Move(self): # Returns True to remove this entity from the "to move" list. Doesn't do anything
        self._Moved = "False"
        return True

    def Second_Move(self): # Returns false if it wants to move but can't, otherwise, true and moves
        self._Moved = "False"
        if self._Status == False:
            return True
        global Current_Location
        global ThePlayer
        Xdifference = self._Xcord - ThePlayer._XCoordinates
        Ydifference = self._Ycord - ThePlayer._YCoordinates

        if abs(Xdifference) == 1 and abs(Ydifference) == 0: # directly adjacent attack
            #Current_Location[self._Ycord][self._Xcord] == "      "
            Current_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] = "  💀  " 
            ThePlayer._StatusMessage = "The collapsed on the ground after having your neck mauled apart"        
            return True
        elif abs(Xdifference) == 0 and abs(Ydifference) == 2:
            #Current_Location[self._Ycord][self._Xcord] == "      "
            Current_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] = "  💀  "
            ThePlayer._StatusMessage = "The collapsed on the ground after having your neck mauled apart"       
            return True
        
        if self.PathFind() == False:
            return True

        NewX, NewY = self.PathFind()
        if Current_Location[NewY][NewX] == "      ":
            Current_Location[NewY][NewX] = "  🧟  "
            Current_Location[self._Ycord][self._Xcord] = "      "
            self._Xcord = NewX
            self._Ycord = NewY
            self._Moved = "True"
            return True
        


        return False

    def Status_Check(self): # Checks if this entity wasn't killed
        global Current_Location
        Grid = Current_Location[self._Ycord][self._Xcord]
        if set(Grid).isdisjoint({"🧟"}):
            self._Status = False
    
    def SurroundCheck(self, Cords): #returns a list with a coordinates as tuple that are directly adjacent and aren't invalid (Not a wall/door)
        global Current_Location
        Moveable_Spaces = []
        x, y = Cords

        if set(Current_Location[y][x+1]).isdisjoint({"(", ")","☱","☷","☴","☵","🚪","🌙"}): #right
                Moveable_Spaces.append((x+1, y))

        if set(Current_Location[y][x-1]).isdisjoint({"(", ")","☱","☷","☴","☵","🚪","🌙"}): #left
            Moveable_Spaces.append((x-1, y))

        if set(Current_Location[y-2][x]).isdisjoint({"(", ")","☱","☷","☴","☵","🚪","🌙"}): # up
            if (y-2) > -1:
                Moveable_Spaces.append((x, y-2))         

        try: 
            if set(Current_Location[y+2][x]).isdisjoint({"(", ")","☱","☷","☴","☵","🚪","🌙"}): #Down
                Moveable_Spaces.append((x, y+2))
        except IndexError:
            pass    

        return Moveable_Spaces
    
    def PathFind(self): # returns a singular tuple (x,y) as the place this entity wants to go 
        global Current_Location
        global ThePlayer
        startCords = (self._Xcord, self._Ycord)
        goalCords =  (ThePlayer._XCoordinates, ThePlayer._YCoordinates)
        queue = [[startCords]]
        seen = [startCords]
        try:
            while True:
                current = queue[0]

                queue.pop(0)
                for i in self.SurroundCheck(current[-1]):
                    currents = current.copy()
                    currents.append(i)
                    if i == goalCords:
                        return currents[1]
                    elif i in seen:
                        continue # IT GETS TAKEN OUT BECAUSE IT'S NOT APPENED BACK IN
                    queue.append(currents)
                    
                    seen.append(i)
        except:
            return False

    def AttackCounterCheck(self): #Does nothing, allows for the crab function to be applied to the entire enemy list
        return

    def Moved(self):
            return self._Moved

class Shadow():
    def __init__(self, Xcord, Ycord):
        self._Xcord = Xcord
        self._Ycord = Ycord
        self._Status = True
        self._MapIntergity = None # To store the wall that this unit replaces, since this can move into walls
        self._direction = None
        self._Moved = "False" # if it didn't move, this is false
        
    def Direction(self): # Returns the direction the entity goes
        global Current_Location
        global ThePlayer

        self._direction = False
        Xdifference = self._Xcord - ThePlayer._XCoordinates
        Ydifference = self._Ycord-1 - ThePlayer._YCoordinates 
        ### MOVEMENT IS SPLIT INTO 4 QUADRANTS, 1 is top right, 2 is top left, 3 is bottom left, 4 is bottom right

        ### The sporadic movement if on same row or column

        if Xdifference == 0: # directly up/down

            if Ydifference > 0:  # up
                if self._Xcord == 1: # on left border
                    self._direction = "2"   
                elif self._Xcord == len(Current_Location[1])-2: #on right border
                    self._direction = "1"
                else:
                    self._direction = random.choice(["1" , "2"])

            if Ydifference < 0: # down
                if self._Xcord == 1: # on left border
                    self._direction = "4"
                elif self._Xcord == len(Current_Location[1])-2: #on right border
                    self._direction = "3"
                else:
                    self._direction = random.choice(["3", "4"])
        
        elif Ydifference == 0: #directly left/right

            if Xdifference < 0: #directly right
                if self._Ycord == 1: # Can't go up, second row
                    self._direction = "4"
                elif self._Ycord == len(Current_Location)-1: #can't go down, last row
                    self._direction = "1"
                else:
                    self._direction = random.choice(["1", "4"])

            elif Xdifference > 0: # directly left
                if self._Ycord == 1: # Can't go up, second row
                    self._direction = "3"
                if self._Ycord == len(Current_Location)-1: #can't go down, last row
                    self._direction = "2"
                else:
                    self._direction = random.choice(["2", "3"])
        
        elif Xdifference < 0 and Ydifference > 0: # Quadrant 1
            self._direction = "1"

        elif Xdifference > 0 and Ydifference > 0: # Quadrant 2
            self._direction = "2"

        elif Xdifference > 0 and Ydifference < 0: # Quadrant 3
            self._direction = "3"
        
        elif Xdifference < 0 and Ydifference < 0: # Quadrant 4
            self._direction = "4"

    def First_Move(self): # Returns false if it wants to move but can't, otherwise, true and moves or True if dead
        self._Moved = "False"
        if self._Status == False:
            return True
        
        global Current_Location
        global ThePlayer

        self.Direction()

        ### Actual Movement if grid not occupied by another shadow
        AttackCordsY = self._Ycord
        AttackCordsX = self._Xcord
        self._Moved = False
        if self._direction == "1": # Quadrant 1
            CurrentGrid = Current_Location[self._Ycord][self._Xcord]
            Grid = Current_Location[AttackCordsY-2][AttackCordsX+1]
            if set(Grid).isdisjoint({"👤"}): # Can it actually move?
                if self._MapIntergity: # Fixing the grid it moves off of.
                    Current_Location[self._Ycord][self._Xcord] = CurrentGrid[0:2] + self._MapIntergity + CurrentGrid[3:5]
                else:
                    Current_Location[self._Ycord][self._Xcord] = "      "

                self._Ycord = AttackCordsY-2
                self._Xcord = AttackCordsX+1
                Current_Location[self._Ycord][self._Xcord] = Grid[0:2] + "👤" + Grid[4:6]
                self._MapIntergity = None

                if not set(Grid).isdisjoint({'☴','☵','☷','☱'}):
                    self._MapIntergity = Grid[3:5]
                self._Moved = "True"


        elif self._direction == "2": # Quadrant 1
            CurrentGrid = Current_Location[self._Ycord][self._Xcord]
            Grid = Current_Location[AttackCordsY-2][AttackCordsX-1]
            if set(Grid).isdisjoint({"👤"}): # Can it actually move?

                if self._MapIntergity: # Fixing the grid it moves off of.
                    Current_Location[self._Ycord][self._Xcord] = CurrentGrid[0:2] + self._MapIntergity + CurrentGrid[3:5]
                else:
                    Current_Location[self._Ycord][self._Xcord] = "      "

                self._Ycord = AttackCordsY-2
                self._Xcord = AttackCordsX-1
                Current_Location[self._Ycord][self._Xcord] = Grid[0:2] + "👤" + Grid[4:6]
                self._MapIntergity = None
                if not set(Grid).isdisjoint({'☴','☵','☷','☱'}):
                    self._MapIntergity = Grid[3:5]
                self._Moved = "True"
        
        elif self._direction == "3": # Quadrant 1
            CurrentGrid = Current_Location[self._Ycord][self._Xcord]
            Grid = Current_Location[AttackCordsY+2][AttackCordsX-1]
            if set(Grid).isdisjoint({"👤"}): # Can it actually move?

                if self._MapIntergity: # Fixing the grid it moves off of.
                    Current_Location[self._Ycord][self._Xcord] = CurrentGrid[0:2] + self._MapIntergity + CurrentGrid[3:5]
                else:
                    Current_Location[self._Ycord][self._Xcord] = "      "

                self._Ycord = AttackCordsY+2
                self._Xcord = AttackCordsX-1
                Current_Location[self._Ycord][self._Xcord] = Grid[0:2] + "👤" + Grid[4:6]
                self._MapIntergity = None

                if not set(Grid).isdisjoint({'☴','☵','☷','☱'}):
                    self._MapIntergity = Grid[3:5]
                self._Moved = "True"

        
        elif self._direction == "4": # Quadrant 1
            CurrentGrid = Current_Location[self._Ycord][self._Xcord]
            Grid = Current_Location[AttackCordsY+2][AttackCordsX+1]
            if set(Grid).isdisjoint({"👤"}): # Can it actually move?

                if self._MapIntergity != None: # Fixing the grid it moves off of.
                    Current_Location[self._Ycord][self._Xcord] = CurrentGrid[0:2] + self._MapIntergity + CurrentGrid[3:5]
                else:
                    Current_Location[self._Ycord][self._Xcord] = "      "

                self._Ycord = AttackCordsY+2
                self._Xcord = AttackCordsX+1
                Current_Location[self._Ycord][self._Xcord] = Grid[0:2] + "👤" + Grid[4:6]
                self._MapIntergity = None

                if not set(Grid).isdisjoint({'☴','☵','☷','☱'}):
                    self._MapIntergity = Grid[3:5]
                self._Moved = "True"


        if Current_Location[self._Ycord-1][self._Xcord] == "  🙂  ":
            Current_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] = "  💀  "
            ThePlayer._StatusMessage = "Your vision fades to black as you were dragged into the floor"
            return True
        
        if self._Moved == "True":
            return True
        return False
        
    def Second_Move(self): # Attacks in the same grid it is in, just incase the player moved on top of it
        self._Moved = "False"
        if self._Status == False:
            return True

        global Current_Location
        if Current_Location[self._Ycord-1][self._Xcord] == "  🙂  ":
            Current_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] = "  💀  "
            ThePlayer._StatusMessage = "Your vision fades to black as you were dragged into the floor"    
            
        return True

    def Status_Check(self): # Checks if this entity wasn't killed
        global Current_Location
        Grid = Current_Location[self._Ycord][self._Xcord]
        if set(Grid).isdisjoint({"👤"}):
            self._Status = False

    def AttackCounterCheck(self): #Does nothing, allows for the crab function to be applied to the entire enemy list
        return

    def Moved(self):
        return self._Moved

class Crab():
    def __init__(self, Xcord, Ycord, Attack):
        self._Xcord = Xcord
        self._Ycord = Ycord
        self._Status = True
        self._AttackPattern = Attack # vertical (v) or horizontal (h)
        self._AttackCounter = 0 # 0 1 2 3
        self._CanMove = True # The crab still counts as moved if it moves into something
        self._Moved = "False" # if it didn't move, this is false

    def First_Move(self): # Returns false if it wants to move but can't
        self._Moved = "False"
        if self._Status == False:
            return True
        return
    
    def Direction_Move(self): # Return North, South or west to move in
        global ThePlayer
        global Current_Location

        Xdifference = self._Xcord - ThePlayer._XCoordinates
        Ydifference = self._Ycord - ThePlayer._YCoordinates 

        if self._AttackPattern == "v":
            if Ydifference == 0:
                return False
            elif Ydifference > 0:
                return "North"
            elif Ydifference < 0:
                return "South"
        elif self._AttackPattern == "h":
            if Xdifference == 0:
                return False
            elif Xdifference > 0:
                return "West"
            elif Xdifference < 0:
                return "East"
    
    def Direction_Fire(self): # Return North, South East or West to shoot in
        global ThePlayer
        global Current_Location
        Xdifference = self._Xcord - ThePlayer._XCoordinates
        Ydifference = self._Ycord - ThePlayer._YCoordinates 

        # Direct line
        if Xdifference == 0 and Ydifference > 0:
            return "North"
        elif Xdifference == 0 and Ydifference < 0:
            return "South"
        elif Xdifference > 0 and Ydifference == 0 :
            return "West"
        elif Xdifference < 0 and Ydifference == 0 :
            return "East"
        
        # Diagonals
        elif abs(Xdifference) == abs (Ydifference): # so in an exact diagonal, it returns one of the two closest directions
            if Xdifference<0 and Ydifference>0:
                return random.choice(["North" , "East"]) # Quadrant 1
            if Xdifference>0 and Ydifference>0:
                return random.choice(["North" , "West"]) # Quadrant 2
            if Xdifference>0 and Ydifference<0:
                return random.choice(["South" , "West"]) # Quadrant 3
            if Xdifference<0 and Ydifference<0:
                return random.choice(["South" , "East"]) # Quadrant 4

        # The zones between the two previous
        
        elif abs(Xdifference) < abs(Ydifference):
            if Ydifference > 0:
                return "North"
            elif Ydifference < 0:
                return "South"
        elif abs(Xdifference) > abs(Ydifference):
            if Xdifference > 0:
                return "West"
            elif Xdifference < 0:
                return "East"

    def Shoot(self, direction): # Edits a Temporily  version of the grid
        global ThePlayer
        global Current_Location
        global Temp_Location
        if Temp_Location == None:
            Temp_Location = copy.deepcopy(Current_Location)
        Current_Location[self._Ycord][self._Xcord] = "  🦀  "
        Temp_Location[self._Ycord][self._Xcord] = "  🦀  "
        Counter = 0
        if direction == "North":
            for row in range(self._Ycord):
                Counter += 1
                Temp_Location[self._Ycord-Counter][self._Xcord] = "  🟥  "
        
        elif direction == "South":
            for row in range((len(Current_Location)-1) - self._Ycord):
                Counter += 1
                Temp_Location[self._Ycord+Counter][self._Xcord] = "  🟥  "

        elif direction == "East":
            for row in range((len(Current_Location[1])-1) - self._Xcord):
                Counter += 1
                Temp_Location[self._Ycord][self._Xcord+Counter] = "🟥🟥🟥"
        
        elif direction == "West":
            for row in range(self._Xcord):
                Counter += 1
                Temp_Location[self._Ycord][self._Xcord-Counter] = "🟥🟥🟥"

    def Second_Move(self): # Returns false if it wants to move but can't
        self._Moved = "False"
        if self._Status == False or self._CanMove == False:
            return True
        global Current_Location
        Value = False

        if self._AttackCounter < 2:
            direction = self.Direction_Move()
            if direction == False:
                Value = False
            elif direction == "North":
                if Current_Location[self._Ycord-2][self._Xcord] == "      ":
                    Current_Location[self._Ycord][self._Xcord] = "      "
                    Current_Location[self._Ycord-2][self._Xcord] = "  🦀  "
                    self._Ycord = self._Ycord-2
                    Value = True
            elif direction == "South":
                if Current_Location[self._Ycord+2][self._Xcord] == "      ":
                    Current_Location[self._Ycord][self._Xcord] = "      "
                    Current_Location[self._Ycord+2][self._Xcord] = "  🦀  "
                    self._Ycord = self._Ycord+2
                    Value = True
            elif direction == "East":
                if Current_Location[self._Ycord][self._Xcord+1] == "      ":
                    Current_Location[self._Ycord][self._Xcord] = "      "
                    Current_Location[self._Ycord][self._Xcord+1] = "  🦀  "
                    self._Xcord = self._Xcord+1
                    Value = True
            elif direction == "West":
                if Current_Location[self._Ycord][(self._Xcord-1)] == "      ":
                    Current_Location[self._Ycord][self._Xcord] = "      "
                    Current_Location[self._Ycord][(self._Xcord-1)] = "  🦀  "
                    self._Xcord = self._Xcord-1
                    Value = True

        elif self._AttackCounter == 2:
            Current_Location[self._Ycord][self._Xcord] = "  🦞  "
            Value = True

        elif self._AttackCounter == 3:
            #Transform back into a crab is done in Shoot() 
            self.Shoot(self.Direction_Fire())
            Value = True
        
        

        if Value == True:
            self._Moved = "True"
            if self._AttackCounter == 3: 
                self._AttackCounter = 0
            elif self._AttackCounter <= 3:
                self._AttackCounter += 1
            self._CanMove = False
            return True        
        return False

    def AttackCounterCheck(self): #Because if it never moves, it never updates the counter. so this updates the counter
        if self._CanMove == True:
            if self._AttackCounter == 3: 
                self._AttackCounter = 0
            elif self._AttackCounter <= 3:
                self._AttackCounter += 1

    def Status_Check(self):
        global Current_Location
        Grid = Current_Location[self._Ycord][self._Xcord]
        if set(Grid).isdisjoint({"🦀", "🦞"}):
            self._Status = False
        self._CanMove = True

    def Moved(self):
        return self._Moved

### INTRO ###
ClearConsole()
print(r'''


        ,----,                                                                                                           
      ,/   .`|                                                                                                           
    ,`   .'  :  ,---,                        ,----..                                                                     
  ;    ;     /,--.' |                       /   /   \                              ,--,         ,---,                    
.'___,/    ,' |  |  :                      |   :     :  ,---.    __  ,-.  __  ,-.,--.'|       ,---.'|   ,---.    __  ,-. 
|    :     |  :  :  :                      .   |  ;. / '   ,'\ ,' ,'/ /|,' ,'/ /||  |,        |   | :  '   ,'\ ,' ,'/ /| 
;    |.';  ;  :  |  |,--.   ,---.          .   ; /--` /   /   |'  | |' |'  | |' |`--'_        |   | | /   /   |'  | |' | 
`----'  |  |  |  :  '   |  /     \         ;   | ;   .   ; ,. :|  |   ,'|  |   ,',' ,'|     ,--.__| |.   ; ,. :|  |   ,' 
    '   :  ;  |  |   /' : /    /  |        |   : |   '   | |: :'  :  /  '  :  /  '  | |    /   ,'   |'   | |: :'  :  /   
    |   |  '  '  :  | | |.    ' / |        .   | '___'   | .; :|  | '   |  | '   |  | :   .   '  /  |'   | .; :|  | '    
    '   :  |  |  |  ' | :'   ;   /|        '   ; : .'|   :    |;  : |   ;  : |   '  : |__ '   ; |:  ||   :    |;  : |    
    ;   |.'   |  :  :_:,''   |  / |        '   | '/  :\   \  / |  , ;   |  , ;   |  | '.'||   | '/  ' \   \  / |  , ;    
    '---'     |  | ,'    |   :    |        |   :    /  `----'   ---'     ---'    ;  :    ;|   :    :|  `----'   ---'     
              `--''       \   \  /          \   \ .'                             |  ,   /  \   \  /                      
                           `----'            `---`                                ---`-'    `----'                       
The Corridor - By Robert Huynh
A game around analyzing made up rules


''')

sleep(1)
print("Press space to start") # Aesthetics 

Ask_For_Key("Key.space", 0)

ClearConsole()
print("\n"*10)
print("Would you like to load your save?") # Save files
sleep(1)
print("Y / N")

Ask_For_Key(["y", "n"], 1)

if Key1 == "y":
    try:
        ThePlayer = pickle.load(open("PlayerSaveFile", "rb"))
        LobbyArt = pickle.load(open("MapSaveFile", "rb"))
    except:
        sleep(0.5)
        Text_Clear.press(Key.enter)
        Text_Clear.release(Key.enter)
        input() 
        ClearConsole()
        print("\n"*10)
        sleep(0.5) 
        print("It seems as though there is no save file.")
        name = input("Please input a name: ") # Intialise the player entity
        ThePlayer = Player(name)
        pickle.dump(ThePlayer, open("PlayerSaveFile", "wb"))
        pickle.dump(LobbyArt, open("MapSaveFile", "wb"))
        
elif Key1 == "n":
    Text_Clear.press(Key.enter)
    Text_Clear.release(Key.enter)
    input()
    ClearConsole()
    print("\n"*10)
    sleep(0.5)    
    name = input("Please input a name: ") # Intialise the player entity
    ThePlayer = Player(name)
    pickle.dump(ThePlayer, open("PlayerSaveFile", "wb"))
    pickle.dump(LobbyArt, open("MapSaveFile", "wb"))

    


### The Game Begins

Game_State = True
while Game_State:
    Lobby_State = True

    if ThePlayer._Level0 == True:
        Lobby_State = False
        ThePlayer._Respawn = True
        ClearConsole()
        print("\n"*9)
        print("""
Welcome to the turtorial, {}!

    Always remember the following:\n""".format(ThePlayer._Name))
        sleep(1)
        print("        W, A, S, D to move\n")
        sleep(0.1)
        Wait_For_Input(5)
        
        print("        K or L for your items\n")
        sleep(0.1)
        Wait_For_Input(5)
        
        print("        Spacebar to skip your turn\n")   
        sleep(0.1)
        Wait_For_Input(5)

        print("        and..")
        sleep(0.1)
        Wait_For_Input(5)
        print("        Enemies are designed to kill you")

        
        sleep(1)
        print("\n"*2)
        print("Press any key to continue")
        Wait_For_Input(2)
        
        Current_Location = copy.deepcopy(L.Level0)
        Randomise_Walls()

    if ThePlayer._Level0 == True:
        pass

    elif ThePlayer._Respawn == True: #if player just died, they are given the chance to respawn inside the level
        ClearConsole()
        print("\n"*10)
        print("Would you like to continue from the level?\n") # Sees if they want to leave
        sleep(0.2)
        print("Y / N")
        Ask_For_Key(["y","n"], 1)

        if Key1 == "y":
            Lobby_State = False
            Level_Dictionary = {1:copy.deepcopy(L.Level1), 2:copy.deepcopy(L.Level2), 3:copy.deepcopy(L.Level3), 4:copy.deepcopy(L.Level4), 5:copy.deepcopy(L.Level5), 6:copy.deepcopy(L.Level6), 7:copy.deepcopy(L.Level7), 8:copy.deepcopy(L.Level8),}
            Current_Location = Level_Dictionary[ThePlayer._Door_Entry_Value]
            Randomise_Walls()
        
        elif Key1 == "n":
            ClearConsole()
            ThePlayer._XCoordinates = 3
            ThePlayer._YCoordinates = 12
            ThePlayer._Respawn = False
            

    if ThePlayer._Respawn == False: # Intro # Aesthetics 
        ClearConsole()
        print("\n" * 10)
        print("You groggily open your eyes and gaze around the to what appears to be a antique corridor lit by a few candles\n")
        sleep(0.3)
        print("Press anything to continue")
        Wait_For_Input(10)
        ClearConsole()
        print("\n" * 10)
        print("You groggily open your eyes and gaze around the to what appears to be a antique corridor lit by a few candles\n")

        print("There is a faint sense of familiarity that you can't place. You try walking around\n\n")
        sleep(0.5)
        print("Press anything to continue")
        Wait_For_Input(10)
        sleep(0.3)
        ClearConsole()

        if ThePlayer._Respawn == False:
            ThePlayer._XCoordinates = 3
            ThePlayer._YCoordinates = 12

    ### LOBBY ###

    while Lobby_State == True: 
        Current_Location = copy.deepcopy(LobbyArt)
        Current_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] = "  🙂  "
        Print_Location()
        ThePlayer.Print_Inventory()
        sleep(0.2)

        Ask_For_Key(("w","a","s","d"), 1)

        ThePlayer.Move_Lobby(Key1) 
        ClearConsole()

    ### LEVEL INTIALISATION ###

    ThePlayer._Status = True 
    ThePlayer._Moonerang = True

    Enemy_List = {}
    counter = 1

    for y in range(len(Current_Location)): # Intializing all the emojis on the pre-set into entities
        for x in range(len(Current_Location[y])):
            Grid = Current_Location[y][x]
            if set(Grid).isdisjoint({"🧟"}) == False:
                Enemy_List[counter] = Zombie(x, y) 
                counter += 1
            if set(Grid).isdisjoint({"👤"}) == False:
                Enemy_List[counter] = Shadow(x, y)
                counter += 1
            if set(Grid).isdisjoint({"🦀"}) == False:
                Enemy_List[counter] = Crab(x, y, Grid[3])
                Current_Location[y][x] = "  🦀  "
                counter += 1
            if set(Grid).isdisjoint({"🙂"}) == False:
                ThePlayer._XCoordinates = x
                ThePlayer._YCoordinates = y

    Time_Between_Combat_Panels = 0.10
    
    ### THE LEVEL ###

    ClearConsole()
    print("\n"*5)
    Print_Location()
    ThePlayer.Print_Inventory()

    while ThePlayer._Status:  
        

        ### PLAYER INPUT ###
        print("Input Action: ") 

        Ask_For_Key(("w","a","s","d","k","l","Key.space"), 1) # Key and/or Key2

        if Key1 == 'Key.space':
            Command1 = 0
            Direction = 0
            
        elif Key1 in ("w","a","s","d","k","l"):
            Command1 = Key1
            if Key1 in ("w","a","s","d"):
                Direction = 0 
                
            elif Key1 in ("k","l"): # if using the weapon, also ask for a direction to shoot in   n
                print("Please input direction: ")
                Ask_For_Key(("w","a","s","d"), 1)
                Direction = Key1

                        
                    
        

        ### MOVE PHASE ONE ###

        counter = 0
        TempEnemies = []
        for enemy in Enemy_List.values():
            TempEnemies.append(enemy)
        while True: #Shadows are the only ones that move in First_Move() at all 
            for Enemy in TempEnemies:
                if Enemy.First_Move() == True: #if it moved, remove it from the TO DO list
                    TempEnemies.remove(Enemy)

                    if ThePlayer.Status_Check() == False:
                        ClearConsole()
                        print("\n"*5)
                        Print_Location()
                        break
            counter += 1                
            if ThePlayer._Status == False or len(TempEnemies) == 0 or counter >= 10:
                break
        TempList = []
        for enemy in Enemy_List.values():
            TempList.append(enemy.Moved()) 
        if ThePlayer._Status == False:
            break
        if "True" in TempList: # All enemies for this phase don't exist.
            ClearConsole()
            print("\n"*5)
            Print_Location()
            ThePlayer.Print_Inventory()
            sleep(Time_Between_Combat_Panels)


        
        ### PLAYER MOVES ###

        ThePlayer.MoveArena(Command1, Direction) # The player moves
        ClearConsole() # Aesthetics and prints layout
        print("\n"*5)
        Print_Location()
        ThePlayer.Print_Inventory()
        if ThePlayer._Status == False: # If he reaches the door
            break 
        sleep(Time_Between_Combat_Panels)
        for enemy in Enemy_List.values():# makes all the enemies that were killed, actually die
            enemy.Status_Check()
        

        ### MOVE PHASE TWO ###

        counter = 0
        TempEnemies = []
        for enemy in Enemy_List.values(): 
            TempEnemies.append(enemy)
        Temp_Location = None # if the crabs shoot, this becomes != None

        while True: #Shadows are the only ones that don't move in Second_Move() at all
            for Enemy in TempEnemies:
                if Enemy.Second_Move() == True: #if it moved, remove it from the TO DO list
                    TempEnemies.remove(Enemy)

                    if ThePlayer.Status_Check() == False:
                        break
            counter += 1
            if ThePlayer._Status == False or len(TempEnemies) == 0 or counter >= 10:
                break
        for enemy in Enemy_List.values():  # Increments counter of the crabs that didn't move
            enemy.AttackCounterCheck()
        if ThePlayer._Status == False:
            break 
        
        TempList = []
        for enemy in Enemy_List.values():
            TempList.append(enemy.Moved()) 
        if "True" in TempList: # All enemies for this phase don't exist.
            ClearConsole()
            print("\n"*5)
            Print_Location()
            ThePlayer.Print_Inventory()
            sleep(Time_Between_Combat_Panels)
        

        if Temp_Location != None: # Prints a temp grid where the crabs shot the lasers destroying the whole grid
            #Temp_location is a snapshot of the past that is edited, so zombies become "unmoved" if the first crab was before the zombie
            #add back the zombies
            for y in range(len(Temp_Location)):
                for x in range(len(Temp_Location[y])):
                    if Current_Location[y][x] == "  🧟  ":
                        if set(Temp_Location[y][x]).isdisjoint(("🟥")) and Temp_Location[y][x] == "      ":
                            Temp_Location[y][x] = "  🧟  "
                            
            if level8Check == True:
                ClearConsole()
                print("\n"*5)
                print(L.Arena_Addition1X)
                print(L.Arena_BorderX) 
                for row in Temp_Location:
                    print('|'.join(row))
                print(L.Arena_BorderX) 
                print(L.Arena_Addition2X) 
            else:
                ClearConsole()
                print("\n"*5)
                print(L.Arena_Addition1)
                print(L.Arena_Border) 
                for row in Temp_Location:
                    print('|'.join(row))
                print(L.Arena_Border) 
                print(L.Arena_Addition2)
            sleep(0.7)
            if Temp_Location[ThePlayer._YCoordinates][ThePlayer._XCoordinates] != "  🙂  ":
                ThePlayer._Status = False
                ThePlayer._Respawn = True
                ThePlayer._Deaths += 1
                ThePlayer._StatusMessage = "A burst of red light melted you"
                break
            ClearConsole()
            print("\n"*5)
            Print_Location()
            ThePlayer.Print_Inventory()


    sleep(1)
    ClearConsole()
    print("\n"*10)
    print(ThePlayer._StatusMessage) # Either a win message or a death message
    sleep(1)
    print("\n")
    print("Press space to continue")
    Ask_For_Key("Key.space", 0)
    pickle.dump(ThePlayer, open("PlayerSaveFile", "wb"))
    pickle.dump(LobbyArt, open("MapSaveFile", "wb"))





        


