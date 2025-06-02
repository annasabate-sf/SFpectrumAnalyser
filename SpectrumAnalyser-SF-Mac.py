import cv2
import numpy as np
import matplotlib.pyplot as plt
from screeninfo import get_monitors
import subprocess



def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))

def resize_to_fit_screen(image, max_width, max_height):
    h, w = image.shape[:2]
    scale = min(max_width / w, max_height / h, 1.0)
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)

def select_image_file():
    try:
        script = '''
        set theFile to choose file of type {"public.image"} with prompt "Select an image file:"
        set thePath to POSIX path of theFile
        return thePath
        '''
        args = ["osascript", "-e", script]
        result = subprocess.run(args, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print("⚠️ Failed to open native file picker:", e)
        return None

def analyze_roi(cropped):
    shape = cropped.shape
    r_dist, g_dist, b_dist, i_dist = [], [], [], []

    for i in range(shape[1]):
        r_val = np.mean(cropped[:, i][:, 2])
        g_val = np.mean(cropped[:, i][:, 1])
        b_val = np.mean(cropped[:, i][:, 0])
        i_val = (r_val + g_val + b_val) / 3

        r_dist.append(r_val)
        g_dist.append(g_val)
        b_dist.append(b_val)
        i_dist.append(i_val)

    plt.figure(figsize=(10, 5))
    
    # Top: show cropped ROI
    plt.subplot(2, 1, 1)
    plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Selected ROI")
    
    # Bottom: plot RGB and intensity
    plt.subplot(2, 1, 2)
    plt.plot(r_dist, color='r', label='Red')
    plt.plot(g_dist, color='g', label='Green')
    plt.plot(b_dist, color='b', label='Blue')
    plt.plot(i_dist, color='k', label='Mean RGB Intensity')
    
    plt.xlabel("Pixel Column Index (px)")
    plt.ylabel("Average Intensity (0-255)")
    plt.title("Color Intensity Across ROI Width")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def display_instructions(image):
    overlay = image.copy()
    cv2.rectangle(overlay, (10, 10), (360, 120), (0, 0, 0), -1)
    instructions = [
        "Press 'r' to rotate",
        "Press 's' to select ROI",
        "Press 'n' to load new image",
        "Press 'q' or ESC to quit"
    ]
    for i, text in enumerate(instructions):
        cv2.putText(overlay, text, (20, 40 + i * 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    return overlay

def main():
    screen = get_monitors()[0]
    max_width = int(screen.width * 0.9)
    max_height = int(screen.height * 0.9)

    image = None
    rotated_image = None

    while True:
        display_image = np.zeros((300, 500, 3), dtype=np.uint8)
        cv2.putText(display_image, "Press 'n' to load image", (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("Image", display_image)

        while image is None:
            key = cv2.waitKey(100) & 0xFF
            if key == ord('n'):
                path = select_image_file()
                if path:
                    image = cv2.imread(path)
                    if image is not None:
                        image = resize_to_fit_screen(image, max_width, max_height)
                        rotated_image = image.copy()
                    else:
                        print("Failed to load image.")
            elif key in [ord('q'), 27]:  # ESC
                cv2.destroyAllWindows()
                return

        while image is not None:
            shown = display_instructions(rotated_image)
            cv2.imshow("Image", shown)
            key = cv2.waitKey(100) & 0xFF

            if key == ord('r'):
                rotated_image = rotate_image(rotated_image, -90)
                rotated_image = resize_to_fit_screen(rotated_image, max_width, max_height)

            elif key == ord('s'):
                roi = cv2.selectROI("Image", rotated_image)
                if roi[2] > 0 and roi[3] > 0:
                    cropped = rotated_image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
                    analyze_roi(cropped)

            elif key == ord('n'):
                image = None
                rotated_image = None
                break  # Go back to main loop and re-load

            elif key in [ord('q'), 27]:  # ESC or 'q'
                cv2.destroyAllWindows()
                return

if __name__ == '__main__':
    main()