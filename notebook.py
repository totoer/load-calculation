from matplotlib import pyplot as plt
import math

IN = 20  # Входящий RPS
OUT = 19 # Скорость обработки RPS
N = 2 # Кол-во сервееров
Q = 15 # Длина очереди

L = IN / OUT # Коэфициент нагруженность системы


S0 = lambda k: (L**k) / math.factorial(k) # Формула расчёта вспомогательной велечены для N
SN = lambda k: (L**k) / ((N**(k-N)) * math.factorial(N)) # Формула расчёта вспомогательной велечены для Q

R = [ S0(k) for k in range(0, N+1) ] # Расчёт для N
R.extend([ SN(k) for k in range(N+1, Q+1) ]) # Расчёт для Q 

P0 = sum(R)**-1 # Вероятность для случая когда в системе 0 запросов
P = [ P0*i for i in R[1:] ] # Расчёт вероятности

print("-"*100)
REJ = P[-1]
print("Вероятность отказа в обслуживании:", REJ*100, "%")
ABS_RPS = IN*(1-P[-1])
print("Абсолютная пропускная способность", ABS_RPS, "RPS")
print("Относительная пропускная способность", (1-REJ)*100, "%")

AVG_S_C = ABS_RPS / OUT
print("Среднее число занятых серверов", AVG_S_C)
AVG_Q_C = ((P0*L**N)*((L/N)-(Q+1)*((L/N)**(Q+1))+Q*((L/N)**(Q+2))))/math.factorial(N)*(1-(L/N)**2)
print("Среднее число запросов в очереди", AVG_Q_C)
AVG_C = AVG_Q_C + AVG_S_C
print("Среднее число запросов", AVG_C)
print("Среднее время обработки запроса", (AVG_C / IN) * 1000, "мс")
print("Среднее время обработки запроса с учётом задержек", 200 + (AVG_C / IN) * 1000, "мс")
print("-"*100)

plt.rcParams['figure.figsize'] = [20, 2]
bars = [f"S{i}" for i in range(len(P))]
bar_colors = ["tab:blue" for _ in range(N)]
bar_colors.extend(["tab:orange" for _ in range(Q)])
plt.bar(bars, P, color=bar_colors, width=0.2)
plt.show()