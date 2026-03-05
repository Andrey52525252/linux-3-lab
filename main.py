from PIL import Image
import os


def slice_vertical(input_path, output_folder):
    # Создаём папку
    os.makedirs(output_folder, exist_ok=True)

    # Открываем изображение
    img = Image.open(input_path)
    width, height = img.size

    # Ширина одной полоски
    slice_width = width // 100

    # Режем на 100 полосок
    for i in range(100):
        left = i * slice_width
        right = left + slice_width if i < 99 else width
        slice_img = img.crop((left, 0, right, height))
        slice_img.save(f"{output_folder}/slice_{i:03d}.png")


# Использование
slice_vertical(r"C:\Users\1\Downloads\photo_5283213454221186599_y.jpg", "slices")