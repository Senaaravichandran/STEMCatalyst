import React, { useState } from 'react';
import './ImageGenerator.css';

const ImageGenerator = () => {
  const [activeTab, setActiveTab] = useState('generate');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Available Models - Fixed list with descriptions for consistent display
  const [selectedModel, setSelectedModel] = useState('flux');
  const [storyModel, setStoryModel] = useState('flux');

  // All available models with descriptions
  const allModels = [
    { id: 'flux', name: 'flux', description: 'High Quality' },
    { id: 'flux-realism', name: 'flux-realism', description: 'Photorealistic' },
    { id: 'flux-cablyai', name: 'flux-cablyai', description: 'Creative Art' },
    { id: 'flux-anime', name: 'flux-anime', description: 'Anime Style' },
    { id: 'flux-3d', name: 'flux-3d', description: '3D Rendered' },
    { id: 'flux-pro', name: 'flux-pro', description: 'Professional' },
    { id: 'turbo', name: 'turbo', description: 'Fast Speed' },
    { id: 'dall-e-3', name: 'dall-e-3', description: 'OpenAI Best' },
    { id: 'sdxl', name: 'sdxl', description: 'Stable Diffusion' },
    { id: 'sdxl-turbo', name: 'sdxl-turbo', description: 'SD Fast' },
    { id: 'kandinsky', name: 'kandinsky', description: 'Artistic Style' },
    { id: 'playground', name: 'playground', description: 'Experimental' },
    { id: 'pixart', name: 'pixart', description: 'Pixel Perfect' },
    { id: 'dreamshaper', name: 'dreamshaper', description: 'Dream Style' },
    { id: 'realistic-vision', name: 'realistic-vision', description: 'Ultra Real' }
  ];

  // Image Generation State
  const [imagePrompt, setImagePrompt] = useState('');
  const [imageContext, setImageContext] = useState('');
  const [imageSize, setImageSize] = useState('1024x1024');
  const [imageQuality, setImageQuality] = useState('standard');
  const [imageStyle, setImageStyle] = useState('vivid');

  // Story Concept Explainer State
  const [storyConcept, setStoryConcept] = useState('');
  const [storySubject, setStorySubject] = useState('Physics');
  const [numberOfSteps, setNumberOfSteps] = useState(4);
  const [storyImages, setStoryImages] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isGeneratingStory, setIsGeneratingStory] = useState(false);

  // Image Analysis State
  const [analysisImageFile, setAnalysisImageFile] = useState(null);
  const [analysisImagePreview, setAnalysisImagePreview] = useState('');
  const [analysisQuestion, setAnalysisQuestion] = useState('');

  // Lightbox Modal State
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxImage, setLightboxImage] = useState('');
  const [lightboxTitle, setLightboxTitle] = useState('');
  const [zoomLevel, setZoomLevel] = useState(1);

  // Reset functions for "Generate Another" buttons
  const resetImageGeneration = () => {
    setImagePrompt('');
    setImageContext('');
    setResult(null);
    setError(null);
  };

  const resetStoryExplainer = () => {
    setStoryConcept('');
    setStoryImages([]);
    setResult(null);
    setError(null);
  };

  const resetImageAnalysis = () => {
    setAnalysisImageFile(null);
    setAnalysisImagePreview('');
    setAnalysisQuestion('');
    setResult(null);
    setError(null);
  };

  // Lightbox functions
  const openLightbox = (imageUrl, title = 'Generated Image') => {
    setLightboxImage(imageUrl);
    setLightboxTitle(title);
    setZoomLevel(1);
    setLightboxOpen(true);
    document.body.style.overflow = 'hidden'; // Prevent background scroll
  };

  const closeLightbox = () => {
    setLightboxOpen(false);
    setLightboxImage('');
    setLightboxTitle('');
    setZoomLevel(1);
    document.body.style.overflow = 'auto';
  };

  const zoomIn = () => {
    setZoomLevel(prev => Math.min(prev + 0.25, 3));
  };

  const zoomOut = () => {
    setZoomLevel(prev => Math.max(prev - 0.25, 0.5));
  };

  const resetZoom = () => {
    setZoomLevel(1);
  };

  const downloadImage = async () => {
    try {
      const response = await fetch(lightboxImage);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${lightboxTitle.replace(/[^a-z0-9]/gi, '_')}_${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      // Fallback: open in new tab
      window.open(lightboxImage, '_blank');
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAnalysisImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setAnalysisImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const generateImage = async () => {
    if (!imagePrompt.trim()) {
      setError('Please enter an image prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Parse size
      const [width, height] = imageSize.split('x').map(Number);
      
      // Build prompt with context
      let fullPrompt = imagePrompt;
      if (imageContext.trim()) {
        fullPrompt += `. Context: ${imageContext}`;
      }
      if (imageStyle === 'vivid') {
        fullPrompt += '. Style: vibrant, colorful, high contrast';
      } else {
        fullPrompt += '. Style: natural, realistic, soft colors';
      }
      
      // Generate unique seed to prevent caching
      const uniqueSeed = Math.floor(Math.random() * 1000000000);
      
      // Use Pollinations API with selected model - ensure model is URL encoded
      const encodedPrompt = encodeURIComponent(fullPrompt);
      const encodedModel = encodeURIComponent(selectedModel);
      const imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?model=${encodedModel}&width=${width}&height=${height}&nologo=true&seed=${uniqueSeed}&nocache=${Date.now()}`;
      
      console.log('Generating image with model:', selectedModel);
      console.log('Image URL:', imageUrl);
      
      // Pre-load image to ensure it's generated before showing
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        setResult({
          success: true,
          image_url: imageUrl,
          model: selectedModel,
          revised_prompt: fullPrompt,
          metadata: {
            size: imageSize,
            quality: imageQuality,
            style: imageStyle,
            seed: uniqueSeed
          }
        });
        setLoading(false);
      };
      img.onerror = () => {
        setError(`Failed to generate image with model: ${selectedModel}. Please try again.`);
        setLoading(false);
      };
      img.src = imageUrl;
    } catch (err) {
      setError('Network error. Please check your connection.');
      console.error('Error:', err);
      setLoading(false);
    }
  };

  const generateStoryExplanation = async () => {
    if (!storyConcept.trim()) {
      setError('Please enter a concept');
      return;
    }

    setIsGeneratingStory(true);
    setError(null);
    setStoryImages([]);
    setCurrentStep(0);

    // Generate step descriptions based on concept
    const stepDescriptions = getStepDescriptions(storyConcept, storySubject, numberOfSteps);

    try {
      const generatedImages = [];
      
      for (let i = 0; i < numberOfSteps; i++) {
        setCurrentStep(i + 1);
        
        const stepPrompt = `Educational illustration Step ${i + 1} of ${numberOfSteps}: ${stepDescriptions[i]}. Subject: ${storySubject}. Style: clean, educational, scientific diagram, labeled, clear visuals, professional textbook illustration.`;
        
        // Generate unique seed for each image
        const uniqueSeed = Math.floor(Math.random() * 1000000000) + i;
        
        // Use Pollinations API for each step with selected model - URL encode model
        const encodedPrompt = encodeURIComponent(stepPrompt);
        const encodedModel = encodeURIComponent(storyModel);
        const imageUrl = `https://image.pollinations.ai/prompt/${encodedPrompt}?model=${encodedModel}&width=512&height=512&nologo=true&seed=${uniqueSeed}&nocache=${Date.now() + i}`;
        
        console.log(`Step ${i + 1} using model:`, storyModel);
        
        // Wait for image to load before adding to array
        await new Promise((resolve, reject) => {
          const img = new Image();
          img.onload = () => {
            generatedImages.push({
              step: i + 1,
              title: `Step ${i + 1}: ${stepDescriptions[i].split('.')[0]}`,
              description: stepDescriptions[i],
              imageUrl: imageUrl,
              model: storyModel
            });
            setStoryImages([...generatedImages]);
            resolve();
          };
          img.onerror = () => {
            // Still add the image URL even if preload fails
            generatedImages.push({
              step: i + 1,
              title: `Step ${i + 1}: ${stepDescriptions[i].split('.')[0]}`,
              description: stepDescriptions[i],
              imageUrl: imageUrl,
              model: storyModel
            });
            setStoryImages([...generatedImages]);
            resolve();
          };
          img.src = imageUrl;
        });
        
        // Small delay between generations
        if (i < numberOfSteps - 1) {
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      }
      
      setResult({ success: true, type: 'story', images: generatedImages });
    } catch (err) {
      setError('Failed to generate story explanation. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsGeneratingStory(false);
      setCurrentStep(0);
    }
  };

  const getStepDescriptions = (concept, subject, steps) => {
    // Generate educational step descriptions based on concept
    const descriptions = [];
    
    // Generic step templates that work for any concept
    const templates = [
      `Introduction to ${concept}: Basic definition and fundamental principles in ${subject}`,
      `Key components and structure of ${concept}: Visual breakdown of main elements`,
      `How ${concept} works: The process and mechanism explained visually`,
      `Real-world applications of ${concept}: Practical examples in ${subject}`,
      `${concept} in action: Step-by-step demonstration of the process`,
      `Advanced aspects of ${concept}: Complex interactions and relationships`,
      `${concept} compared: Similarities and differences with related concepts`,
      `Summary of ${concept}: Key takeaways and important formulas`
    ];
    
    for (let i = 0; i < steps; i++) {
      descriptions.push(templates[i % templates.length]);
    }
    
    return descriptions;
  };

  const analyzeImage = async () => {
    if (!analysisImageFile && !analysisImagePreview) {
      setError('Please upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // Use Pollinations text API for image analysis
      const questionText = analysisQuestion.trim() || 'Describe this image in detail, including any educational or scientific content visible.';
      
      const response = await fetch('https://text.pollinations.ai/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: [
            {
              role: 'user',
              content: [
                {
                  type: 'text',
                  text: questionText
                },
                {
                  type: 'image_url',
                  image_url: {
                    url: analysisImagePreview
                  }
                }
              ]
            }
          ],
          model: 'openai',
          seed: Date.now()
        }),
      });

      const analysisText = await response.text();

      if (analysisText) {
        setResult({
          success: true,
          analysis: analysisText,
          model: 'Pollinations AI Vision',
          image_preview: analysisImagePreview
        });
      } else {
        setError('Failed to analyze image. Please try again.');
      }
    } catch (err) {
      setError('Failed to analyze image. Please check your connection.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="image-generator">
      <div className="header">
        <h2>🎨 AI Image Generator & Analyzer</h2>
        <p>Powered by Pollinations AI with multiple models (Flux, DALL-E, Turbo & more)</p>
      </div>

      <div className="tabs">
        <button 
          className={activeTab === 'generate' ? 'active' : ''} 
          onClick={() => setActiveTab('generate')}
        >
          🖼️ Generate Image
        </button>
        <button 
          className={activeTab === 'story' ? 'active' : ''} 
          onClick={() => setActiveTab('story')}
        >
          📚 Story Explainer
        </button>
        <button 
          className={activeTab === 'analyze' ? 'active' : ''} 
          onClick={() => setActiveTab('analyze')}
        >
          👁️ Analyze Image
        </button>
      </div>

      <div className="content">
        {activeTab === 'generate' && (
          <div className="tab-content">
            <h3>Generate Custom Image</h3>
            <div className="form-group">
              <label>Image Prompt:</label>
              <textarea
                value={imagePrompt}
                onChange={(e) => setImagePrompt(e.target.value)}
                placeholder="Describe the image you want to generate..."
                rows={3}
              />
            </div>
            <div className="form-group">
              <label>Context (Optional):</label>
              <input
                type="text"
                value={imageContext}
                onChange={(e) => setImageContext(e.target.value)}
                placeholder="Additional context for the image..."
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>🤖 AI Model:</label>
                <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)} className="model-select">
                  {allModels.map(model => (
                    <option key={model.id} value={model.id}>
                      {model.name} - {model.description}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Size:</label>
                <select value={imageSize} onChange={(e) => setImageSize(e.target.value)}>
                  <option value="1024x1024">1024x1024</option>
                  <option value="1792x1024">1792x1024</option>
                  <option value="1024x1792">1024x1792</option>
                </select>
              </div>
              <div className="form-group">
                <label>Quality:</label>
                <select value={imageQuality} onChange={(e) => setImageQuality(e.target.value)}>
                  <option value="standard">Standard</option>
                  <option value="hd">HD</option>
                </select>
              </div>
              <div className="form-group">
                <label>Style:</label>
                <select value={imageStyle} onChange={(e) => setImageStyle(e.target.value)}>
                  <option value="vivid">Vivid</option>
                  <option value="natural">Natural</option>
                </select>
              </div>
            </div>
            <div className="button-row">
              <button 
                onClick={generateImage} 
                disabled={loading || !imagePrompt.trim()}
                className="generate-btn"
              >
                {loading ? '🔄 Generating...' : '🎨 Generate Image'}
              </button>
              {result && (
                <button 
                  onClick={resetImageGeneration}
                  className="reset-btn"
                >
                  🔄 Generate Another
                </button>
              )}
            </div>
          </div>
        )}

        {activeTab === 'story' && (
          <div className="tab-content">
            <h3>📚 Story Concept Explainer</h3>
            <p className="subtitle">Generate step-by-step visual explanations for any concept</p>
            
            <div className="form-group">
              <label>Concept Name:</label>
              <input
                type="text"
                value={storyConcept}
                onChange={(e) => setStoryConcept(e.target.value)}
                placeholder="e.g., Photosynthesis, Newton's Laws, Cell Division..."
              />
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label>Subject:</label>
                <select value={storySubject} onChange={(e) => setStorySubject(e.target.value)}>
                  <option value="Physics">Physics</option>
                  <option value="Chemistry">Chemistry</option>
                  <option value="Mathematics">Mathematics</option>
                  <option value="Biology">Biology</option>
                  <option value="Computer Science">Computer Science</option>
                  <option value="General Science">General Science</option>
                </select>
              </div>
              <div className="form-group">
                <label>Number of Steps:</label>
                <select value={numberOfSteps} onChange={(e) => setNumberOfSteps(parseInt(e.target.value))}>
                  <option value={3}>3 Steps</option>
                  <option value={4}>4 Steps</option>
                  <option value={5}>5 Steps</option>
                  <option value={6}>6 Steps</option>
                  <option value={8}>8 Steps</option>
                </select>
              </div>
              <div className="form-group">
                <label>🤖 AI Model:</label>
                <select value={storyModel} onChange={(e) => setStoryModel(e.target.value)} className="model-select">
                  {allModels.map(model => (
                    <option key={model.id} value={model.id}>
                      {model.name} - {model.description}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            
            <div className="button-row">
              <button 
                onClick={generateStoryExplanation} 
                disabled={isGeneratingStory || !storyConcept.trim()}
                className="generate-btn"
              >
                {isGeneratingStory ? `🔄 Generating Step ${currentStep}/${numberOfSteps}...` : '📚 Generate Story Explanation'}
              </button>
              {storyImages.length > 0 && !isGeneratingStory && (
                <button 
                  onClick={resetStoryExplainer}
                  className="reset-btn"
                >
                  🔄 Generate Another Story
                </button>
              )}
            </div>

            {/* Story Images Display */}
            {storyImages.length > 0 && (
              <div className="story-results">
                <h4>🌟 Visual Story: {storyConcept}</h4>
                <p className="story-model-info">🤖 Generated with model: <strong>{storyModel}</strong></p>
                <p className="click-hint">💡 Click any image to view full size & download</p>
                <div className="story-grid">
                  {storyImages.map((step, index) => (
                    <div key={index} className="story-step">
                      <div className="step-number">Step {step.step}</div>
                      <img 
                        src={step.imageUrl} 
                        alt={step.title}
                        className="clickable-image"
                        onClick={() => openLightbox(step.imageUrl, `Step ${step.step}: ${storyConcept}`)}
                        title="Click to view full size"
                        onError={(e) => {
                          e.target.src = 'https://via.placeholder.com/512x512?text=Loading...';
                        }}
                      />
                      <div className="step-content">
                        <h5>{step.title}</h5>
                        <p>{step.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'analyze' && (
          <div className="tab-content">
            <h3>🔍 Analyze Image with AI Vision</h3>
            <p className="subtitle">Upload an image to get AI-powered analysis</p>
            
            <div className="form-group">
              <label>Upload Image:</label>
              <div className="upload-area">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  id="image-upload"
                  className="file-input"
                />
                <label htmlFor="image-upload" className="upload-label">
                  {analysisImagePreview ? (
                    <div className="preview-container">
                      <img src={analysisImagePreview} alt="Preview" className="image-preview" />
                      <span className="change-text">📷 Click to change image</span>
                    </div>
                  ) : (
                    <div className="upload-placeholder">
                      <span className="upload-icon">📷</span>
                      <span>Click to upload an image</span>
                      <span className="upload-hint">Supports JPG, PNG, GIF, WebP</span>
                    </div>
                  )}
                </label>
              </div>
            </div>
            
            <div className="form-group">
              <label>Question (Optional):</label>
              <input
                type="text"
                value={analysisQuestion}
                onChange={(e) => setAnalysisQuestion(e.target.value)}
                placeholder="Ask a specific question about the image..."
              />
            </div>
            
            <div className="button-row">
              <button 
                onClick={analyzeImage} 
                disabled={loading || !analysisImagePreview}
                className="generate-btn"
              >
                {loading ? '🔄 Analyzing...' : '👁️ Analyze Image'}
              </button>
              {result && result.analysis && (
                <button 
                  onClick={resetImageAnalysis}
                  className="reset-btn"
                >
                  🔄 Analyze Another
                </button>
              )}
            </div>
          </div>
        )}

        {error && (
          <div className="error-message">
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {result && (
          <div className="result-section">
            <h3>✅ Result</h3>
            
            {result.image_url && (
              <div className="image-result">
                <img 
                  src={result.image_url} 
                  alt="Generated" 
                  className="generated-image clickable-image"
                  onClick={() => openLightbox(result.image_url, `Generated Image - ${result.model}`)}
                  title="Click to view full size"
                />
                <div className="image-info">
                  <p className="model-badge"><strong>🤖 Model Used:</strong> <span className="model-name">{result.model}</span></p>
                  {result.revised_prompt && (
                    <p><strong>📝 Prompt:</strong> {result.revised_prompt}</p>
                  )}
                  {result.metadata && (
                    <div className="metadata">
                      <p><strong>📐 Size:</strong> {result.metadata.size}</p>
                      <p><strong>✨ Style:</strong> {result.metadata.style}</p>
                      {result.metadata.seed && (
                        <p><strong>🎲 Seed:</strong> {result.metadata.seed}</p>
                      )}
                    </div>
                  )}
                </div>
              </div>
            )}

            {result.analysis && (
              <div className="analysis-result">
                {result.image_preview && (
                  <div className="analyzed-image-container">
                    <img src={result.image_preview} alt="Analyzed" className="analyzed-image" />
                  </div>
                )}
                <div className="analysis-content">
                  <h4>🔍 Analysis Result</h4>
                  <div className="analysis-text">{result.analysis}</div>
                  <p className="model-info"><strong>Model:</strong> {result.model}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Lightbox Modal */}
      {lightboxOpen && (
        <div className="lightbox-overlay" onClick={closeLightbox}>
          <div className="lightbox-container" onClick={(e) => e.stopPropagation()}>
            <div className="lightbox-header">
              <h3>{lightboxTitle}</h3>
              <button className="lightbox-close" onClick={closeLightbox}>✕</button>
            </div>
            <div className="lightbox-image-container">
              <img 
                src={lightboxImage} 
                alt={lightboxTitle}
                style={{ transform: `scale(${zoomLevel})` }}
                className="lightbox-image"
              />
            </div>
            <div className="lightbox-controls">
              <button onClick={zoomOut} disabled={zoomLevel <= 0.5} title="Zoom Out">
                🔍➖
              </button>
              <button onClick={resetZoom} title="Reset Zoom">
                {Math.round(zoomLevel * 100)}%
              </button>
              <button onClick={zoomIn} disabled={zoomLevel >= 3} title="Zoom In">
                🔍➕
              </button>
              <button onClick={downloadImage} className="download-btn" title="Download Image">
                ⬇️ Download
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageGenerator;
