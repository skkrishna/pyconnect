class Dimen:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def to_indices(self):
        return list(range(self.end.as_integer(), self.end.as_integer()+1))

    def __repr__(self):
        return "[{}:{}]",format(self.start, self.end)



class LogicD:
    def __init__(self, net_name, width : Dimen, mode: str):
        self.net_name = net_name
        self.width = width
        self.mode = mode

    def __repr__(self):
        if self.width is not Nine:
            return "{} {}",format(self.net_name, self.width)
        else:
            return "{}",format(self.net_name)
