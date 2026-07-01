from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image


def load_image_from_upload(uploaded_file) -> np.ndarray:
    """Read an uploaded Streamlit file into an RGB numpy image."""
    image = Image.open(uploaded_file).convert("RGB")
    return np.array(image)


def resize_image(image: np.ndarray, width: int = 900) -> tuple[np.ndarray, float]:
    """Resize an image for processing while returning the original scale ratio."""
    height, current_width = image.shape[:2]
    if current_width <= width:
        return image.copy(), 1.0
    ratio = current_width / float(width)
    resized = cv2.resize(image, (width, int(height / ratio)), interpolation=cv2.INTER_AREA)
    return resized, ratio


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert an RGB or BGR image to grayscale."""
    if len(image.shape) == 2:
        return image.copy()
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


def gaussian_blur(gray_image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Apply Gaussian blur to reduce noise before edge detection."""
    return cv2.GaussianBlur(gray_image, (kernel_size, kernel_size), 0)


def canny_edges(gray_image: np.ndarray, threshold: int = 75) -> np.ndarray:
    """Detect image edges using Canny with a user-controlled threshold."""
    lower = max(0, int(threshold))
    upper = min(255, int(threshold * 2))
    return cv2.Canny(gray_image, lower, upper)


def dilate_edges(edge_image: np.ndarray, iterations: int = 1) -> np.ndarray:
    """Dilate edge lines so document boundaries become easier to contour."""
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(edge_image, kernel, iterations=iterations)


def erode_edges(edge_image: np.ndarray, iterations: int = 1) -> np.ndarray:
    """Erode dilated edges to remove small blobs while keeping boundaries."""
    kernel = np.ones((3, 3), np.uint8)
    return cv2.erode(edge_image, kernel, iterations=iterations)


def adaptive_threshold(gray_image: np.ndarray) -> np.ndarray:
    """Create a crisp document-like binary image using adaptive thresholding."""
    return cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21,
        12,
    )


def equalize_histogram(image: np.ndarray) -> np.ndarray:
    """Improve tonal range with histogram equalization."""
    if len(image.shape) == 2:
        return cv2.equalizeHist(image)
    ycrcb = cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)


def sharpen_image(image: np.ndarray, amount: int = 20) -> np.ndarray:
    """Sharpen an image using an unsharp-mask style blend."""
    strength = max(0.0, amount / 50.0)
    blurred = cv2.GaussianBlur(image, (0, 0), 3)
    return cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)


def adjust_brightness(image: np.ndarray, brightness: int = 0) -> np.ndarray:
    """Shift image brightness by adding a signed beta value."""
    return cv2.convertScaleAbs(image, alpha=1.0, beta=int(brightness))


def adjust_contrast(image: np.ndarray, contrast: int = 0) -> np.ndarray:
    """Adjust image contrast using an alpha multiplier derived from the slider."""
    alpha = max(0.1, 1.0 + (contrast / 100.0))
    return cv2.convertScaleAbs(image, alpha=alpha, beta=0)


def rotate_image(image: np.ndarray, angle_label: str) -> np.ndarray:
    """Rotate an image by one of the supported right-angle orientations."""
    if angle_label == "90°":
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    if angle_label == "180°":
        return cv2.rotate(image, cv2.ROTATE_180)
    if angle_label == "270°":
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return image.copy()


def image_to_png_bytes(image: np.ndarray) -> bytes:
    """Encode a numpy image as PNG bytes for Streamlit session storage."""
    pil_image = Image.fromarray(image)
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    return buffer.getvalue()


def png_bytes_to_image(data: bytes) -> np.ndarray:
    """Decode PNG bytes from session state into an RGB numpy image."""
    image = Image.open(BytesIO(data)).convert("RGB")
    return np.array(image)
