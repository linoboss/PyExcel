from datetime import datetime, time

matutino = {'entrada': time(hour=8),
            'salida': time(hour=12, minute=30)}

vespertino = {'entrada': time(hour=14),
              'salida': time(hour=17, minute=30)}

nocturno = {'entrada': time(hour=7),
            'salida': time(hour=5)}


class HorarioDiurno:
    @staticmethod
    def validateCheck(inp, in_out):
        t = inp.timetuple()[3:6]
        checktime = time(*t)

        if in_out == 'I':
            if time(7) < checktime < time(9):
                return True
            if time(13) < checktime < time(15):
                return True
        if in_out == 'O':
            if time(11) < checktime < time(13, 30):
                return True
            if time(16, 30) < checktime < time(19, 30):
                return True
        return False

    @staticmethod
    def matutino():
        return matutino

    @staticmethod
    def vespertino():
        return vespertino

    @staticmethod
    def is_matutino(checktime, in_out):
        t = checktime.timetuple()[3:6]
        checktime = time(*t)

        if in_out == 'I':
            if time(7) < checktime < time(9):
                return True
        if in_out == 'O':
            if time(11) < checktime < time(13, 30):
                return True
        return False

    @staticmethod
    def is_vespertino(checktime, in_out):
        t = checktime.timetuple()[3:6]
        checktime = time(*t)

        if in_out == 'I':
            if time(13) < checktime < time(15):
                return True
        if in_out == 'O':
            if time(16, 30) < checktime < time(19, 30):
                return True
        return False

    @staticmethod
    def keys():
        return "matutino", "vespertino"


class HorarioNocturno:
    @staticmethod
    def validateCheck(inp, in_or_out):
        t = inp.timetuple()[3:6]
        checktime = time(*t)
        if in_or_out == 'I':
            if time(17) < checktime < time(21):
                return True
        if in_or_out == 'O':
            if time(4, 30) < checktime < time(7, 30):
                return True
        return False

    def keys(self):
        return "nocturno"


if __name__ == "__main__":
    t = datetime(2014, 9, 4, 8, 32, 12)
    HorarioDiurno.validateCheck(t, "I")
