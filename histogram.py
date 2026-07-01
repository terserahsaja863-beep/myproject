from __future__ import annotations

import cv2
import matplotlib.pyplot as plt
import numpy as np


def create_histogram_figure(before: np.ndarray, after: np.ndarray):
    """Create a Matplotlib figure comparing before and after grayscale histograms."""
    before_gray = cv2.cvtColor(before, cv2.COLOR_RGB2GRAY) if len(before.shape) == 3 else before
    after_gray = cv2.cvtColor(after, cv2.COLOR_RGB2GRAY) if len(after.shape) == 3 else after
    fig, axes = plt.subplots(1, 2, figsize=(9, 3), dpi=130)
    for axis, image, title, color in [
        (axes[0], before_gray, "Histogram Before", "#2563EB"),
        (axes[1], after_gray, "Histogram After", "#14B8A6"),
    ]:
        axis.hist(image.ravel(), bins=256, range=(0, 255), color=color, alpha=0.86)
        axis.set_title(title, fontsize=10, fontweight="bold")
        axis.set_xlim(0, 255)
        axis.grid(alpha=0.18)
    fig.tight_layout()
    return fig
