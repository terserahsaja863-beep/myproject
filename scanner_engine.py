from __future__ import annotations

import logging
import time
from typing import Any

import cv2
import numpy as np

from src.geometry import draw_contour, find_largest_contour, perspective_transform
from src.preprocessing import (
    adaptive_threshold,
    adjust_brightness,
    adjust_contrast,
    canny_edges,
    dilate_edges,
    equalize_histogram,
    erode_edges,
    gaussian_blur,
    resize_image,
    rotate_image,
    sharpen_image,
    to_grayscale,
)

LOGGER = logging.getLogger("smart_document_scanner.engine")


def validate_image(image: np.ndarray) -> None:
    """Raise a clear error when image data is missing or invalid."""
    if image is None or not isinstance(image, np.ndarray) or image.size == 0:
        raise ValueError("Image data is empty or invalid.")


def scan_document(
    image: np.ndarray,
    brightness: int = 12,
    contrast: int = 18,
    edge_threshold: int = 75,
    sharpen: int = 28,
) -> dict[str, Any]:
    """Run the full document scanner pipeline and return every stage."""
    validate_image(image)
    LOGGER.info("Starting full document scan")
    start = time.perf_counter()
    resized, _ = resize_image(image)
    grayscale = to_grayscale(resized)
    blurred = gaussian_blur(grayscale)
    edges = canny_edges(blurred, edge_threshold)
    dilated = dilate_edges(edges)
    eroded = erode_edges(dilated)
    contour = find_largest_contour(eroded)
    contour_detection = draw_contour(resized, contour)
    warped = perspective_transform(resized, contour)
    warped_gray = to_grayscale(warped)
    threshold = adaptive_threshold(warped_gray)
    equalized = equalize_histogram(threshold)
    sharpened = sharpen_image(equalized, sharpen)
    brightened = adjust_brightness(sharpened, brightness)
    contrasted = adjust_contrast(brightened, contrast)
    final_scan = cv2.cvtColor(contrasted, cv2.COLOR_GRAY2RGB) if len(contrasted.shape) == 2 else contrasted
    elapsed = time.perf_counter() - start
    LOGGER.info("Document scan completed in %.3fs; contour_found=%s", elapsed, contour is not None)
    return {
        "elapsed": elapsed,
        "contour_found": contour is not None,
        "stages": {
            "Original": image,
            "Resized": resized,
            "Grayscale": grayscale,
            "Gaussian Blur": blurred,
            "Edge Detection": edges,
            "Dilasi": dilated,
            "Erosi": eroded,
            "Contour Detection": contour_detection,
            "Perspective Transform": warped,
            "Threshold": threshold,
            "Histogram Equalization": equalized,
            "Sharpen": sharpened,
            "Brightness Adjustment": brightened,
            "Contrast Adjustment": contrasted,
            "Final Scan": final_scan,
        },
        "final": final_scan,
    }


def auto_enhance(image: np.ndarray) -> dict[str, Any]:
    """Apply automatic brightness, contrast, histogram equalization, and sharpening."""
    validate_image(image)
    LOGGER.info("Starting auto enhance")
    start = time.perf_counter()
    equalized = equalize_histogram(image)
    brightened = adjust_brightness(equalized, 10)
    contrasted = adjust_contrast(brightened, 24)
    sharpened = sharpen_image(contrasted, 35)
    elapsed = time.perf_counter() - start
    LOGGER.info("Auto enhance completed in %.3fs", elapsed)
    return {
        "elapsed": elapsed,
        "stages": {
            "Original": image,
            "Histogram Equalization": equalized,
            "Brightness Adjustment": brightened,
            "Contrast Adjustment": contrasted,
            "Sharpen": sharpened,
            "Final Scan": sharpened,
        },
        "final": sharpened,
    }


def apply_manual_edits(
    image: np.ndarray,
    brightness: int,
    contrast: int,
    edge_threshold: int,
    sharpen: int,
    rotation: str,
) -> dict[str, Any]:
    """Apply edit panel controls to the current image and expose edge preview stages."""
    validate_image(image)
    LOGGER.info("Starting manual edit")
    start = time.perf_counter()
    rotated = rotate_image(image, rotation)
    gray = to_grayscale(rotated)
    blurred = gaussian_blur(gray)
    edges = canny_edges(blurred, edge_threshold)
    edited = sharpen_image(rotated, sharpen)
    edited = adjust_brightness(edited, brightness)
    edited = adjust_contrast(edited, contrast)
    elapsed = time.perf_counter() - start
    LOGGER.info("Manual edit completed in %.3fs", elapsed)
    return {
        "elapsed": elapsed,
        "stages": {
            "Original": image,
            "Rotate": rotated,
            "Grayscale": gray,
            "Gaussian Blur": blurred,
            "Edge Detection": edges,
            "Sharpen": edited,
            "Final Scan": edited,
        },
        "final": edited,
    }
