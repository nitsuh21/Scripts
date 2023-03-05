Input = ['"t-shirt OR trousers" in "blue OR green"']
output = []
counter = 0
for i in Input:
    for j in i:
        if j == "-":
            counter+=1
times = (3 * counter)+1
print(times)
            