class play(object):
    number = 0
    def __init__(self,name,city):
        self._name = name
        self._city = city
        play.number += 1
    def show(self):
        print(self._name,self._city)

    @classmethod
    def get_play(cls):
       print(cls.number)

obj = play("hell","world")
print(obj.__dict__)
print(obj.number)
# obj.city="北京"
# obj.name="小明"
# obj.age=18
#
# print(obj.city,obj.name,obj.age)
class VIP(play):
    pass

obj1 = VIP("小明","北京")
obj1.show()

def a():
    pass
def a(b):
    pass


