from __future__ import annotations

import cv2
import numpy as np


def find_largest_contour(edge_image: np.ndarray) -> np.ndarray | None:
    """Find the largest four-point contour that likely represents a document."""
    contours, _ = cv2.findContours(edge_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours[:8]:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            return approx.reshape(4, 2)
    return None


def order_points(points: np.ndarray) -> np.ndarray:
    """Order four contour points as top-left, top-right, bottom-right, bottom-left."""
    rect = np.zeros((4, 2), dtype="float32")
    sums = points.sum(axis=1)
    diffs = np.diff(points, axis=1)
    rect[0] = points[np.argmin(sums)]
    rect[2] = points[np.argmax(sums)]
    rect[1] = points[np.argmin(diffs)]
    rect[3] = points[np.argmax(diffs)]
    return rect


def perspective_transform(image: np.ndarray, contour: np.ndarray | None) -> np.ndarray:
    """Warp a document contour to a flat top-down perspective."""
    if contour is None:
        return image.copy()
    rect = order_points(contour.astype("float32"))
    tl, tr, br, bl = rect
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_width = max(int(width_a), int(width_b), 1)
    max_height = max(int(height_a), int(height_b), 1)
    destination = np.array(
        [[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]],
        dtype="float32",
    )
    matrix = cv2.getPerspectiveTransform(rect, destination)
    return cv2.warpPerspective(image, matrix, (max_width, max_height))


def draw_contour(image: np.ndarray, contour: np.ndarray | None) -> np.ndarray:
    """Draw the detected document contour on a copy of the image."""
    output = image.copy()
    if contour is not None:
        cv2.drawContours(output, [contour.astype("int32")], -1, (37, 99, 235), 4)
    return output
