# Author: Michelle Mann
# Date: 08/03/2021
# Description: Portfolio Project
# Quoridor Game. Allows two players to move their pawn across a 9x9 square
# game board. First to the opposing side wins. Players can use fences to block
# each-other's moves. Each player gets 10 fences.


class YouAlreadyLiveHereError(Exception):
    """
    Reminds players that they are already occupying the space they'd like to move to.
    """
    pass


class Node:
    """
    Represents a single playable position on a game board.
    Will be composited into our QuoridorGame class.
    """

    def __init__(self, name):
        """
        Initializes a single playable position with 9 outside movement opportunities
        and a data member that can be set to a specific player object. Additionally,
        offers options to add a fence in any of the four cardinal directions for the node.
        """
        # Will initialize node name as None. Will ultimately adopt the name of the coordinate
        # Node exists at on board (col, row) or (x, y)
        self._node_name = name
        self._next_node = None

        # Will initialize as None, if a player lands in spot, will update to P1 or P2
        # Can also be a fence.
        self._player_data = None

        # The positions in any cardinal position around the node.
        self._one_up = None  # The node above this node
        self._one_down = None  # The node below this node
        self._one_right = None  # The node right of this node
        self._one_left = None  # The node left of this node
        self._one_diag_up_right = None  # The node up/right of this node
        self._one_diag_up_left = None  # The node up/left of this node
        self._one_diag_down_right = None  # The node down/right of this node
        self._one_diag_down_left = None  # The node down/left of this node

        # Defines the four sides of a node that fences can be place
        self._up_wall = False
        self._down_wall = False
        self._left_wall = False
        self._right_wall = False

    def __repr__(self):
        """The representation of our object"""
        return "--" + repr(self._node_name) + "--"

    def set_player_data(self, player_obj):
        """Sets the player_data member to that of a player object"""
        self._player_data = player_obj

    def get_player_data(self):
        """Returns the player_data object of a specific node"""
        return self._player_data

    def get_next(self):
        """Returns the next node object currently linked in the list."""
        return self._next_node

    def set_next(self, node_object):
        """Sets the node object the current object will point to"""
        self._next_node = node_object

    def set_node_name(self, coordinate):
        """Sets the node name with a tuple value (row, col)"""
        self._node_name = coordinate

    def get_node_name(self):
        """Returns the node name which is a tuple coordinate of it's
        location"""
        return self._node_name

    def get_up_wall(self):
        """Returns whether there is a fence in north wall"""
        return self._up_wall

    def set_up_wall(self):
        """Sets whether there is a fence in the north wall"""
        if self.get_up_wall() is False:
            self._up_wall = True
            return self._up_wall
        else:
            return "Wall already exists"

    def get_down_wall(self):
        """Returns whether there is a fence in south wall"""
        return self._down_wall

    def set_down_wall(self):
        """Sets whether there is a fence in the south wall"""
        if self.get_down_wall() is False:
            self._down_wall = True
            return self._down_wall
        else:
            return "Wall already exists"

    def get_left_wall(self):
        """Returns whether there is a fence in west wall"""
        return self._left_wall

    def set_left_wall(self):
        """Sets whether there is a fence in the west wall"""
        if self.get_left_wall() is False:
            self._left_wall = True
            return self._left_wall
        else:
            return "Wall already exists"

    def get_right_wall(self):
        """Returns whether there is a fence in east wall"""
        return self._right_wall

    def set_right_wall(self):
        """Sets whether there is a fence in the east wall"""
        if self.get_right_wall() is False:
            self._right_wall = True
            return self._right_wall
        else:
            return "Wall already exists"

    def get_list_of_walls(self):
        """
        Returns the list of all walls
        """
        list_of_walls = {
            "up": self.get_up_wall(),
            "down": self.get_down_wall(),
            "left": self.get_left_wall(),
            "right": self.get_right_wall()
        }

        return list_of_walls

    def get_nearby_nodes(self):
        """Returns all spaces touching this Node as index values (row, col)"""
        list_of_nearby_spaces = {"up": self._one_up,
                                 "down": self._one_down,
                                 "right": self._one_right,
                                 "left": self._one_left,
                                 "up-right": self._one_diag_up_right,
                                 "up-left": self._one_diag_up_left,
                                 "down-right": self._one_diag_down_right,
                                 "down-left": self._one_diag_down_left
                                 }
        return list_of_nearby_spaces

    def set_nearby_nodes(self):
        """Sets all nearby nodes of our current node"""
        current_node = self.get_node_name()

        self._one_up = (current_node[0], current_node[1] - 1)  # (0, -1)
        self._one_down = (current_node[0], current_node[1] + 1)  # (0, 1)
        self._one_right = (current_node[0] + 1, current_node[1])  # (1, 0)
        self._one_left = (current_node[0] - 1, current_node[1])  # (-1, 0)
        self._one_diag_up_right = (current_node[0] + 1, current_node[1] - 1)  # (1, -1)
        self._one_diag_up_left = (current_node[0] - 1, current_node[1] - 1)  # (-1, -1)
        self._one_diag_down_right = (current_node[0] + 1, current_node[1] + 1)  # (1, 1)
        self._one_diag_down_left = (current_node[0] - 1, current_node[1] + 1)  # (-1, 1)


