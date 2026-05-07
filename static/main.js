document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    
    const uploadPanel = document.getElementById('upload-panel');
    const loadingPanel = document.getElementById('loading-panel');
    const resultsPanel = document.getElementById('results-panel');
    
    const resetBtn = document.getElementById('reset-btn');
    const storyText = document.getElementById('story-text');
    const timeline = document.getElementById('timeline');

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });

    // Browse button
    browseBtn.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    // Reset
    resetBtn.addEventListener('click', () => {
        fileInput.value = '';
        resultsPanel.classList.add('hidden');
        uploadPanel.classList.remove('hidden');
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        const file = files[0];
        
        if (!file.type.startsWith('video/')) {
            alert('Please upload a video file.');
            return;
        }

        uploadVideo(file);
    }

    async function uploadVideo(file) {
        // Show loading state
        uploadPanel.classList.add('hidden');
        loadingPanel.classList.remove('hidden');

        const formData = new FormData();
        formData.append('video', file);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            displayResults(data);

        } catch (error) {
            console.error(error);
            alert('Error analyzing video. Please try again.');
            loadingPanel.classList.add('hidden');
            uploadPanel.classList.remove('hidden');
        }
    }

    function displayResults(data) {
        // Hide loading, show results
        loadingPanel.classList.add('hidden');
        resultsPanel.classList.remove('hidden');

        // Set story
        storyText.textContent = data.story || "No story generated.";

        // Clear and build timeline
        timeline.innerHTML = '';
        
        if (data.events && data.events.length > 0) {
            data.events.forEach((event, index) => {
                const delay = index * 0.1; // Staggered animation
                
                const item = document.createElement('div');
                item.className = 'timeline-item';
                item.style.animationDelay = `${delay}s`;

                let tagsHtml = '';
                if (event.objects && event.objects.length > 0) {
                    tagsHtml = `<div class="objects-tags">
                        ${event.objects.map(obj => `<span class="tag">${obj}</span>`).join('')}
                    </div>`;
                }

                item.innerHTML = `
                    <div class="time-badge">${event.time}</div>
                    <div class="event-caption">${event.caption}</div>
                    ${tagsHtml}
                `;
                
                timeline.appendChild(item);
            });
        } else {
            timeline.innerHTML = '<p>No key moments detected.</p>';
        }
    }
});
