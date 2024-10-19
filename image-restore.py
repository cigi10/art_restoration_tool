import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
import os

def load_image(path):
    return cv2.imread(path)

def denoise_image(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

def add_noise(image):
    noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
    noisy_image = cv2.add(image, noise)
    return np.clip(noisy_image, 0, 255)

def build_denoising_model(input_shape):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.Conv2D(3, (3, 3), padding='same')
    ])
    return model

def train_model(model, noisy_images, clean_images, epochs=10, batch_size=32):
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(noisy_images, clean_images, epochs=epochs, batch_size=batch_size, validation_split=0.0)

def predict_and_visualize(model, image):
    test_noisy_image = add_noise(image)
    predicted_denoised_image = model.predict(test_noisy_image[np.newaxis, ...])

    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.title('Noisy Image')
    plt.imshow(test_noisy_image / 255.0)
    
    plt.subplot(1, 3, 2)
    plt.title('Denoised Image')
    plt.imshow(predicted_denoised_image[0] / 255.0)
    
    plt.subplot(1, 3, 3)
    plt.title('Original Image')
    plt.imshow(image / 255.0)
    
    plt.show()

def generate_noise(image_directory):
    clean_images = []
    noisy_images = []
    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            img = load_image(os.path.join(image_directory, filename))
            clean_images.append(img)
            noisy_images.append(add_noise(img))
    return np.array(clean_images), np.array(noisy_images)

def main():
    image_directory = input("Enter the path to the image directory: ")
    print(f"Using image directory: '{image_directory}'")
    clean_images, noisy_images = generate_noise(image_directory)
    model = build_denoising_model((256, 256, 3))
    train_model(model, noisy_images, clean_images)

if __name__ == "__main__":
    main()

