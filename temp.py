if piece == 0:
            if self.rotation == 0:
                return ((x-1,y),(x,y),(x+1,y),(x+2,y))
            elif self.rotation == 1:
                return ((x,y-1),(x,y),(x,y+1),(x,y)+2)
            elif self.rotation == 2:
                return ((x-2,y),(x-1,y),(x,y),(x+1,y))
            elif self.rotation == 3:
                return ((x,y-2),(x,y-1),(x,y),(x,y+1))
        elif piece == 1:
            return ((x,y),(x,y+1),(x+1,y),(x+1,y+1))
        elif piece == 2:
            if self.rotation == 0:
                return ((x-1,y),(x,y),(x+1,y),(x,y+1))
            elif self.rotation == 1:
                return ((x,y+1),(x,y),(x,y-1),(x-1,y))
            elif self.rotation == 2:
                return ((x-1,y),(x,y),(x+1,y),(x,y-1))
            elif self.rotation == 3:
                return ((x,y+1),(x,y),(x,y-1),(x+1,y))
        elif piece == 3:
            if self.rotation == 0:
                return ((x-1,y),(x,y),(x+1,y),(x-1,y-1))
            elif self.rotation == 1:
                return ((x+1,y-1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation == 2:
                return ((x-1,y),(x,y),(x+1,y),(x+1,y+1))
            elif self.rotation == 3:
                return ((x-1,y+1),(x,y+1),(x,y),(x,y-1))
        elif piece == 4:
            if self.rotation == 0:
                return ((x-1,y),(x,y),(x+1,y),(x+1,y-1))
            elif self.rotation == 1:
                return ((x+1,y+1),(x,y+1),(x,y),(x,y-1))
            elif self.rotation == 2:
                return ((x-1,y),(x,y),(x+1,y),(x-1,y+1))
            elif self.rotation == 3:
                return ((x-1,y-1),(x,y+1),(x,y),(x,y-1))
        elif piece == 5:
            if self.rotation == 0:
                return ((x,y),(x+1,y),(x,y-1),(x-1,y+1))
            elif self.rotation == 1:
                return ((x-1,y-1),(x-1,y),(x,y),(x,y+1))
            elif self.rotation == 2:
                return ((x-1,y),(x,y-1),(x,y),(x+1,y-1))
            elif self.rotation == 3:
                return ((x,y+1),(x,y),(x+1,y),(x+1,y+1))
        elif piece == 6:
            if self.rotation == 0:
                return ((x-1,y),(x,y),(x,y-1),(x+1,y+1))
            elif self.rotation == 1:
                return ((x,y-1),(x,y),(x-1,y),(x-1,y+1))
            elif self.rotation == 2:
                return ((x-1,y-1),(x,y-1),(x,y),(x+1,y))
            elif self.rotation == 3:
                return ((x,y+1),(x,y),(x+1,y),(x+1,y-1))