class GameBoard:
    """
    Represents a square game board of nodes as a linked list
    (will default to 9 x 9 but can be of any size)
    Will be composited into our QuoridorGame class.
    """

    def __init__(self):
        """
        Initializes a game board with nodes in every position
        """
        # The header of our linked list
        self._board_head = None

        # The dedicated positions that player 1 would need to reach to win
        self._p2_winning_area = [(0, 0),
                                 (1, 0),
                                 (2, 0),
                                 (3, 0),
                                 (4, 0),
                                 (5, 0),
                                 (6, 0),
                                 (7, 0),
                                 (8, 0)]

        # The dedicated positions that player 2 would need to reach to win
        self._p1_winning_area = [(0, 8),
                                 (1, 8),
                                 (2, 8),
                                 (3, 8),
                                 (4, 8),
                                 (5, 8),
                                 (6, 8),
                                 (7, 8),
                                 (8, 8)]

        # The extreme bounds of the board
        self._outer_bounds = [(0, 0), (8, 8)]

    def get_head(self):
        """Returns the head of our list"""
        return self._board_head

    def set_head(self, node_object):
        """Sets the object our header points to."""
        self._board_head = node_object

    def get_p1_winning_area(self):
        """Returns a list of node names that P1 must land on
        in order to win the game."""
        return self._p1_winning_area

    def get_p2_winning_area(self):
        """Returns a list of node names that P2 must land on
        in order to win the game."""
        return self._p2_winning_area

    def get_outer_bounds(self):
        """
        Returns the outer bounds of the board.
        """
        return self._outer_bounds

    def is_empty(self):
        """
        Returns True if the linked list is empty,
        returns False otherwise
        """
        return self._board_head is None

    def create_board(self, previous=None, cols_count=0, rows_count=0, cols=9, rows=9):
        """
        Creates the game board with specific numbers of rows and columns
        Defaults to ReadMe spec "9 x 9" and Node() objects, but doesn't
        require these.
        """
        # When our col_count = 9 and row_count =9, we've hit the last node.
        # Return the list at that point.
        if cols_count == cols and rows_count == (rows - 1):
            return

        # In the case of an empty list -- create the first object.
        # When we iterate, this will become our previous.
        elif self.is_empty():
            node_object = Node((cols_count, rows_count))
            self.set_head(node_object)
            return self.create_board(self.get_head(), cols_count + 1, rows_count, cols, rows)

        # If previous isn't none, and we haven't overpopulated our col, create a new node
        # in this column. Set the previous node's next to the new node and iterate again
        elif previous is not None and cols_count != cols:
            current = Node((cols_count, rows_count))
            previous.set_next(current)
            return self.create_board(current, cols_count + 1, rows_count, cols, rows)

        # If previous isn't none, but we've overpopulated our col, increment our row first
        # then create a new node in the first column of new row. Set the previous node's
        # next to the new node and iterate again
        elif previous is not None and cols_count == cols:
            cols_count = 0
            rows_count += 1
            current = Node((cols_count, rows_count))
            previous.set_next(current)
            return self.create_board(current, cols_count + 1, rows_count, cols, rows)

    def find_board_node(self, coord_tuple, pos=None):
        """
        Will recursively find the node object associated with the coord_tuple by
        searching through the linked list of our game board and finding the node with
        the corresponding node name. Will return the node.
        """
        # Sets the position parameter to the header (the first in the list)
        if pos is None:
            pos = self.get_head()

        # If pos.get_next() is None, that means we've reached the end of the list.
        if pos.get_next() is None and pos.get_node_name() != coord_tuple:
            return "The node coordinate you're looking for does not exist."

        # If the name matches the coordinate name of the node, return the node
        if pos.get_node_name() == coord_tuple:
            return pos

        # Otherwise iterate through the list.
        else:
            return self.find_board_node(coord_tuple, pos.get_next())

    def find_player_node(self, player_name, pos=None):
        """
        Will recursively find the node object associated with the player name by
        searching through the linked list of our game board and finding the node with
        the corresponding node data. Will return the node.
        """
        # Sets the position parameter to the header (the first in the list)
        if pos is None:
            pos = self.get_head()

        # If pos.get_next() is None, that means we've reached the end of the list.
        if pos.get_next() is None and pos.get_player_data() != player_name:
            return "The Player you're looking for does not exist."

        # If the name matches the coordinate name of the node, return the node
        elif pos.get_player_data() == player_name:
            return pos

        # Otherwise iterate through the list.
        else:
            return self.find_player_node(player_name, pos.get_next())

    def establish_outer_fences(self, pos=None, cols=9, rows=9):
        """
        Takes a linked list. Appends individual nodes for to create the outer fences of
        the game board. Returns the new list of nodes with updated fence options.
        """
        # If pos is none, establish it with the head
        if pos is None:
            pos = self.get_head()

        # Grabs the name of each node.
        node_name = pos.get_node_name()

        # If the .get_next is None, we're at the bottom right of the board.
        # Initiate the bottom and right fence of that node.
        if pos.get_next() is None:
            pos.set_down_wall()
            pos.set_right_wall()
            return

        # Otherwise, grab the x and y coordinate of the node's name
        # and turn on the following fences.
        else:
            x = node_name[0]
            y = node_name[1]

            # If x == 0, we're talking about the left-most row
            if x == 0:
                pos.set_left_wall()

            # If x is between 0 and the number of rows and y is zero,
            # We're talking about the top column
            if y == 0:
                pos.set_up_wall()

            # If x is between 0 and the number of rows and y is our rows,
            # We're talking about the bottom column
            if y == (rows - 1):
                pos.set_down_wall()

            # If x == our cols, we're talking about the right-most row
            if x == (cols - 1):
                pos.set_right_wall()

            return self.establish_outer_fences(pos.get_next())

    def rec_display(self, a_node):
        """Helper function of display. Recursively displays the board
        as a list of node names. Does not account for list of lists."""
        if a_node is None:
            return
        print(a_node.get_node_name(), end=" ")
        self.rec_display(a_node.get_next())

    def display(self):
        """Recursively displays the board as a list of node names.
        Does not account for a list of lists. """
        self.rec_display(self.get_head())

    def to_plain_board(self, pos=None, result=None, cols_count=0, rows_count=0, cols=9, rows=9):
        """
        Recursively returns a bracketed list of lists containing our board values,
        in the same order, as the linked list
        """
        # If our result list doesn't already exist as a list, create it.
        if result is None:
            result = list()
            for row in range(0, rows):
                result.append(list())

        # If our position hasn't been initialized, do so with the header.
        if pos is None:
            pos = self.get_head()

        # pos.next is None implies that we've reached the last value in our list.
        # if so, this is our last append. Then return the result.
        if pos.get_next() is None:
            result[rows_count].append(pos.get_node_name())
            return result

        # Otherwise, append appropriately, and move to the next object node.
        else:
            if cols_count != cols:
                result[rows_count].append(pos.get_node_name())
                return self.to_plain_board(pos.get_next(), result, cols_count + 1, rows_count, cols, rows)

            elif cols_count == cols:
                cols_count = 0
                rows_count += 1
                result[rows_count].append(pos.get_node_name())
                return self.to_plain_board(pos.get_next(), result, cols_count + 1, rows_count, cols, rows)


