import cv2
import os
from datetime import datetime

def capture_snapshot(output_dir='snapshots'):
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the camera
    cap = cv2.VideoCapture(0)  # 0 indicates the default camera
    
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    # Capture a single frame
    ret, frame = cap.read()
    
    # Release the camera
    cap.release()
    
    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not capture frame.")
        return None
    
    # Generate a unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"snapshot_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    # Save the snapshot
    cv2.imwrite(filepath, frame)
    
    print(f"Snapshot saved: {filepath}")
    return filepath

def capture_with_preview():
    # Initialize the camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None
    
    # Create a window for preview
    cv2.namedWindow("Camera Preview", cv2.WINDOW_NORMAL)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not capture frame.")
            break
        
        # Display the resulting frame
        cv2.imshow("Camera Preview", frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        # Capture snapshot on spacebar press
        if key == ord(' '):
            # Generate a unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.jpg"
            filepath = os.path.join('snapshots', filename)
            
            # Create snapshots directory if it doesn't exist
            os.makedirs('snapshots', exist_ok=True)
            
            # Save the snapshot
            cv2.imwrite(filepath, frame)
            print(f"Snapshot saved: {filepath}")
        
        # Exit on 'q' key press
        elif key == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("Choose a snapshot method:")
    print("1. Simple Snapshot")
    print("2. Preview and Capture")
    
    choice = input("Enter your choice (1/2): ")
    
    if choice == '1':
        capture_snapshot()
    elif choice == '2':
        capture_with_preview()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
