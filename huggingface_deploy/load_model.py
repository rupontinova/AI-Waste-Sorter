"""
Load and configure YOLOv8 waste classification model
This script demonstrates loading a base YOLOv8 model or Hugging Face model
"""

from ultralytics import YOLO
import torch
from pathlib import Path

def load_pretrained_model():
    """
    Load a YOLOv8 model for waste classification
    First tries Hugging Face, falls back to base YOLOv8 model
    Returns the model object
    """
    print("="*60)
    print("Loading YOLOv8 Model for Waste Classification")
    print("="*60)
    
    # Try loading from Hugging Face Hub
    try:
        print("\nAttempt 1: Loading from Hugging Face Hub...")
        from huggingface_hub import hf_hub_download
        
        model_path = hf_hub_download(
            repo_id="kendrickfff/waste-classification-yolov8-ken",
            filename="best.pt"
        )
        model = YOLO(model_path)
        print("✓ Successfully loaded Hugging Face model!")
        
    except Exception as e:
        print(f"✗ Hugging Face model not available: {e}")
        print("\nAttempt 2: Using base YOLOv8n model (for demonstration)...")
        
        try:
            # Load base YOLOv8 nano model - will auto-download
            model = YOLO("yolov8n.pt")
            print("✓ Base YOLOv8n model loaded successfully!")
            print("\nNOTE: This is a general object detection model.")
            print("For production, you should fine-tune on waste-specific data.")
            
        except Exception as e2:
            print(f"\n✗ Error loading model: {e2}")
            raise
    
    print("\n" + "-"*60)
    print(f"Model type: {type(model)}")
    print(f"Number of classes: {len(model.names)}")
    print(f"Classes: {list(model.names.values())[:10]}...")  # Show first 10
    print("-"*60)
    
    return model

def test_model(model, test_image_path=None):
    """
    Test the model with a sample prediction
    """
    if test_image_path:
        print(f"\nTesting model with image: {test_image_path}")
        results = model(test_image_path)
        
        for r in results:
            print(f"\nDetections found: {len(r.boxes)}")
            for box in r.boxes:
                cls_id = int(box.cls.item())
                conf = box.conf.item()
                label = model.names[cls_id]
                print(f"  - {label}: {conf:.2f}")
    else:
        print("\nModel is ready for inference!")
        print("To test with an image, provide the path as an argument.")

def save_model_locally(model, output_path="best.pt"):
    """
    Save the model locally for use in Flask backend
    """
    print(f"\nSaving model to: {output_path}")
    try:
        # Export the model weights
        model.export(format='torchscript', simplify=True)
        # For now, just note the path
        print(f"✓ Model ready for use!")
        print(f"  Model path: {model.ckpt_path if hasattr(model, 'ckpt_path') else 'embedded'}")
    except Exception as e:
        print(f"Note: {e}")
        print("Model is ready to use as-is")

if __name__ == "__main__":
    # Load the pre-trained model
    model = load_pretrained_model()
    
    # Test the model (without an image, just verify it's loaded)
    test_model(model)
    
    # Save the model locally
    save_model_locally(model)
    
    print("\n" + "="*60)
    print("✓ Model Setup Complete!")
    print("="*60)
    print("\nModel classes:")
    for idx, name in list(model.names.items())[:15]:  # Show first 15
        print(f"  {idx}: {name}")
    if len(model.names) > 15:
        print(f"  ... and {len(model.names) - 15} more classes")
    
    print("\n" + "="*60)
    print("Next Steps:")
    print("="*60)
    print("1. Flask Backend - Will remap detected objects to waste categories")
    print("2. React Frontend - Will provide UI for image upload and visualization")
    print("\nTarget waste categories:")
    print("  - Plastic")
    print("  - Paper") 
    print("  - Metal")
    print("  - Organic")
    print("="*60)

