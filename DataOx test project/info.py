class Info:

    def __init__(self, row):
        self.date = row[0]
        self.open = row[1]
        self.high = row[2]
        self.low = row[3]
        self.close = row[4]
        self.adj_close = row[5]
        self.volume = row[6]