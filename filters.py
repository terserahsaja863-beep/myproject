from __future__ import annotations

import cv2
import numpy as np

from src.preprocessing import adjust_brightness, adjust_contrast, equalize_histogram, sharpen_image, to_grayscale


def apply_filter(image: np.ndarray, filter_name: str) -> np.ndarray:
    """Apply one named visual filter to an RGB image."""
    if filter_name == "Grayscale":
        gray = to_grayscale(image)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    if filter_name == "High Contrast":
        return adjust_contrast(image, 65)
    if filter_name == "Black & White":
        gray = to_grayscale(image)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
    if filter_name == "Sepia":
        kernel = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
        sepia = cv2.transform(image, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)
    if filter_name == "Color Boost":
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.35, 0, 255).astype(np.uint8)
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    if filter_name == "Document Boost":
        enhanced = equalize_histogram(image)
        enhanced = sharpen_image(enhanced, 35)
        return adjust_brightness(adjust_contrast(enhanced, 28), 8)
    return image.copy()
