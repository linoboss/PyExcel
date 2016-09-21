class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


WorkDayTable = Namespace(id=0, day=1, worker=2,
                         intime_1=3, outtime=4,
                         intime_2=5, outtime_2=6,
                         intime_3=7, outtime_3=8,
                         shift=9, worked_time=10,
                         extra_time=11, absent_time=12)


print(WorkDayTable.id)
