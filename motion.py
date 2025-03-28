import cv2
import os
import time

class MotionDetector:
    def __init__(self, reference_image_path, output_dir='snapshots', threshold=30, interval=5):
        # We can change the interval for capturing the images
        # Images are stored into a seprate file called snapshots
       
        # Create output directory if it doesn't exist
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Load reference image and convert to grayscale
        self.reference_image = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
        if self.reference_image is None:
            raise ValueError("Could not load reference image")
        
        # Camera setup
        # Use default camera
        self.cap = cv2.VideoCapture(0)  
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        
        # Parameters
        self.threshold = threshold
        self.interval = interval
        
    def detect_motion(self):
        last_snapshot_time = 0
        
        while True:
            # Capture frame
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            # Show live camera feed
            cv2.imshow('Live Camera', frame)
            
            # Check if it's time to take a snapshot
            current_time = time.time()
            if current_time - last_snapshot_time >= self.interval:
                # Convert frame to grayscale
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Motion detection
                diff = cv2.absdiff(self.reference_image, gray_frame)
                
                # Apply threshold
                _, thresh = cv2.threshold(diff, self.threshold, 255, cv2.THRESH_BINARY)
                
                # Find contours (lines/motion)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Check if significant motion is detected
                if len(contours) > 0:
                    # Save snapshot
                    snapshot_path = os.path.join(self.output_dir, f'snapshot_{int(current_time)}.jpg')
                    cv2.imwrite(snapshot_path, frame)
                    print(f"Motion detected! Snapshot saved: {snapshot_path}")
                    
                    # Draws contours on frame to visualize motion
                    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
                    cv2.imshow('Motion Detected', frame)
                else:
                    print("No significant motion detected")
                
                # Update last snapshot time
                last_snapshot_time = current_time
            
            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    # Provide path to your reference image
    reference_image_path = 'Add the location to reference image'
    
    try:
        # Initialize and run motion detector
        motion_detector = MotionDetector(reference_image_path)
        motion_detector.detect_motion()
    except Exception as e:
        print(f"Error: {e}")


main()