class Fence:
    """
    Represents a fence object that will block a 1 x 1 move square wall.
    Will be composited into our Player class.
    """

    def __init__(self, direction, creation_point):
        """
        Creation of a dedicated fence with direction and end points
        """
        self._direction = direction
        self._creation_point = creation_point
        self._end_point = None

    def get_direction(self):
        """
        Returns the direction of a Fence object.
        """
        return self._direction

    def get_creation_point(self):
        """
        Returns the creation point of a Fence object.
        """
        return self._creation_point

    def find_end(self, direction, creation_point):
        """Finds the end point of a specified fence."""
        if direction == "v":
            end_point = creation_point[1] + 1
            self.set_end_point((self._creation_point[0], end_point))
            return
        elif direction == "h":
            end_point = creation_point[0] + 1
            self.set_end_point((end_point, self._creation_point[1]))
            return

    def set_end_point(self, end_point):
        """
        Sets the end point of a specific Fence object.
        """
        self._end_point = end_point

    def get_end_point(self):
        """
        Returns the end point of a specific Fence object
        """
        return self._end_point


class Player:
    """
    Represents an individual player's moves, fences, and tokens
    Will be composited into our QuoridorGame class.
    """

    def __init__(self, name, home_position):
        """Creation of a named player, their fences, their home position, and their current position"""
        self._player_name = int(name)
        self._home_position = home_position
        self._fences = None
        self._no_of_fences = 10
        self._current_position = None

    def __repr__(self):
        """The representation of a Player Object"""
        return "Player #: " + repr(self._player_name) + ", Current position: " + repr(self._current_position)

    def get_home_position(self):
        """
        Returns the home position of the player
        """
        return self._home_position

    def get_player_name(self):
        """
        Returns the player's name.
        """
        return self._player_name

    def get_current_position(self):
        """
        Returns the current position of the player.
        """
        return self._current_position

    def set_current_position(self, position):
        """
        Set's the position of the player's current position.
        """
        self._current_position = position

    def get_fences(self):
        """Returns a list of fences the player has set"""
        if self._fences is None:
            self._fences = list()
            return self._fences
        else:
            return self._fences

    def get_no_of_fences(self):
        """Returns the number of fences left to a player"""
        return self._no_of_fences

    def remove_fence(self):
        """Deduction of a fence from a players no. of fences when used"""
        self._no_of_fences -= 1
        return self._no_of_fences

    def add_new_fence(self, direction, pos_tuple):
        """Appends fences list with a new fence input. """
        # If player has available fences:
        fence_list = self.get_fences()

        if self.is_fence_available():

            # Creation of the fence object
            new_fence = Fence(direction, pos_tuple)

            # Finding of our fence end point.
            new_fence.find_end(direction, pos_tuple)
            fence_end = new_fence.get_end_point()

            # Appending the players list of fences with the fence segment.
            # This is for printing
            coordinates = [pos_tuple[0], fence_end[0]], [pos_tuple[1], fence_end[1]]
            fence_list.append(list(coordinates))

            # Deduction of a fence from players total allowed fences.
            self.remove_fence()
            return

        else:
            return False

    def is_fence_available(self):
        """
        Returns True if player object has remaining fences available, False
        if not.
        """
        player_no_feces = self.get_no_of_fences()

        if player_no_feces > 0:
            return True
        else:
            return False


