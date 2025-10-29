/**
 * Story to Comic Strip Generator - Frontend JavaScript
 */

// DOM Elements
const storyInput = document.getElementById('story-input');
const maxPanelsSlider = document.getElementById('max-panels');
const panelsValue = document.getElementById('panels-value');
const charCount = document.getElementById('char-count');
const generateBtn = document.getElementById('generate-btn');
const loadingSection = document.getElementById('loading-section');
const errorSection = document.getElementById('error-section');
const errorMessage = document.getElementById('error-message');
const dismissErrorBtn = document.getElementById('dismiss-error');
const outputSection = document.getElementById('output-section');
const comicPanelsContainer = document.getElementById('comic-panels');
const generateAnotherBtn = document.getElementById('generate-another');
const downloadBtn = document.getElementById('download-btn');
const exampleButtons = document.querySelectorAll('.btn-example');

// API Configuration
const API_BASE_URL = window.location.origin;

// State
let currentComic = null;

/**
 * Initialize the application
 */
function init() {
    // Update character count
    storyInput.addEventListener('input', updateCharCount);

    // Update slider value display
    maxPanelsSlider.addEventListener('input', updateSliderValue);

    // Generate comic button
    generateBtn.addEventListener('click', handleGenerate);

    // Example buttons
    exampleButtons.forEach(btn => {
        btn.addEventListener('click', handleExampleClick);
    });

    // Error dismiss button
    dismissErrorBtn.addEventListener('click', hideError);

    // Generate another button
    generateAnotherBtn.addEventListener('click', resetToInput);

    // Download button
    downloadBtn.addEventListener('click', handleDownload);

    // Enter key in textarea
    storyInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleGenerate();
        }
    });

    // Initial character count
    updateCharCount();
}

/**
 * Update character count display
 */
function updateCharCount() {
    const count = storyInput.value.length;
    charCount.textContent = count.toLocaleString();
}

/**
 * Update slider value display
 */
function updateSliderValue() {
    panelsValue.textContent = maxPanelsSlider.value;
}

/**
 * Handle example button click
 */
