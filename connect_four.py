connect_4_games = {}

class Board:
    # Values:
    white = 1
    red = 2
    blue = 3

    rows = [[],[],[],[],[],[],[]]   # 6 rows
                                    # 7 columns

    def printBoard(self):
        string = ""
        for rowInd in range(0, 6):
            row = self.rows[rowInd]

            for valueInd in range(0, 7):
                value = row[valueInd]
                if value == self.white:
                    string += ":white_circle:"
                elif value == self.red:
                    string += ":red_circle:"
                elif value == self.blue:
                    string += ":blue_circle:"
                else:
                    print(f"Internal Error : Connect 4 : Unknown value code {value}")

                if rowInd != 5:
                    string += "\n"  # Insert a new line

    def getBelow(self, RowInd, ColumnInd):
        # Returns whats below the cell

        if ColumnInd == 6:
            return None
        
        row = self.rows[RowInd]
        return row[ColumnInd + 1], RowInd, ColumnInd + 1

    def getAbove(self, RowInd, ColumnInd):
        # Returns whats above the cell
        
        if ColumnInd == 0:
            return None

        row = self.rows[RowInd]
        return row[ColumnInd - 1], RowInd, ColumnInd - 1

    def getLeft(self, RowInd, ColumnInd):
        # Returns whats to the left of the cell
        
        if RowInd == 0:
            return None
        
        row = self.rows[RowInd - 1]
        return row[ColumnInd], RowInd - 1, ColumnInd

    def getRight(self, RowInd, ColumnInd):
        # Returns whats to the right of the cell

        if RowInd == 5:
            return None

        row = self.rows[RowInd + 1]
        return row[ColumnInd], RowInd + 1, ColumnInd

    def getTopLeft(self, RowInd, ColumnInd):
        top, trow, tcol = self.getAbove(RowInd, ColumnInd)

        if top == None:
            return None

        return self.getLeft(trow, tcol)

    def getTopRight(self, RowInd, ColumnInd):
        top, trow, tcol = self.getAbove(RowInd, ColumnInd)

        if top == None:
            return None

        return self.getRight(trow, tcol)

    def getBottomLeft(self, RowInd, ColumnInd):
        bottom, brow, bcol = self.getBelow(RowInd, ColumnInd)

        if bottom == None:
            return None

        return self.getLeft(brow, bcol)
    def getBottomRight(self, RowInd, ColumnInd):
        bottom, brow, bcol = self.getBelow(RowInd, ColumnInd)

        if bottom == None:
            return None

        return self.getRight(brow, bcol)
            
    def fill(self, RowInd, ColumnInd, valueNum):
        # Fill a specific cell

        self.rows[RowInd][ColumnInd] = valueNum

    def fillDefault(self):
        # Fills the board with all whites 
        for rowInd in range(0, 6):
            for colInd in range(0, 7):
                self.fill(rowInd, colInd, self.white)


        
        