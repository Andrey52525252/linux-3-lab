import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Укажите полный путь к файлу
with open(r"C:\Users\arslanovSamat\Desktop\инжа\pythonPackage\dataPackage.txt", "r") as f:
    data = [list(map(int, line.split())) for line in f]

print(f"Загружено {len(data)} строк")
print(f"Первая строка: {data[0][:10]}...")  # Покажем первые 10 элементов

fig, ax = plt.subplots(figsize=(16, 8))

def update(frame):
    ax.clear()
    ax.bar(range(100), data[frame], color='skyblue')
    ax.set_title(f'Шаг {frame + 1} из {len(data)}')
    ax.set_ylim(0, 100)
    ax.set_xticks(range(0, 100, 10))

ani = FuncAnimation(fig, update, frames=len(data), interval=0.001)
plt.show()
