import os
import rasterio
import numpy as np
import matplotlib.pyplot as plt


def save_layer_as_png(image, output_path, cmap=None):
    plt.figure(figsize=(10, 10))
    if cmap:
        plt.imshow(image, cmap=cmap)
    else:
        plt.imshow(image)
    plt.axis('off')
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()


def create_png_from_geotiff(file_path, r_band, g_band, b_band, ik_band, mask_band):
    try:
        # Получаем директорию и имя файла для сохранения
        folder, file_name = os.path.split(file_path)
        base_name = os.path.splitext(file_name)[0]

        with rasterio.open(file_path) as src:
            # Чтение слоёв
            red = src.read(r_band)
            green = src.read(g_band)
            blue = src.read(b_band)
            ik = src.read(ik_band)
            mask = src.read(mask_band)

            # Масштабирование значений для RGB изображения
            def scale_band(band):
                band = band.astype(np.float32)
                band_min, band_max = band.min(), band.max()
                scaled = (band - band_min) / (band_max - band_min) * 255
                return scaled.astype(np.uint8)

            red = scale_band(red)
            green = scale_band(green)
            blue = scale_band(blue)

            # Создание RGB изображения
            rgb_image = np.stack([red, green, blue], axis=-1)

            # Сохранение RGB изображения
            rgb_output_path = os.path.join(folder, f"{base_name}_RGB.png")
            save_layer_as_png(rgb_image, rgb_output_path)
            print(f"RGB изображение сохранено в: {rgb_output_path}")

            # Сохранение ИК слоя (инфракрасный канал) с зелёной палитрой
            ik_output_path = os.path.join(folder, f"{base_name}_IK.png")
            save_layer_as_png(ik, ik_output_path, cmap='summer')
            print(f"ИК изображение сохранено в: {ik_output_path}")

            # Сохранение маски пожара
            mask_output_path = os.path.join(folder, f"{base_name}_mask.png")
            save_layer_as_png(mask, mask_output_path, cmap='gray')
            print(f"Маска пожара сохранена в: {mask_output_path}")

    except Exception as e:
        print(f'Ошибка при обработке {file_path}: {e}')


def process_all_folders(base_dir, r_band, g_band, b_band, ik_band, mask_band):
    for i in range(21):  # Обрабатываем папки от 00 до 20
        folder_name = f"{i:02d}"  # Форматируем имя папки с ведущим нулём
        folder_path = os.path.join(base_dir, folder_name)

        if not os.path.isdir(folder_path):
            print(f"Папка не найдена: {folder_path}")
            continue

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.tiff'):
                file_path = os.path.join(folder_path, file_name)
                print(f"Обрабатывается файл: {file_path}")
                create_png_from_geotiff(file_path, r_band, g_band, b_band, ik_band, mask_band)


# Укажите базовый каталог, где находятся папки с TIFF файлами
base_directory = '/Users/admin/Downloads/minprirody_train/train'
process_all_folders(base_directory, 1, 2, 3, 4, 5)