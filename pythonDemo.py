from PIL import Image
import os
import glob

# Пути к файлам
SLICES_DIR = r"C:\Users\arslanovSamat\Desktop\инжа\pythonPackage\slices"
DATA_FILE_PATH = r"C:\Users\arslanovSamat\Desktop\инжа\pythonPackage\dataPackage.txt"
OUTPUT_DIR = r"C:\Users\arslanovSamat\Desktop\инжа\pythonPackage\sorting_frames"

def load_slices(slices_dir):
    """
    Загружает все нарезанные полоски, автоматически определяя их имена.
    """
    # Ищем все PNG файлы в папке
    slice_files = glob.glob(os.path.join(slices_dir, "*.png"))
    slice_files.sort()  # Сортируем для порядка
    
    if not slice_files:
        print(f"Ошибка: В папке {slices_dir} не найдено PNG файлов!")
        print("Содержимое папки:")
        for f in os.listdir(slices_dir):
            print(f"  - {f}")
        return None
    
    print(f"Найдено {len(slice_files)} PNG файлов:")
    for i, f in enumerate(slice_files[:5]):  # Покажем первые 5
        print(f"  {i+1}. {os.path.basename(f)}")
    if len(slice_files) > 5:
        print(f"  ... и еще {len(slice_files) - 5}")
    
    if len(slice_files) != 100:
        print(f"Предупреждение: Ожидалось 100 файлов, найдено {len(slice_files)}")
    
    # Загружаем все изображения
    slices = []
    print("\nЗагружаем изображения...")
    
    for i, filepath in enumerate(slice_files):
        try:
            img = Image.open(filepath)
            slices.append(img)
            if (i + 1) % 20 == 0:
                print(f"Загружено {i + 1}/{len(slice_files)}")
        except Exception as e:
            print(f"Ошибка при загрузке {filepath}: {e}")
            return None
    
    # Определяем размеры для будущих кадров
    total_width = sum(img.width for img in slices)
    height = slices[0].height
    
    print(f"\nУспешно загружено {len(slices)} полосок")
    print(f"Общая ширина кадра: {total_width}px")
    print(f"Высота кадра: {height}px")
    
    return slices, total_width, height

def create_frame(slices, order, total_width, height):
    """
    Создает один кадр, располагая полоски в заданном порядке.
    order: список чисел от 1 до 100, где число n означает,
           что на эту позицию нужно поставить полоску с индексом n-1
    """
    # Создаем новое пустое изображение
    frame = Image.new('RGB', (total_width, height))
    
    current_x = 0
    for position, slice_number in enumerate(order):
        # Индекс полоски = число из файла - 1
        slice_index = slice_number - 1
        
        # Проверяем, что индекс в допустимых пределах
        if slice_index < 0 or slice_index >= len(slices):
            print(f"Ошибка: индекс {slice_index} вне диапазона (0-{len(slices)-1})")
            continue
            
        slice_img = slices[slice_index]
        
        # Вставляем полоску
        frame.paste(slice_img, (current_x, 0))
        current_x += slice_img.width
    
    return frame

def main():
    print("=" * 50)
    print("ВИЗУАЛИЗАЦИЯ СОРТИРОВКИ")
    print("=" * 50)
    
    # 1. Проверяем существование папки с полосками
    if not os.path.exists(SLICES_DIR):
        print(f"Ошибка: Папка {SLICES_DIR} не найдена!")
        return
    
    # 2. Загружаем все полоски
    result = load_slices(SLICES_DIR)
    if result is None:
        return
    slices, total_width, height = result
    
    # 3. Создаем папку для результатов
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"\nСоздана папка {OUTPUT_DIR}")
    else:
        # Очищаем папку
        for f in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, f))
        print(f"\nПапка {OUTPUT_DIR} очищена")
    
    # 4. Читаем файл с данными сортировки
    if not os.path.exists(DATA_FILE_PATH):
        print(f"Ошибка: Файл {DATA_FILE_PATH} не найден!")
        return
    
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            lines = f.readlines()
        print(f"\nФайл данных прочитан. Найдено {len(lines)} строк.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return
    
    # 5. Создаем кадры
    frame_number = 0
    total_frames = len(lines)
    
    print(f"\nНачинаем создание {total_frames} кадров...")
    print("-" * 40)
    
    for i, line in enumerate(lines):
        frame_number += 1
        line = line.strip()
        if not line:
            continue
        
        # Преобразуем строку в список чисел
        try:
            current_order = [int(x) for x in line.split()]
        except ValueError as e:
            print(f"Предупреждение: строка {frame_number} содержит нечисловые данные: {e}")
            continue
        
        if len(current_order) != 100:
            print(f"Предупреждение: строка {frame_number} содержит {len(current_order)} чисел (ожидалось 100)")
            continue
        
        # Создаем кадр
        frame = create_frame(slices, current_order, total_width, height)
        
        # Сохраняем
        output_filename = os.path.join(OUTPUT_DIR, f"frame_{frame_number:06d}.png")
        frame.save(output_filename, "PNG")
        
        # Показываем прогресс
        if (i + 1) % 100 == 0 or (i + 1) == total_frames:
            print(f"✓ Создано {i + 1}/{total_frames} кадров")
    
    print("-" * 40)
    print(f"\n✅ Готово! Создано {frame_number} кадров в папке:")
    print(f"   {OUTPUT_DIR}")
    
    # 6. Предлагаем создать GIF
    print("\n" + "=" * 50)
    print("СОЗДАНИЕ GIF-АНИМАЦИИ")
    print("=" * 50)
    print("Хотите создать GIF-анимацию из всех кадров?")
    print("1. Да, создать GIF")
    print("2. Нет, завершить работу")
    print("3. Да, создать GIF с настройкой скорости")
    
    choice = input("\nВаш выбор (1/2/3): ").strip()
    
    if choice == '1':
        create_gif(OUTPUT_DIR)
    elif choice == '3':
        try:
            duration = int(input("Введите задержку между кадрами в миллисекундах (50-200): "))
            create_gif(OUTPUT_DIR, duration=duration)
        except ValueError:
            print("Неверный ввод. Используем стандартные настройки.")
            create_gif(OUTPUT_DIR)
    else:
        print("Работа завершена.")

def create_gif(frames_dir, output_path="sorting_animation.gif", duration=50):
    """
    Создает GIF-анимацию из всех кадров.
    duration - задержка между кадрами в миллисекундах
    """
    print(f"\nСоздаем GIF с задержкой {duration}ms...")
    
    # Получаем все файлы кадров
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith("frame_")])
    
    if not frame_files:
        print("Нет кадров для создания GIF!")
        return
    
    print(f"Загружаем {len(frame_files)} кадров...")
    
    frames = []
    for i, filename in enumerate(frame_files):
        if (i + 1) % 100 == 0:
            print(f"Загружено {i + 1}/{len(frame_files)} кадров...")
        try:
            frame = Image.open(os.path.join(frames_dir, filename))
            frames.append(frame)
        except Exception as e:
            print(f"Ошибка при загрузке {filename}: {e}")
    
    if frames:
        # Сохраняем GIF
        output_gif = os.path.join(os.path.dirname(frames_dir), output_path)
        frames[0].save(
            output_gif,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,
            optimize=True
        )
        print(f"\n✅ GIF создан: {output_gif}")
        print(f"   Размер: {len(frames)} кадров, задержка: {duration}ms")
    else:
        print("Не удалось загрузить кадры для GIF")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nРабота прервана пользователем.")
    except Exception as e:
        print(f"\nНепредвиденная ошибка: {e}")
        import traceback
        traceback.print_exc()
