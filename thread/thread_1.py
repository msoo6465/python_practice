import threading



index =0

def sum():
    global index
    total = 0
    while True:
        index = int(input('int input : '))
    print("SubThread",total)

t = threading.Thread(target=sum,daemon=True)
t.start()
preind = index
while True:
    if index != preind:
        print('\nchange index = ',index)
        preind = index
        if index == -1:
            break
    else:
        pass

print("Main Thread")
print(index)