class QuoridorGame:
    """
    Represents the actual gameplay of our Quoridor Game. Will use attributes of our Nodes,
    our Board, our Fences and our Players. Will also be able to print our board.
    """

    def __init__(self):
        """
        Creation and initialization of all attributes of our Quoridor Game.
        """
        # Creation of our game board and outer fences.
        self._game_board = GameBoard()
        self._game_board.create_board()
        self._game_board.establish_outer_fences()

        # Creation of our players
        self._player_1 = Player(1, (4, 0))
        self._player_2 = Player(2, (4, 8))

        self._list_of_players = [None, self._player_1, self._player_2]

        self.initialize_start_positions()

        # Tracker of turns. Will default to player 1.
        self._move_options = [1, 2]
        self._whose_move = self._move_options[0]

    def initialize_start_positions(self):
        """
        Adjusts the nodes of the players start position to reflect their current position.
        """
        # Defines variables
        p1 = self._player_1
        p2 = self._player_2

        # Obtains players starting positions
        p1_home = p1.get_home_position()
        p2_home = p2.get_home_position()

        # Sets the player's current position to their home position.
        self._player_1.set_current_position(p1_home)
        self._player_2.set_current_position(p2_home)

        # Finds their respective nodes.
        p1_node = self._game_board.find_board_node(p1_home)
        p2_node = self._game_board.find_board_node(p2_home)

        # Updates the nodes corresponding player data.
        p1_node.set_player_data(p1.get_player_name())
        p2_node.set_player_data(p2.get_player_name())

    def get_game_board(self):
        """
        Returns the game board
        """
        return self._game_board

    def get_player_1(self):
        """
        Returns Player 1 object
        """
        return self._player_1

    def get_player_2(self):
        """
        Returns Player 1 object
        """
        return self._player_2

    def get_whose_move(self):
        """
        Returns whose move it is. Will be used to test whether tokens are allowed
        to move.
        """
        return self._whose_move

    def set_whose_move(self):
        """
        Allows us to change whose move is next. Will update at the end of a valid move
        Will not change if move is invalid. Will default to player 1
        """
        if self.get_whose_move() == 1:
            self._whose_move = self._move_options[1]
        else:
            self._whose_move = self._move_options[0]

    def get_opposing_player(self, player):
        if player == 1:
            opposing_player = self._player_2
        else:
            opposing_player = self._player_1

        return opposing_player

    def is_winner(self, player):
        """
        Takes a player number integer and returns True if the player has won or False
        if they have not yet won.
        """
        game_board = self._game_board

        if player == 1:
            list_of_nodes = game_board.get_p1_winning_area()
        else:
            list_of_nodes = game_board.get_p2_winning_area()

        for node in list_of_nodes:
            temp_node = game_board.find_board_node(node)

            if temp_node.get_player_data() == player:
                return True
        else:
            return False

    def is_player_turn(self, player):
        """
        Returns True is proposed player is current player, otherwise
        Returns False.
        """
        if player == self._whose_move:
            return True
        else:
            return False

    def is_on_board(self, coord_tuple):
        """
        Returns True if proposed move is on the board. Otherwise
        returns False.
        """
        game_board = self._game_board.get_outer_bounds()

        if game_board[0][0] <= coord_tuple[0] <= game_board[1][0] and \
                game_board[0][1] <= coord_tuple[1] <= game_board[1][1]:
            return True
        else:
            return False

    def get_lcd_direction(self, current_position, prop_move):
        """
        Subtracts the proposed move from the players current space to get the direction
        of the player's trajectory
        """
        # "LCD" is lowest common denominator

        lcd_of_travel = ((prop_move[0] - current_position[0]), (prop_move[1] - current_position[1]))

        if lcd_of_travel == (0, 0):
            raise YouAlreadyLiveHereError()

        else:
            travel_basis = {
                (0, -1): "up",
                (0, 1): "down",
                (1, 0): "right",
                (-1, 0): "left",
                (1, -1): "up-right",
                (-1, -1): "up-left",
                (1, 1): "down-right",
                (-1, 1): "down-left"
            }

        if lcd_of_travel in travel_basis:
            return travel_basis[lcd_of_travel]
        elif lcd_of_travel[0] == 0 and lcd_of_travel[1] == 2 or lcd_of_travel[1] == -2:
            lcd_of_travel = (lcd_of_travel[0], (lcd_of_travel[1] / 2))
            return travel_basis[lcd_of_travel]
        else:
            return False

    def move_type(self, player, coord_tuple):
        """
        Determines what kind of move we're dealing with:
        Simple - basic cardinal direction (up, down, left, right)
        Diagonal - Off-axis of cardinal direction
        Complicated - includes a jump of some variety
        """
        move_type = ["SIMPLE", "DIAGONAL", "COMPLICATED"]

        current_node = self._game_board.find_player_node(player)

        node_name = current_node.get_node_name()

        try:
            self.get_lcd_direction(node_name, coord_tuple)
        except YouAlreadyLiveHereError:
            return False
        else:
            prop_move_direction = self.get_lcd_direction(node_name, coord_tuple)

            if prop_move_direction and prop_move_direction in ("up", "down", "left", "right"):
                return move_type[0]

            elif prop_move_direction and prop_move_direction in ("up-left", "up-right", "down-left", "down-right"):
                return move_type[1]

            else:
                return move_type[2]

    def up_or_down(self, prop_move_direction):
        """
        Determines if we're moving up or down the board.
        """
        if "up" in prop_move_direction:
            return "up"

        elif "down" in prop_move_direction:
            return "down"

        else:
            return False

    def opposite_direction(self, direction):
        """
        Returns the opposite direction of a given direction
        """
        if direction == "up":
            return "down"
        elif direction == "down":
            return "up"
        elif direction == "left":
            return "right"
        else:
            return "left"

    def wall_player_existence(self, direction, current_node, opposing_player):
        """
        Determines if a wall exists in the user_entered direction.
        """
        temp_node = self._game_board.find_board_node(current_node.get_nearby_nodes()[direction])
        temp_node_player_data = temp_node.get_player_data()

        if temp_node.get_list_of_walls()[direction] is True and \
                temp_node_player_data is opposing_player.get_player_name():
            return True
        else:
            return False

    def is_valid_simple_move(self, player, coord_tuple):
        """
        Does the work to determine if a simple move is valid.
        valid means no blocking walls and no opposing player data.
        """
        current_node = self._game_board.find_player_node(player)
        proposed_node = self._game_board.find_board_node(coord_tuple)
        proposed_node_data = proposed_node.get_player_data()

        current_walls = current_node.get_list_of_walls()
        prop_move_direction = self.get_lcd_direction(current_node.get_node_name(), coord_tuple)

        if current_walls[prop_move_direction] is False and proposed_node_data is None:
            return True
        else:
            return False

    def is_valid_diag_move(self, player, coord_tuple):
        """
        Does the work to determine if a diagonal move is valid.
        valid means no blocking walls: up and right/left or down and right/left
        and no opposing player data.
        """
        # The variables we'll use.
        current_node = self._game_board.find_player_node(player)
        proposed_node = self._game_board.find_board_node(coord_tuple)
        proposed_node_data = proposed_node.get_player_data()
        opposing_player = self.get_opposing_player(player)
        opposing_player_node = self._game_board.find_player_node(opposing_player.get_player_name())

        # Sets all nearby nodes of the current node and determines our direction.
        current_node.set_nearby_nodes()
        prop_move_direction = self.get_lcd_direction(current_node.get_node_name(), coord_tuple)

        # Step 1: Determine if the player is traversing up or down.
        temp_direction = self.up_or_down(prop_move_direction)

        # Step 2: Determine if a player and a wall exists in said direction
        does_wall_player_exist = self.wall_player_existence(temp_direction, current_node, opposing_player)

        # Step 3: Determine opposite direction
        opp_dir = self.opposite_direction(temp_direction)

        if does_wall_player_exist and proposed_node_data is None:
            node_walls = opposing_player_node.get_list_of_walls()
            if "left" in prop_move_direction and node_walls[opp_dir] is False and node_walls["left"] is False:
                return True
            elif "right" in prop_move_direction and node_walls[opp_dir] is False and node_walls["right"] is False:
                return True
            else:
                return False
        else:
            return False

    def is_valid_comp_move(self, player, coord_tuple):
        """
        Does the work to determine if a complicated move is valid.
        valid means the opposing player is in a space above or below the player token
        and no wall exists beyond the opposing player's token.
        """
        # The variables we'll use.
        current_node = self._game_board.find_player_node(player)
        proposed_node = self._game_board.find_board_node(coord_tuple)
        opposing_player = self.get_opposing_player(player)
        opp_player_node = self._game_board.find_player_node(opposing_player.get_player_name())

        # Sets all nearby nodes of the current node and determines our direction.
        current_node.set_nearby_nodes()

        try:
            self.get_lcd_direction(current_node.get_node_name(), coord_tuple)
        except YouAlreadyLiveHereError:
            return False
        else:
            prop_move_direction = self.get_lcd_direction(current_node.get_node_name(), coord_tuple)

            # Step 1: Determine if the player is traversing up or down.
            try:
                self.up_or_down(prop_move_direction)
            except TypeError:
                return False
            else:
                temp_direction = self.up_or_down(prop_move_direction)

                # Step 2: Determine if the opposing player is above or below the player token
                temp_node = self._game_board.find_board_node(current_node.get_nearby_nodes()[temp_direction])
                temp_node_player_data = temp_node.get_player_data()
                opp_dir = self.opposite_direction(temp_direction)

                # Step 3: Make sure the node above is the opposing player's node.
                if temp_node_player_data == opposing_player.get_player_name():

                    # If true, find the node above the opposing player node.
                    # Confirm this is the node they're proposing to move to and that it is
                    # empty of player data.
                    new_temp_node = self._game_board.find_board_node(opp_player_node.get_nearby_nodes()[temp_direction])
                    if new_temp_node is proposed_node and new_temp_node.get_nearby_walls()[opp_dir] is False and \
                            new_temp_node.get_player_data is None:
                        return True
                    else:
                        return False
                else:
                    return False

    def make_move(self, player, coord_tuple):
        """
        Does all the work when a move is checked as valid.
        """
        proposed_node = self._game_board.find_board_node(coord_tuple)
        current_node = self._game_board.find_player_node(player)
        active_player = self._list_of_players[player]

        proposed_node.set_player_data(player)
        current_node.set_player_data(None)

        active_player.set_current_position(coord_tuple)
        self.set_whose_move()
        return True

    def move_pawn(self, player, coord_tuple):
        """
        Takes an integer that represents which player (1 or 2) is making the move
        and a tuple with the coordinates of where they plan to move. Checks to see
        if it's their turn, that it's a valid move, and if it forces a win of the game.
        Updates the node of the new position to reflect the player token.
        """
        # If the game has been won, return False; otherwise, continue.
        if self.is_winner(1) is False and self.is_winner(2) is False:

            # It needs to be the correct players turn, and the move needs to be
            # on the board.
            if self.is_player_turn(player) and self.is_on_board(coord_tuple):

                # Determine what type of move we're doing.
                move_type = self.move_type(player, coord_tuple)

                if move_type == "SIMPLE":
                    if self.is_valid_simple_move(player, coord_tuple):
                        self.make_move(player, coord_tuple)
                        return True
                    else:
                        return False

                elif move_type == "DIAGONAL":
                    if self.is_valid_diag_move(player, coord_tuple):
                        self.make_move(player, coord_tuple)
                        return True
                    else:
                        return False
                else:
                    if self.is_valid_comp_move(player, coord_tuple):
                        self.make_move(player, coord_tuple)
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    def place_fence(self, player, fence_direction, coord_tuple):
        """
        Takes an integer that represents which player (1 or 2) is placing the fence. Checks
        whether or not there is already a fence in that position or that it is a valid fence
        placement. Updates the players list of fence placements for printing and docs one of the
        players remaining available fences.
        """
        # If the game has been won, return False; otherwise, continue.
        if self.is_winner(1) is False and self.is_winner(2) is False:

            # It needs to be the correct players turn, and the move needs to be
            # on the board.
            if self.is_player_turn(player) and self.is_on_board(coord_tuple):
                active_player = self._list_of_players[player]
                active_node = self._game_board.find_board_node(coord_tuple)

                # If it's a vertical wall and there isn't one already on left:
                # Create the fence. Find the node - set it's left wall. Find the node
                # to the left and set it's right wall (which is the same wall).
                # Update player token at end of turn.
                if fence_direction == "v" and active_node.get_left_wall() is False:
                    active_player.add_new_fence(fence_direction, coord_tuple)
                    active_node.set_left_wall()
                    active_node.set_nearby_nodes()
                    one_left = active_node.get_nearby_nodes()["left"]  # Pulls one node left
                    new_node = self._game_board.find_board_node(one_left)
                    new_node.set_right_wall()
                    self.set_whose_move()
                    return True

                # If it's a horizontal wall and there isn't one already on top:
                # Create the fence. Find the node - set it's top wall. Find the node
                # above and set it's bottom wall (which is the same wall).
                # Update player token at end of turn.
                elif fence_direction == "h" and active_node.get_up_wall() is False:
                    active_player.add_new_fence(fence_direction, coord_tuple)
                    active_node.set_up_wall()
                    active_node.set_nearby_nodes()
                    one_up = active_node.get_nearby_nodes()["up"]  # Pulls one node above
                    new_node = self._game_board.find_board_node(one_up)
                    new_node.set_down_wall()
                    self.set_whose_move()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def print_board(self):
        """
        Grabs the data from our list of players regarding their current positions and their fence
        placements as segments. Prints via pyplot the list of line segments as walls and the current
        positions of the players as (0.5, 0.5) offset from a players current index. Grid will be on and
        I will ask for the x, y study to include from (0,0) to (8,8) and each players fences and token
        will be a separate color.
        """

        import matplotlib.pyplot as pyplt

        player_1_fences = self._player_1.get_fences()
        player_2_fences = self._player_2.get_fences()

        pyplt.xlim([0, 9])
        pyplt.ylim([9, 0])

        pyplt.grid("on")

        p1_location = self.get_player_1().get_current_position()
        p2_location = self.get_player_2().get_current_position()

        pyplt.plot((p1_location[0] + 0.5), (p1_location[1] + 0.5), 'ro', label="P1")
        pyplt.plot((p2_location[0] + 0.5), (p2_location[1] + 0.5), 'bo', label="P2")

        for segment in player_1_fences:
            x1 = segment[0]
            y1 = segment[1]
            pyplt.plot(x1, y1, '-ro')

        for segment in player_2_fences:
            x1 = segment[0]
            y1 = segment[1]
            pyplt.plot(x1, y1, '-bo')

        pyplt.legend()
        pyplt.show()


