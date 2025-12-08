"""
Test script for the Flask backend
This script tests the /predict endpoint with a sample image
"""

import requests
import json
from PIL import Image, ImageDraw
import io

def create_test_image():
    """
    Create a simple test image with colored shapes
    """
    # Create a simple image with a white background
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw some colored rectangles (simulating objects)
    # Red rectangle (could be detected as something)
    draw.rectangle([100, 100, 200, 200], fill='red', outline='black', width=3)
    
    # Green rectangle
    draw.rectangle([300, 150, 400, 250], fill='green', outline='black', width=3)
    
    # Blue rectangle
    draw.rectangle([450, 200, 550, 350], fill='blue', outline='black', width=3)
    
    # Add some text
    draw.text((250, 50), "TEST IMAGE", fill='black')
    
    return img

def test_health_check():
    """Test the health check endpoint"""
    print("="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get('http://localhost:5001/')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_categories():
    """Test the categories endpoint"""
    print("\n" + "="*60)
    print("Testing Categories Endpoint")
    print("="*60)
    
    try:
        response = requests.get('http://localhost:5001/categories')
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_predict():
    """Test the prediction endpoint with a test image"""
    print("\n" + "="*60)
    print("Testing Prediction Endpoint")
    print("="*60)
    
    # Create a test image
    img = create_test_image()
    
    # Save to BytesIO
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Prepare the files dict
    files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
    
    try:
        print("Sending test image to /predict endpoint...")
        response = requests.post('http://localhost:5001/predict', files=files)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Prediction successful!")
            print(f"\nSuccess: {data.get('success')}")
            print(f"Total Objects: {data.get('total_objects')}")
            print(f"Detections: {len(data.get('detections', []))}")
            
            if data.get('detections'):
                print("\nDetected Objects:")
                for i, det in enumerate(data['detections'], 1):
                    print(f"  {i}. {det['originalLabel']} -> {det['label']} "
                          f"(confidence: {det['confidence']:.2f})")
            
            if data.get('counts'):
                print("\nCategory Counts:")
                for category, count in data['counts'].items():
                    print(f"  {category}: {count}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🧪 SMART WASTE SORTER BACKEND TEST SUITE")
    print("="*70 + "\n")
    
    # Run all tests
    results = []
    
    print("📍 Backend URL: http://localhost:5001")
    print("\n")
    
    results.append(("Health Check", test_health_check()))
    results.append(("Categories", test_categories()))
    results.append(("Prediction", test_predict()))
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Backend is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    print("="*70 + "\n")



