class Pixel:
    def __init__(self, r=0, g=0, b=0) -> None:
        self.red = r
        self.green = g
        self.blue = b
        pass

    def __eq__(self, __o: object) -> bool:
        return self.red == __o.red and self.green == __o.green and self.blue == __o.blue
