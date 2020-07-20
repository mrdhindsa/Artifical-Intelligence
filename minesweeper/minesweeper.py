import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # {A,B,C} = 2 and C is a mine -> {A,B} = 1
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # {A,B,C} = 2 and C is safe -> {A,B} = 2
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # Set of all possible moves, used by make random move
        self.allMoves = set()
        for h in range(self.height):
            for w in range(self.width):
                self.allMoves.add((h, w))

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # (1) Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # (2) Mark the cell as safe
        self.mark_safe(cell)

        # (3) Add a new sentence based on the value of cell and count
        Neighbors = self.neighbors(cell)
        # Remove known mines
        for n in Neighbors.intersection(self.mines):
            Neighbors.remove(n)
            count -= 1
        newSentence = Sentence(cells=Neighbors, count=count)
        self.knowledge.append(newSentence)

        # (4) Traverse knowledge base and mark cells and safe/mine if possible
        for sentence in self.knowledge.copy():
            m, s = sentence.known_mines(), sentence.known_safes()
            if m:
                for mine in m.copy():
                    self.mark_mine(mine)
                self.knowledge.remove(sentence)
            if s:
                for safe in s.copy():
                    self.mark_safe(safe)
                self.knowledge.remove(sentence)        

        # (5) {A,B,C} = 1 and {A,B,C,D,E} = 2 -> {D,E} = 1
        cknowledge = self.knowledge.copy()
        for sentence1 in cknowledge:
            for sentence2 in cknowledge:
                if(sentence1 != sentence2 and cell in sentence1.cells and cell in sentence2.cells and sentence1.cells.issubset(sentence2.cells)):
                    newSen = Sentence(sentence2.cells - sentence1.cells, sentence2.count-sentence1.count)
                    self.knowledge.append(newSen)

    def neighbors(self, cell):
        """
        Returns a set of valid neighbors of cell. 
        """
        to_return = set()
        directions = [(-1,-1), # Diagonal - Up Left
                      (-1,0),  # Up
                      (-1,1),  # Diagonal - Up Right
                      (0,-1),  # Left
                      (0,1),   # Right
                      (1,-1),  # Diagonal - Down Left
                      (1,0),   # Down
                      (1,1)]   # Diagonal - Down Right
        row, col = cell[0], cell[1]
        for i, j in directions:
            newcell = (row + i, col + j)
            if (self.inbound(newcell) and newcell not in self.safes): # Checking for all possible neighbors of cell that are not known_safe
                to_return.add(newcell)
        return to_return

    def inbound(self, t):
        """
        Returns a bool if tuple t (i,j) is a valid coordinate on the board.
        """
        i, j = t[0], t[1]
        return i >= 0 and i < self.height and j >= 0 and j < self.width

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        moves = self.safes - self.moves_made
        if moves:
            return random.choice(tuple(moves))
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        moves = self.allMoves - self.moves_made - self.mines
        if moves:
            return random.choice(tuple(moves))
        else:
            return None