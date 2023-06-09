# Author: Michelle Mann
# Date: 08/03/2021
# Description: Unit Test for Quoridor

import unittest
from Quoridor import Node, GameBoard, Fence, Player, QuoridorGame


class TestQuoridor(unittest.TestCase):
    """Contains the unit test for Library"""

    def test_create_Node(self):
        """
        Tests whether Node class creates objects correctly.
        Specifically tests all get methods
        """

        # Creation of our item.
        item_1 = Node((1, 1))

        item_1.set_player_data("P1")

        # Calls all get methods for item.
        name = item_1.get_node_name()
        data = item_1.get_player_data()
        up = item_1.get_up_wall()
        down = item_1.get_down_wall()
        left = item_1.get_left_wall()
        right = item_1.get_right_wall()

        item_1.set_nearby_nodes()
        nearby_nodes = item_1.get_nearby_nodes()

        # Populates a result variable with all get methods
        result = [name, data, up, down, left, right]
        result_2 = nearby_nodes
        test = [(1, 1), "P1", False, False, False, False]
        test_2 = {"up": (1, 0),
                  "down": (1, 2),
                  "right": (2, 1),
                  "left": (0, 1),
                  "up-right": (2, 0),
                  "up-left": (0, 0),
                  "down-right": (2, 2),
                  "down-left": (0, 2)
                  }

        # Asserts that the get methods are equal to our test baseline.
        self.assertEqual(result, test)
        self.assertEqual(result_2, test_2)

    def test_game_board_object(self):
        """
        Tests all get/set methods for a game board object.
        """

        board_1 = GameBoard()

        result_1 = board_1.is_empty()
        test_1 = True

        board_1.create_board(cols=4, rows=4)

        node_1 = board_1.get_head()
        result_2 = node_1.get_node_name()

        test_2 = (0, 0)

        result_3 = board_1.get_p1_winning_area()
        test_3 = [(0, 8),
                  (1, 8),
                  (2, 8),
                  (3, 8),
                  (4, 8),
                  (5, 8),
                  (6, 8),
                  (7, 8),
                  (8, 8)
                  ]

        result_4 = board_1.get_p2_winning_area()
        test_4 = [(0, 0),
                  (1, 0),
                  (2, 0),
                  (3, 0),
                  (4, 0),
                  (5, 0),
                  (6, 0),
                  (7, 0),
                  (8, 0)
                  ]

        result_5 = board_1.get_outer_bounds()
        test_5 = [(0, 0), (8, 8)]

        self.assertEqual(result_1, test_1)
        self.assertEqual(result_2, test_2)
        self.assertEqual(result_3, test_3)
        self.assertEqual(result_4, test_4)
        self.assertEqual(result_5, test_5)

    def test_create_gameboard_1(self):
        """
        Tests whether GameBoard class creates a predictable game board.
        """

        board_1 = GameBoard()

        board_1.create_board(cols=4, rows=4)

        result = board_1.to_plain_board(cols=4, rows=4)

        test_1 = [[(0, 0), (1, 0), (2, 0), (3, 0)],
                  [(0, 1), (1, 1), (2, 1), (3, 1)],
                  [(0, 2), (1, 2), (2, 2), (3, 2)],
                  [(0, 3), (1, 3), (2, 3), (3, 3)]]

        self.assertEqual(result, test_1)

    def test_game_board_walls(self):
        """
        Tests whether GameBoard class initializes walls correctly. Tests
        the find_node method to confirm walls of the board work.
        """

        board_1 = GameBoard()

        board_1.create_board()

        board_1.establish_outer_fences()

        # Testing the find_board_node methods
        # Confirming that find_board_node returns nodes
        # and not data.
        node_1 = board_1.find_board_node((0, 0))  # Tests a corner node.
        node_2 = board_1.find_board_node((2, 0))  # Tests a node at the top.
        node_3 = board_1.find_board_node((8, 1))  # Tests a far right node.
        node_4 = board_1.find_board_node((0, 3))  # Tests a far left node.
        node_5 = board_1.find_board_node((10, 5))  # Tests a node that DNE

        # Testing the the find method for a node that does not exist.
        result = node_5

        # Testing updating the Nodes that fences are correctly updating.
        # Testing the walls around node_1
        result_1 = node_1.get_left_wall()
        result_2 = node_1.get_right_wall()
        result_3 = node_1.get_up_wall()
        result_4 = node_1.get_down_wall()

        # Testing the walls around node_2
        result_5 = node_2.get_left_wall()
        result_6 = node_2.get_right_wall()
        result_7 = node_2.get_up_wall()
        result_8 = node_2.get_down_wall()

        # Testing the walls around node_3
        result_9 = node_3.get_left_wall()
        result_10 = node_3.get_right_wall()
        result_11 = node_3.get_up_wall()
        result_12 = node_3.get_down_wall()

        # Testing the walls around node_4
        result_13 = node_4.get_left_wall()
        result_14 = node_4.get_right_wall()
        result_15 = node_4.get_up_wall()
        result_16 = node_4.get_down_wall()

        test_1 = ["The node coordinate you're looking for does not exist."]
        test_2 = [True, False, True, False]
        test_3 = [False, False, True, False]
        test_4 = [False, True, False, False]
        test_5 = [True, False, False, False]

        self.assertEqual([result], test_1)
        self.assertEqual([result_1, result_2, result_3, result_4], test_2)
        self.assertEqual([result_5, result_6, result_7, result_8], test_3)
        self.assertEqual([result_9, result_10, result_11, result_12], test_4)
        self.assertEqual([result_13, result_14, result_15, result_16], test_5)

    def test_find_player(self):
        """
        Tests find_player_node in GameBoard class.
        """
        # Creation of a game board.
        board_1 = GameBoard()

        # Creation of all the nodes in a game board.
        board_1.create_board(cols=4, rows=4)

        # Setting a node's player data to a specific node.
        node_1 = board_1.find_board_node((0, 3))
        node_1.set_player_data("P1")

        # Finding a specific node based on player data
        node_2 = board_1.find_player_node("P1")

        # Testing the find method for a player that DNE
        node_3 = board_1.find_player_node("P2")

        result = node_2.get_node_name()
        test_1 = (0, 3)

        result_2 = node_3
        test_2 = "The Player you're looking for does not exist."

        self.assertEqual(result, test_1)
        self.assertEqual(result_2, test_2)

    def test_create_fence(self):
        """
        Tests all the get/set methods on a Fence object
        """
        # creation of a Fence object
        fence_1 = Fence("v", (1, 1))
        fence_2 = Fence("h", (1, 1))

        # confirms get method for creation point works.
        result_1 = fence_1.get_creation_point()

        # Confirms get method for direction works
        result_2 = fence_1.get_direction()

        # Confirms method for finding the endpoint of a Fence works.
        fence_1.find_end(result_2, result_1)
        fence_2.find_end("h", (1, 1))

        # Confirms the get method for the end point works.
        result_3 = fence_1.get_end_point()
        result_4 = fence_2.get_end_point()

        test_1 = (1, 1)
        test_2 = "v"
        test_3 = (1, 2)
        test_4 = (2, 1)

        self.assertEqual(result_1, test_1)
        self.assertEqual(result_2, test_2)
        self.assertEqual(result_3, test_3)
        self.assertEqual(result_4, test_4)

    def test_create_player(self):
        """
        Tests all the get methods on a Player object
        """
        player_1 = Player(1, (4, 0))

        player_home = player_1.get_home_position()
        player_fences = player_1.get_fences()
        player_no_fences = player_1.get_no_of_fences()

        result_1 = [player_home, player_fences, player_no_fences]
        test_1 = [(4, 0), [], 10]

        self.assertEqual(result_1, test_1)

    def test_create_player_fences(self):
        """
        Tests all the functionality of a player's Fence list.
        """
        player_1 = Player(1, (4, 0))
        player_fences = player_1.get_fences()

        player_1.add_new_fence("v", (1, 1))

        result_2 = player_1.get_fences()
        test_2 = [[[1, 1], [1, 2]]]

        self.assertEqual(result_2, test_2)

        fence_2 = player_1.add_new_fence("v", (1, 2))
        fence_3 = player_1.add_new_fence("v", (1, 3))
        fence_4 = player_1.add_new_fence("v", (1, 4))
        fence_5 = player_1.add_new_fence("v", (1, 5))
        fence_6 = player_1.add_new_fence("v", (1, 6))
        fence_7 = player_1.add_new_fence("v", (1, 7))
        fence_8 = player_1.add_new_fence("v", (2, 1))
        fence_9 = player_1.add_new_fence("v", (2, 2))
        fence_10 = player_1.add_new_fence("v", (2, 3))

        result_3 = player_1.get_fences()

        test_3 = [[[1, 1], [1, 2]],
                  [[1, 1], [2, 3]],
                  [[1, 1], [3, 4]],
                  [[1, 1], [4, 5]],
                  [[1, 1], [5, 6]],
                  [[1, 1], [6, 7]],
                  [[1, 1], [7, 8]],
                  [[2, 2], [1, 2]],
                  [[2, 2], [2, 3]],
                  [[2, 2], [3, 4]]]

        result_4 = player_1.add_new_fence("v", (2, 4))
        test_4 = False

        self.assertEqual(result_3, test_3)
        self.assertEqual(result_4, test_4)

    def test_game_play(self):
        """
        Tests the initialization of the game play.
        """
        # Creation of a game board
        q = QuoridorGame()
        # Confirm get player methods work.
        print(q.get_player_1())
        print(q.get_player_2())

        # Create a variable for the gameboard.
        gb = q.get_game_board()

        # Create a variable for our first node.
        # Confirm find_board_node works by finding player data
        # associated with node.
        node_1 = gb.find_board_node((4, 0))
        print(node_1.get_player_data())

        node_2 = gb.find_board_node((4, 8))
        print(node_2.get_player_data())

        # Confirm the find_player method works.
        print(gb.find_player_node(1))

        # Test a failed move attempt. Currently player 1's turn.
        print(q.move_pawn(2, (4, 7)))

        # Test a valid move.
        print(q.move_pawn(1, (4, 1)))

        # Confirm player's token's reflect new move.
        print(q.get_player_1())
        print(q.get_player_2())
        # Confirm make_move is updating whose turn it is.
        print(q.get_whose_move())

        # Attempt to place fence not on a turn.
        print(q.place_fence(1, 'h', (6, 5)))

        # Attempt a valid move for player 2
        print(q.move_pawn(2, (4, 7)))

        # Confirm player's tokens reflect new move.
        print(q.get_player_1())
        print(q.get_player_2())

        # Attempt to place a fence on valid turn.
        print(q.place_fence(1, 'h', (6, 5)))

        # Confirms all aspects of fence are accurate.
        # Confirms Player fence data is updated.
        node_3 = gb.find_board_node((6, 5))
        print(node_3)
        print(node_3.get_up_wall())
        print(node_3.get_list_of_walls())
        player_1 = q.get_player_1()
        print(player_1.get_fences())
        print(player_1.get_no_of_fences())

        # Confirms update on whose move after fence placement.
        print(q.get_whose_move())

        # Confirms valid fence placement with vertical fence.
        print(q.place_fence(2, 'v', (3, 3)))
        node_4 = gb.find_board_node((3, 3))
        print(node_4)
        print(node_4.get_left_wall())
        print(node_4.get_list_of_walls())
        player_2 = q.get_player_2()
        print(player_2.get_fences())
        print(player_2.get_no_of_fences())

        print(q.is_winner(1))
        print(q.is_winner(2))

        print(q.move_pawn(1, (4, 2)))

        print(q.move_pawn(2, (4, 6)))

        print(q.get_whose_move())

        print(q.get_player_1())
        print(q.get_player_2())

        print(q.move_pawn(1, (4, 3)))
        print(q.move_pawn(2, (4, 5)))

        print(q.get_player_1())
        print(q.get_player_2())

        print(q.place_fence(1, "h", (4, 3)))
        print(player_1.get_fences())

        print(q.move_pawn(2, (4, 4)))

        print(q.place_fence(1, "v", (7, 6)))

        print(q.move_pawn(2, (5, 3)))
        print(q.get_player_1())
        print(q.get_player_2())

















