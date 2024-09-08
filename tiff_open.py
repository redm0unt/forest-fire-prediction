import rasterio
import matplotlib.pyplot as plt
import numpy as np

file_path = '/Users/admin/Downloads/minprirody_train/train/19/2021-05-04.tiff'


# In[4]:


def print_geotiff_info(path):
    try:
        # Открываем файл
        with rasterio.open(path) as src:
            # Основные метаданные
            print(f"File Path: {path}")
            print(f"Driver: {src.driver}")
            print(f"Width: {src.width}")
            print(f"Height: {src.height}")
            print(f"Count (Bands): {src.count}")
            print(f"CRS: {src.crs}")
            print(f"Transform: {src.transform}")
            print(f"Bounding Box: {src.bounds}")
            print(f"Datum: {src.dtypes}")

            # Информация по каждому каналу
            for i in range(1, src.count + 1):
                band = src.read(i)
                print(f"\nBand {i}:")
                print(f"  Data Type: {src.dtypes[i - 1]}")
                print(f"  Min Value: {band.min()}")
                print(f"  Max Value: {band.max()}")
                print(f"  Mean Value: {band.mean()}")
                print(f"  Standard Deviation: {band.std()}")

    except Exception as e:
        print(f'Error: {e}')


# Вывод информации о GeoTIFF
print_geotiff_info(file_path)


# In[5]:

def visualize_rgb_geotiff(file_path, r_band, g_band, b_band, ik_band, mask_band):
    try:
        with rasterio.open(file_path) as src:
            num_bands = src.count
            print(f"Number of bands: {num_bands}")
            red = src.read(r_band)  # B02 - Blue
            green = src.read(g_band)  # B03 - Green
            blue = src.read(b_band)  # B04 - Red
            ik = src.read(ik_band)
            mask = src.read(mask_band)

            def scale_band(band):
                band = band.astype(np.float32)
                band_min, band_max = band.min(), band.max()
                scaled = (band - band_min) / (band_max - band_min) * 255
                return scaled.astype(np.uint8)

            ed = scale_band(red)
            green = scale_band(green)
            blue = scale_band(blue)

            photo = np.stack([red, green, blue], axis=-1)  # Отрисовка всего изображения
            # photo = np.stack([ik], axis=-1) # Отрисовка ИК-слоя изображения
            # photo = np.stack([mask], axis=-1)  # Отрисовка маски изображения
            photo = photo.astype(np.uint8)
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.imshow(photo)
            ax.axis('off')
            plt.show()
    except Exception as e:
        print(f'Ошибка: {e}')


# In[6]:
# Визуализация изображения
visualize_rgb_geotiff(file_path, 1, 2, 3, 4, 5)
