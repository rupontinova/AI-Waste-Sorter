graph TD
    subgraph "User's Browser"
        A[React Frontend UI]
    end

    subgraph "Backend Server"
        B[Flask API]
        C[YOLOv8 AI Model]
    end

    A -- "1. User uploads image (HTTP POST)" --> B
    B -- "2. Sends image for processing" --> C
    C -- "3. Returns detection data (labels, boxes, confidence)" --> B
    B -- "4. Sends results back (JSON)" --> A
    A -- "5. Displays results visually" --> A

    style A fill:#61DAFB,stroke:#000,stroke-width:2px,color:#000
    style B fill:#3776AB,stroke:#000,stroke-width:2px,color:#fff
    style C fill:#FFD43B,stroke:#000,stroke-width:2px,color:#000

### Diagram Explanation

This diagram shows the flow of data through the Smart Waste Sorter application:

1.  **React Frontend UI**: This is the web interface running in the user's browser. The user interacts with the system by uploading an image file through this UI.

2.  **Flask API**: The React frontend sends the uploaded image to the Flask backend server. Flask acts as the central controller, handling incoming requests and managing the AI model.

3.  **YOLOv8 AI Model**: The Flask server passes the image to the YOLOv8 model. The model analyzes the image to detect and classify different types of waste, determining their location (bounding box), category (label), and a confidence score.

4.  **JSON Response**: The model's findings are sent back to the Flask API, which formats them into a structured JSON response. This JSON is then sent back to the user's browser.

5.  **Visual Display**: The React frontend receives the JSON data and uses it to visually display the results on the original image, drawing bounding boxes around detected items and labeling them with their waste category.

