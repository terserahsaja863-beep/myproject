import cv2


def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """Atur brightness dan contrast gambar menggunakan konversi skala piksel."""
    adjusted = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)
    return adjusted


def to_grayscale(image):
    """Konversi gambar BGR menjadi grayscale tiga channel agar mudah ditampilkan."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    equalized = cv2.equalizeHist(gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)


def high_contrast(image):
    """Tingkatkan detail dokumen menggunakan histogram equalization pada channel luminance."""
    ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb)
    y_channel = cv2.equalizeHist(y_channel)
    enhanced = cv2.merge((y_channel, cr_channel, cb_channel))
    return cv2.cvtColor(enhanced, cv2.COLOR_YCrCb2BGR)


def black_and_white(image):
    """Buat efek hasil scan hitam putih dengan adaptive thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21,
        10,
    )
    return cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)


def apply_scan_mode(image, mode):
    """Terapkan mode tampilan hasil scan sesuai pilihan user di sidebar."""
    if mode == "Grayscale":
        return to_grayscale(image)
    if mode == "High Contrast":
        return high_contrast(image)
    if mode == "Black & White":
        return black_and_white(image)
    return image
