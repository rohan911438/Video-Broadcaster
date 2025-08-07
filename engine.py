import cv2
from ultralytics import YOLO
import numpy as np
import torch
import os

class CustomSegmentationWithYolo():
    def __init__(self, erode_size=5, erode_intensity=2):
        try:
            self.model = YOLO('yolov8m-seg.pt')
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            raise
        self.erode_size = erode_size
        self.erode_intensity = erode_intensity
        self.background_image = self._load_background_image("./static/wallhaven.png")
         
    def _load_background_image(self, path):
        if os.path.exists(path):
            img = cv2.imread(path)
            if img is not None:
                return img
            else:
                print(f"Warning: Could not read background image at {path}. Using black background instead.")
                return np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            print(f"Warning: Background image not found at {path}. Using black background instead.")
            return np.zeros((480, 640, 3), dtype=np.uint8)
         
    def generate_mask_from_result(self, results):
        try:
            for result in results:
                if result.masks:
                    # get array results
                    masks = result.masks.data
                    boxes = result.boxes.data
                    
                    # extract classes
                    clss = boxes[:, 5]
                    
                    # get indices of results where class is 0 (people in COCO)
                    people_indices = torch.where(clss == 0)
                    
                    # use these indices to extract the relevant masks
                    people_masks = masks[people_indices]

                    if len(people_masks) == 0:
                        return None
                    
                    # scale for visualizing results
                    people_mask = torch.any(people_masks, dim=0).to(torch.uint8) * 255

                    # Erode the mask to bring boundaries inward
                    '''
                    Erosion scans the image with a small kernel (a tiny matrix) and replaces the pixel value with 
                    the minimum value under the kernel. So if even one pixel under the kernel is black, the pixel 
                    being processed will turn black. This has the effect of eating away the white areas, shrinking the mask.
                    '''
                    # iterations - number of times to apply the erosion
                    # kernel - This is a small matrix (typically a square) that slides over the image.
                    kernel = np.ones((self.erode_size, self.erode_size), np.uint8)
                    eroded_mask = cv2.erode(people_mask.cpu().numpy(), kernel, iterations=self.erode_intensity)

                    return eroded_mask
                else:
                    return None
        except Exception as e:
            print(f"Error generating mask: {e}")
            return None


    def apply_blur_with_mask(self, frame, mask, blur_strength=21):
        try:
            # Ensure blur strength is odd
            if blur_strength % 2 == 0:
                blur_strength += 1
            
            blur_strength = (blur_strength, blur_strength)
            blurred_frame = cv2.GaussianBlur(frame, blur_strength, 0)
            
            # Ensure mask is binary
            mask = (mask > 0).astype(np.uint8)
            
            # Expand mask to 3 channels
            mask_3d = cv2.merge([mask, mask, mask])
            
            # Combine blurred and original frame
            result_frame = np.where(mask_3d == 1, frame, blurred_frame)
            
            return result_frame
        except Exception as e:
            print(f"Error applying blur: {e}")
            return frame
    
    def apply_black_background(self, frame, mask):
        try:
            # Create a black background
            black_background = np.zeros_like(frame)
            # Apply the mask
            result_frame = np.where(mask[:, :, np.newaxis] == 255, frame, black_background)
            return result_frame
        except Exception as e:
            print(f"Error applying black background: {e}")
            return frame

    def apply_custom_background(self, frame, mask):
        try:
            # Load the background image
            background_image = cv2.resize(self.background_image, (frame.shape[1], frame.shape[0]))
            # Apply the mask
            result_frame = np.where(mask[:, :, np.newaxis] == 255, frame, background_image)
            return result_frame
        except Exception as e:
            print(f"Error applying custom background: {e}")
            return frame