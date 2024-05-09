a = [
    [1,2,3,4,2,3,1,2],
    [1,1,3,2,3,3,1,2],
    [1,2,3,2,1,3,1,4],
    ]

histograma = {}

for i in range(3):
    for j in range(8):
        intensidade = a[i][j]
        if(intensidade in histograma):
            histograma[intensidade] += 1
        else:
            histograma[intensidade] = 1
    
print(histograma)