import WalabotAPI
import numpy as np
import matplotlib.pyplot as plt


def initialize_walabot():
    try:
        WalabotAPI.Init()  # Initialize the Walabot
        WalabotAPI.ConnectAny()  # Connect to the first available Walabot
        # Set the profile (sensor mode)
        WalabotAPI.SetProfile(WalabotAPI.PROF_SENSOR)
        WalabotAPI.Start()  # Start scanning
    except WalabotAPI.WalabotError as e:
        print(f"Error initializing Walabot: {e.message}")
        exit(1)


def collect_data():
    try:
        # Collect raw data (TOF profile)
        WalabotAPI.Trigger()  # Trigger a scan
        raw_data = WalabotAPI.GetRawImageSlice()
        return raw_data
    except WalabotAPI.WalabotError as e:
        print(f"Error collecting data: {e.message}")
        exit(1)


def create_heatmap(raw_data):
    # Process raw data and create a simple heatmap
    # You can enhance this step for better results
    heatmap = np.zeros((100, 100))  # Assuming a 100x100 grid
    for i, distance in enumerate(raw_data):
        x, y = i, int(distance * 10)  # Scale for visualization
        heatmap[y, x] = 1  # Mark the position

    return heatmap


def is_person_identified(heatmap, threshold=0.5):
    """
    Determines if a person is identified in the heatmap.

    Args:
        heatmap (np.ndarray): The heatmap (2D array) with intensity values.
        threshold (float): Threshold for person detection (adjust as needed).

    Returns:
        bool: True if a person is identified, False otherwise.
    """
    max_intensity = np.max(heatmap)
    return max_intensity >= threshold


def main():
    initialize_walabot()
    raw_data = collect_data()
    heatmap = create_heatmap(raw_data)

    # Visualize the heatmap
    plt.imshow(heatmap, cmap='hot', origin='lower')
    plt.title("Person Detection Heatmap")
    plt.xlabel("X (pixels)")
    plt.ylabel("Y (pixels)")
    plt.show()

    # Analyze the heatmap
    person_detected = is_person_identified(heatmap)
    if person_detected:
        print("Person detected!")
    else:
        print("No person identified.")


if __name__ == "__main__":
    main()