def main():
    """Tests for Game, will not run if imported"""
    q = QuoridorGame()

    print(q.move_pawn(1, (4, 1)))

    print(q.move_pawn(2, (5, 8)))

    print(q.place_fence(1, "v", (7, 6)))

    print(q.move_pawn(2, (5, 8)))

    print(q.place_fence(2, "h", (2, 5)))

    print(q.place_fence(1, "h", (3, 3)))

    print(q.place_fence(2, "h", (0, 3)))

    print(q.move_pawn(1, (4, 2)))

    print(q.move_pawn(2, (4, 7)))

    print(q.move_pawn(2, (4, 8)))

    print(q.move_pawn(1, (4, 3)))

    print(q.move_pawn(2, (5, 7)))

    print(q.move_pawn(2, (4, 7)))

    print(q.move_pawn(1, (4, 4)))

    print(q.move_pawn(2, (4, 6)))

    print(q.place_fence(1, "h", (4, 4)))

    print(q.move_pawn(2, (4, 5)))

    print(q.place_fence(1, "v", (0, 0)))

    print(q.place_fence(1, "v", (4, 0)))

    print(q.move_pawn(2, (5, 4)))

    print(q.move_pawn(1, (6, 4)))

    print(q.place_fence(1, "h", (5, 4)))

    print(q.move_pawn(2, (6, 4)))

    print(q.move_pawn(1, (4, 5)))

    print(q.move_pawn(2, (6, 3)))

    print(q.move_pawn(1, (4, 6)))

    # q.print_board()


if __name__ == '__main__':
    main()
