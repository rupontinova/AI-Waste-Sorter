import React, { useState, useRef, useEffect, useMemo, useCallback } from 'react';
import axios from 'axios';
import Webcam from "react-webcam";
import './App.css';

// API URL - uses environment variable for production, localhost for development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [sortingHistory, setSortingHistory] = useState(() => {
    try {
      const savedHistory = localStorage.getItem('sortingHistory');
      return savedHistory ? JSON.parse(savedHistory) : [];
    } catch (error) {
      console.error("Could not parse sorting history from localStorage", error);
      return [];
    }
  });
  const canvasRef = useRef(null);
  const webcamRef = useRef(null);

  // Effect to save history to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('sortingHistory', JSON.stringify(sortingHistory));
  }, [sortingHistory]);

  // Define colors for each waste category
  const categoryColors = {
    'Plastic': '#FF4444',  // Red
    'Paper': '#44FF44',    // Green
    'Metal': '#4444FF',    // Blue
    'Organic': '#FFAA00',  // Orange
    'Other': '#888888'     // Gray
  };

  // Recycling information for each category
  const recyclingInfo = {
    'Plastic': 'Rinse bottles and containers before recycling. Remove caps and labels if possible.',
    'Paper': 'Keep paper dry and clean. Flatten cardboard boxes to save space.',
    'Metal': 'Clean metal cans and containers. Be careful of sharp edges.',
    'Organic': 'Compost organic waste at home or use municipal composting services.',
    'Other': 'Check local regulations for items classified as "Other".'
  };

  const handleFile = useCallback((file) => {
    if (file) {
      // Validate file type
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }
      
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResults(null);
      setError(null);
    }
  }, []);

  // Handle file input change
  const onFileChange = (event) => {
    handleFile(event.target.files[0]);
  };

  const handleDrag = (event) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === "dragenter" || event.type === "dragover") {
      setDragging(true);
    } else if (event.type === "dragleave") {
      setDragging(false);
    }
  };
  
  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    setDragging(false);
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      handleFile(event.dataTransfer.files[0]);
    }
  };

  // Handle form submission
  const onFileUpload = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setResults(null);
    setError(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      console.log('Uploading image to backend...');
      
      // Send image to Flask API (port 5001 to avoid conflict with macOS AirPlay)
      const response = await axios.post(`${API_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 30000  // 30 second timeout
      });

      console.log('Response received:', response.data);
      
      if (response.data.success && response.data.counts) {
        setResults(response.data);
        const newHistoryEntry = {
          date: new Date().toISOString(),
          counts: response.data.counts,
        };
        setSortingHistory(prevHistory => [...prevHistory, newHistoryEntry]);
      } else {
        setError('Classification failed: ' + response.data.error);
      }
      
    } catch (err) {
      console.error("Error uploading file:", err);
      
      if (err.code === 'ECONNABORTED') {
        setError('Request timeout. Please try again.');
      } else if (err.response) {
        setError(`Server error: ${err.response.data.error || err.response.statusText}`);
      } else if (err.request) {
        setError(`Cannot connect to backend. Make sure Flask server is running on ${API_URL}`);
      } else {
        setError('An error occurred: ' + err.message);
      }
    }
    
    setLoading(false);
  };

  // Draw on canvas when results change
  useEffect(() => {
    if (preview && canvasRef.current && !isWebcamActive) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const img = new Image();
      
      img.src = preview;
      img.onload = () => {
        // Set canvas dimensions to match the image
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Draw the original image on the canvas
        ctx.drawImage(img, 0, 0);
        
        // If we have results, draw them
        if (results && results.detections && results.detections.length > 0) {
          ctx.lineWidth = 3;
          ctx.font = '18px Arial';
          
          results.detections.forEach(det => {
            const [x1, y1, x2, y2] = det.box;
            const label = det.originalLabel || det.label;
            const category = det.label;
            const displayText = `${category}: ${label} (${(det.confidence * 100).toFixed(0)}%)`;
            
            // Get color based on waste category
            const color = categoryColors[category] || '#888888';
            
            // Draw the bounding box
            ctx.strokeStyle = color;
            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
            
            // Draw the label background
            ctx.fillStyle = color;
            const textWidth = ctx.measureText(displayText).width;
            ctx.fillRect(x1, y1 - 25, textWidth + 10, 28);
            
            // Draw the label text
            ctx.fillStyle = '#FFFFFF';
            ctx.fillText(displayText, x1 + 5, y1 - 5);
          });
        }
      };
    }
  }, [results, preview, categoryColors, isWebcamActive]);

  // Clear selection
  const clearSelection = () => {
    setSelectedFile(null);
    setPreview(null);
    setResults(null);
    setError(null);
    setIsWebcamActive(false);
  };

  // Calculate total stats from history
  const totalStats = useMemo(() => {
    const stats = {};
    let totalItems = 0;
    sortingHistory.forEach(entry => {
      for (const category in entry.counts) {
        if (stats[category]) {
          stats[category] += entry.counts[category];
        } else {
          stats[category] = entry.counts[category];
        }
        totalItems += entry.counts[category];
      }
    });
    return { stats, totalItems };
  }, [sortingHistory]);

  const capture = useCallback(async () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        const blob = await fetch(imageSrc).then(res => res.blob());
        const file = new File([blob], "webcam-capture.jpg", { type: "image/jpeg" });
        handleFile(file);
        setIsWebcamActive(false);
      }
    }
  }, [webcamRef, handleFile]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>♻️ Smart Waste Sorter</h1>
        <p className="subtitle">Upload an image and let AI classify your waste for proper recycling.</p>
      </header>

      <main className="container">
        <section className="upload-section section-card">
          <h3><i className="fas fa-cloud-upload-alt"></i> Upload Waste Image</h3>
          
          <div 
            className={`file-input-wrapper ${dragging ? 'dragging' : ''}`}
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
          >
            <input 
              type="file" 
              id="file-upload" 
              onChange={onFileChange} 
              accept="image/*"
              disabled={loading}
            />
            <label htmlFor="file-upload" className={`file-input-label ${loading ? 'disabled' : ''}`}>
              <i className="fas fa-file-upload"></i> Select Image
            </label>
            <span className="file-name" id="selected-file-name">
              {selectedFile ? selectedFile.name : 'No file selected'}
            </span>
          </div>
          
          <div className="button-group">
            <button 
              onClick={onFileUpload} 
              disabled={loading || !selectedFile}
              className="btn btn-primary"
              id="classify-btn"
            >
              <i className="fas fa-sort-amount-up"></i> {loading ? 'Analyzing...' : 'Classify'}
            </button>
            <button 
              onClick={clearSelection}
              disabled={loading || (!selectedFile && !results)}
              className="btn btn-secondary"
              id="reset-btn"
            >
              <i className="fas fa-redo-alt"></i> Reset
            </button>
            <button
              onClick={() => {
                clearSelection();
                setIsWebcamActive(!isWebcamActive);
              }}
              className="btn btn-primary"
            >
              <i className={`fas ${isWebcamActive ? 'fa-times-circle' : 'fa-camera'}`}></i> {isWebcamActive ? 'Close Camera' : 'Open Camera'}
            </button>
          </div>

          {error &&
            <p className="error-message" id="error-box">
              Error: {error}
            </p>
          }
        </section>
        
        <div className="content">
          <section className="canvas-section section-card">
            <h3><i className="fas fa-image"></i> Image Preview & Results</h3>
            <div className="canvas-container">
              {!isWebcamActive && !preview && (
                <p id="placeholder-text" style={{ color: 'var(--color-text-light)' }}>
                  Image will appear here after upload.
                </p>
              )}
              {preview && !isWebcamActive && (
                <canvas ref={canvasRef} id="image-canvas"></canvas>
              )}
              {isWebcamActive && (
                <div className="webcam-container">
                  <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width="100%"
                    height="100%"
                    videoConstraints={{ facingMode: "environment" }}
                  />
                  <button onClick={capture} className="btn btn-primary capture-btn">
                    <i className="fas fa-camera"></i> Capture Photo
                  </button>
                </div>
              )}
            </div>
          </section>

          {results && (
            <section className="results-section section-card">
              <h3><i className="fas fa-chart-bar"></i> Classification Results</h3>
              <div className="counts-container" id="results-list">
                {results.counts && Object.keys(results.counts).length > 0 ? (
                  Object.entries(results.counts)
                    .sort((a, b) => b[1] - a[1])
                    .map(([category, count]) => (
                      <div key={category} className="count-item">
                        <div className="category-info">
                          <div 
                            className="color-indicator" 
                            style={{ backgroundColor: categoryColors[category] }}
                          />
                          <div>
                            <span className="category-name">{category}</span>
                            <p className="recycling-tip">{recyclingInfo[category]}</p>
                          </div>
                        </div>
                        <span className="count-badge">{count} Items</span>
                      </div>
                    ))
                ) : (
                  <p>No objects detected.</p>
                )}
              </div>
                <p className="summary" id="summary-message">
                  <strong>Total Objects Detected:</strong> {results.total_objects}
                </p>
            </section>
          )}
        </div>
          
        <section className="instructions section-card">
          <h3><i className="fas fa-info-circle"></i> How to Use & Waste Categories</h3>
          <h4>Usage Guide:</h4>
          <ol>
            <li>Click <strong>'Select Image'</strong>, drag and drop an image, or use the <strong>'Open Camera'</strong> button.</li>
            <li>Click the <strong>'Classify'</strong> button to start the AI analysis.</li>
            <li>View the image on the left, where detected items will be marked with a color-coded box.</li>
            <li>Check the <strong>'Classification Results'</strong> on the right for a count of each waste type.</li>
          </ol>
          
          <div className="categories-legend">
            <h4>Category Legend:</h4>
            <div className="legend-items">
              {Object.entries(categoryColors).map(([category, color]) => (
                <div key={category} className="legend-item">
                  <div 
                    className="legend-color" 
                    style={{ backgroundColor: color }}
                  />
                  <span>{category}</span>
                </div>
              ))}
            </div>
          </div>
        </section>
        
        {/* Personal Stats Section */}
        {sortingHistory.length > 0 && (
          <section className="stats-section section-card">
            <h3><i className="fas fa-history"></i> Your Sorting History</h3>
            <div className="counts-container">
              {Object.entries(totalStats.stats)
                .sort((a, b) => b[1] - a[1])
                .map(([category, count]) => (
                <div key={category} className="count-item">
                  <div className="category-info">
                  <div
                    className="color-indicator"
                    style={{ backgroundColor: categoryColors[category] || '#888888' }}
                  />
                  <span className="category-name">{category}</span>
                  </div>
                  <span className="count-badge">{count}</span>
                </div>
              ))}
            </div>
            <div className="summary">
              <strong>Total Items Sorted:</strong> {totalStats.totalItems}
            </div>
            <button
              onClick={() => {
                if(window.confirm("Are you sure you want to clear your sorting history?")) {
                  setSortingHistory([]);
                }
              }}
              className="btn btn-secondary"
              style={{marginTop: '1rem', width: '100%'}}
            >
              <i className="fas fa-trash-alt"></i> Clear History
            </button>
          </section>
        )}
      </main>

      <footer className="App-footer">
        &copy; 2025 Smart Waste Sorter App. All Rights Reserved.
      </footer>
    </div>
  );
}

export default App;
