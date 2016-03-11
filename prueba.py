class a:
    def __init__(self):
        self.a = 1
        print('aki')

    def b(self):
        self.a += 1


class b(a):
    def __init__(self):
        super(b, self).__init__()
        super(a, self).__init__()
        print(self.a)

b()