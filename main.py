import numpy as np
import rasterio
import matplotlib.pyplot as plt
import pandas as pd


def channel_norm(band: np.ndarray) -> np.ndarray:
    '''
    Функция нормализации цветового канала
    '''
    
    band = band.astype(np.float32)
    band_min, band_max = band.min(), band.max()
    scaled = (band - band_min) / (band_max - band_min) * 255
    
    return scaled.astype(np.uint8)


def read_from_tiff(path_to_tiff: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''
    Чтение rgb-изображения, инфракрасного канала и маски
    '''
    
    r_band, g_band, b_band, ir_band, mask_band = range(1, 6)
    with rasterio.open(path_to_tiff) as src:
        # Чтение слоёв из geoTIFF
        red: np.ndarray = src.read(r_band)
        green: np.ndarray = src.read(g_band)
        blue: np.ndarray = src.read(b_band)
        infrared: np.ndarray = src.read(ir_band)
        mask: np.ndarray = src.read(mask_band)
        
        # Нормализация цветовых каналов
        red: np.ndarray = channel_norm(red)
        green: np.ndarray = channel_norm(green)
        blue: np.ndarray = channel_norm(blue)

    # Создание RGB изображения
    rgb_image = np.stack([red, green, blue], axis=-1)
    rgb_image = rgb_image.astype(np.float32)

    return rgb_image, infrared, mask


def get_vegetation_mask(path_to_tiff: str, threshold: float = 0.4) -> np.ndarray:
    '''
    Функция для определения растительности.
    На входе – изображение GeoTIFF, на выходе – бинарная маска растительности
    '''
    
    rgb_image, infrared, mask = read_from_tiff(path_to_tiff)

    # Извлечение красного канала из RGB изображения
    red_channel = rgb_image[:, :, 0]

    # NDVI вычисляется как (ИК - R) / (ИК + R)
    ndvi: np.ndarray = (infrared - red_channel) / (infrared + red_channel + 1e-6)  # Добавляем малое число, чтобы избежать деления на ноль

    # Создание бинарной маски пожара
    vegetation_mask = np.where(ndvi < threshold, 0, 1).astype(np.uint8)

    return vegetation_mask


def IoU(predicted_mask: np.ndarray, actual_mask: np.ndarray) -> float:
    '''
    Функция для вычисления intersection over union и оценке качества модели
    '''
    
    intersection = np.where(predicted_mask * actual_mask, 1, 0)
    union = np.where(predicted_mask + actual_mask, 1, 0)
    loss = intersection.sum() / union.sum()
    return loss


def get_fire_prediction(file_path: str, heat_threshold: float = 0.1, vegetation_threshold: float = 0.3) -> np.ndarray:
    '''
    Функция для предсказания бинарной маски предполагаемых мест возникновения пожаров на изображении
    '''
    
    MAX = 255
    norm_heat_threshold = heat_threshold * MAX

    vegetation_mask = get_vegetation_mask(file_path, vegetation_threshold).astype(bool)
    rgb_image, infrared, mask = read_from_tiff(file_path)
    heatmap_binary = np.where(infrared > norm_heat_threshold, 1, 0).astype(bool)

    fire_pred = np.where(heatmap_binary * vegetation_mask, 1, 0)
    return fire_pred


if __name__ == '__main__':
    # Путь до файла GeoTIFF
    file_path = '/Users/admin/Downloads/minprirody_train/train/20/2021-05-15.tiff'
    
    # Получение бинарной маски предполагаемых мест возникновения пожаров
    fire_pred = get_fire_prediction(file_path)
    
    # Визуализация бинарной маски предсказанных пожаров
    plt.imshow(fire_pred, cmap='grey')
    plt.title('Fire prediction Mask based on NDVI')
    plt.show()