function handleExampleClick(e) {
    const exampleType = e.target.getAttribute('data-example');
    if (exampleStories[exampleType]) {
        storyInput.value = exampleStories[exampleType];
        updateCharCount();
        storyInput.focus();

        // Smooth scroll to textarea
        storyInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

/**
 * Handle generate button click
 */
async function handleGenerate() {
    const story = storyInput.value.trim();
    const maxPanels = parseInt(maxPanelsSlider.value);

    // Validate input
    if (!story) {
        showError('Please enter a story to generate a comic strip.');
        return;
    }

    if (story.length < 10) {
        showError('Your story is too short. Please write a longer story (at least 10 characters).');
        return;
    }

    // Show loading state
    showLoading();
    hideError();
    hideOutput();

    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                story: story,
                max_panels: maxPanels
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate comic strip');
        }

        if (data.success && data.panels) {
            currentComic = data;
            displayComic(data.panels);
            showOutput();
        } else {
            throw new Error('Invalid response from server');
        }

    } catch (error) {
        console.error('Error generating comic:', error);
        showError(error.message || 'Failed to generate comic strip. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Display the generated comic panels
 */
function displayComic(panels) {
    comicPanelsContainer.innerHTML = '';

    panels.forEach(panel => {
        const panelElement = createPanelElement(panel);
        comicPanelsContainer.appendChild(panelElement);
    });

    // Smooth scroll to output
    setTimeout(() => {
        outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Create a panel element
 */
function createPanelElement(panel) {
    const panelDiv = document.createElement('div');
    panelDiv.className = 'comic-panel';

    // Panel number
    const panelNumber = document.createElement('div');
    panelNumber.className = 'panel-number';
    panelNumber.textContent = panel.panel_number;
    panelDiv.appendChild(panelNumber);

    // Image (if exists)
    if (panel.image_data) {
        const imageContainer = document.createElement('div');
        imageContainer.className = 'panel-image-container';

        const img = document.createElement('img');
        img.className = 'panel-image';
        img.src = `data:image/png;base64,${panel.image_data}`;
        img.alt = `Panel ${panel.panel_number}: ${panel.scene}`;
        img.loading = 'lazy';

        imageContainer.appendChild(img);
        panelDiv.appendChild(imageContainer);
    }

    // Scene
    const sceneDiv = document.createElement('div');
    sceneDiv.className = 'panel-scene';

    const sceneLabel = document.createElement('div');
    sceneLabel.className = 'panel-scene-label';
    sceneLabel.textContent = 'Scene';
    sceneDiv.appendChild(sceneLabel);

    const sceneText = document.createElement('div');
    sceneText.className = 'panel-scene-text';
    sceneText.textContent = panel.scene;
    sceneDiv.appendChild(sceneText);

    panelDiv.appendChild(sceneDiv);

    // Narration (if exists)
    if (panel.narration) {
        const narrationDiv = document.createElement('div');
        narrationDiv.className = 'panel-narration';
        narrationDiv.textContent = panel.narration;
        panelDiv.appendChild(narrationDiv);
    }

    // Dialogues
    if (panel.dialogue && panel.dialogue.length > 0) {
        const dialogueContainer = document.createElement('div');
        dialogueContainer.className = 'panel-dialogue';

        panel.dialogue.forEach(dialogue => {
            const dialogueBubble = document.createElement('div');
            dialogueBubble.className = 'dialogue-bubble';

            const dialogueText = document.createElement('div');
            dialogueText.className = 'dialogue-text';
            dialogueText.textContent = dialogue;

            dialogueBubble.appendChild(dialogueText);
            dialogueContainer.appendChild(dialogueBubble);
        });

        panelDiv.appendChild(dialogueContainer);
    }

    return panelDiv;
}

/**
 * Handle download button click
 */
function handleDownload() {
    if (!currentComic) return;

    // Create a text representation of the comic
    let content = '=' .repeat(60) + '\n';
    content += 'COMIC STRIP\n';
    content += '='.repeat(60) + '\n\n';

    currentComic.panels.forEach(panel => {
        content += `Panel ${panel.panel_number}:\n`;
        content += `Scene: ${panel.scene}\n`;

        if (panel.narration) {
            content += `Narration: ${panel.narration}\n`;
        }

        if (panel.dialogue && panel.dialogue.length > 0) {
            content += 'Dialogue:\n';
            panel.dialogue.forEach(dialogue => {
                content += `  - ${dialogue}\n`;
            });
        }

        content += '\n';
    });

    content += '='.repeat(60) + '\n';
    content += 'Generated by Story to Comic Strip Generator\n';

    // Create download
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `comic-strip-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

/**
 * Show loading section
 */
function showLoading() {
    loadingSection.classList.remove('hidden');
    generateBtn.disabled = true;
}

/**
 * Hide loading section
 */
function hideLoading() {
    loadingSection.classList.add('hidden');
    generateBtn.disabled = false;
}

/**
 * Show error section
 */
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');

    // Smooth scroll to error
    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

/**
 * Hide error section
 */
function hideError() {
    errorSection.classList.add('hidden');
}

/**
 * Show output section
 */
function showOutput() {
    outputSection.classList.remove('hidden');
}

/**
 * Hide output section
 */
function hideOutput() {
    outputSection.classList.add('hidden');
}

/**
 * Reset to input view
 */
function resetToInput() {
    hideOutput();
    hideError();
    currentComic = null;

    // Smooth scroll to input
    storyInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    storyInput.focus();
}

/**
 * Check API configuration on load
 */
async function checkConfiguration() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/config`);
        const data = await response.json();

        if (!data.api_key_configured) {
            console.warn('Gemini API key is not configured');
            // You could show a warning banner here if needed
        }
    } catch (error) {
        console.error('Failed to check configuration:', error);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Check configuration
checkConfiguration();
