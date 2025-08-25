import random
from functools import reduce

# generating random values of temperatures
temps = [random.uniform(10.0, 50.0) for _ in range(10)]

print(f"Recorded temperatures: {[round(t, 2) for t in temps]}")

# callibrating each temperature
callibrated_temp = list(map(lambda x: x + 0.8, temps))
print(f"Calibrated temperatures: {[round(t, 2) for t in callibrated_temp]}")

# removing outliers
temps_after_outliers = list(filter(lambda x: x < 30.0, callibrated_temp))
print(f"Temperatures below 30.0: {[round(t, 2) for t in temps_after_outliers]}")

# average temperatures
avg_temp = sum(temps_after_outliers) / len(temps_after_outliers)
print(f"Average temp: {avg_temp:.2f}")
