from functools import reduce
a = ('이은성' , '김형32진' , '안재진')

ee = []
for i in a:
    new_word = reduce(lambda x,y:x+y if y.isnumeric() == False else x , i)
    ee.append(new_word)


print(reduce(lambda x,y:x+y if type(y) == int else x, [1,2,3,4,'dd',5,6]))



