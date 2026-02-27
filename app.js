// Detect if running locally on port 8080 and point to port 8000 backend
const BASE_URL = window.location.port === '8080' ? 'http://127.0.0.1:8000' : '';
const API_URL = `${BASE_URL}/api/recommend`;
const OPTIONS_API_URL = `${BASE_URL}/api/options`;

document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('recommendation-form');
    const placeSelect = document.getElementById('place');
    const cuisineSelect = document.getElementById('cuisine');

    // UI States
    const emptyState = document.getElementById('empty-state');
    const loadingState = document.getElementById('loading-state');
    const resultsContent = document.getElementById('results-content');
    const errorState = document.getElementById('error-state');
    const errorMessage = document.getElementById('error-message');

    // Dynamic Content Areas
    const rationaleBox = document.getElementById('ai-rationale');
    const gridBox = document.getElementById('restaurants-grid');

    // Fetch dropdown options
    try {
        const res = await fetch(OPTIONS_API_URL);
        const optionsData = await res.json();

        placeSelect.innerHTML = '<option value="">Select Location</option>';
        optionsData.locations.forEach(loc => {
            const opt = document.createElement('option');
            opt.value = loc;
            opt.textContent = loc;
            placeSelect.appendChild(opt);
        });

        cuisineSelect.innerHTML = '<option value="">Select Cuisine</option>';
        optionsData.cuisines.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            cuisineSelect.appendChild(opt);
        });
    } catch (err) {
        console.error("Failed to load options", err);
        placeSelect.innerHTML = '<option value="">Error loading locations</option>';
        cuisineSelect.innerHTML = '<option value="">Error loading cuisines</option>';
    }

    // When location changes, fetch only available cuisines for that location
    placeSelect.addEventListener('change', async (e) => {
        const selectedLocation = e.target.value;
        const url = selectedLocation
            ? `${OPTIONS_API_URL}?location=${encodeURIComponent(selectedLocation)}`
            : OPTIONS_API_URL;

        cuisineSelect.innerHTML = '<option value="">Loading cuisines...</option>';

        try {
            const res = await fetch(url);
            const optionsData = await res.json();

            cuisineSelect.innerHTML = '<option value="">Select Cuisine</option>';
            optionsData.cuisines.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c;
                opt.textContent = c;
                cuisineSelect.appendChild(opt);
            });
        } catch (err) {
            console.error("Failed to update cuisines", err);
            cuisineSelect.innerHTML = '<option value="">Error loading cuisines</option>';
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Extract values
        const place = document.getElementById('place').value.trim();
        const cuisine = document.getElementById('cuisine').value.trim();
        const rawPrice = document.getElementById('max_price').value;
        const rawRating = document.getElementById('min_rating').value;

        const payload = {
            place: place,
            cuisine: cuisine,
        };

        if (rawPrice) payload.max_price = parseFloat(rawPrice);
        if (rawRating) payload.min_rating = parseFloat(rawRating);

        // Show Loading State
        emptyState.classList.add('hidden');
        resultsContent.classList.add('hidden');
        errorState.classList.add('hidden');
        loadingState.classList.remove('hidden');

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error('Failed to fetch recommendations from the Chef AI.');

            const data = await response.json();

            // Clear previous results
            gridBox.innerHTML = '';

            if (!data.recommendations || data.recommendations.length === 0) {
                rationaleBox.innerHTML = `<h3><span style="color:var(--accent-red)">Oops!</span></h3><p>${data.llm_rationale || "No restaurants found matching your criteria. Try adjusting your constraints."}</p>`;
            } else {
                // Populate Rationale
                rationaleBox.innerHTML = `<h3>Chef's Rationale</h3><p>${data.llm_rationale.replace(/\\n/g, '<br/>')}</p>`;

                // Construct Cards
                data.recommendations.forEach((r, index) => {
                    const costDisplay = r.cost ? `₹${r.cost} for two` : 'Cost N/A';
                    const ratingDisplay = r.rate ? `${r.rate} ★` : 'NEW';

                    const card = document.createElement('div');
                    card.className = 'restaurant-card';
                    card.style.animationDelay = `${index * 0.1}s`; // Staggered animation

                    card.innerHTML = `
                        <div class="r-header">
                            <span class="r-name">${r.name}</span>
                            <span class="r-rating">${ratingDisplay}</span>
                        </div>
                        <div class="r-cuisines">${r.cuisines}</div>
                        <div style="font-size: 0.85em; color: var(--text-secondary); margin-top: 0.2rem;">${r.address}</div>
                        
                        <div class="r-meta">
                            <span>${costDisplay}</span>
                            <a href="${r.url}" target="_blank" style="color:var(--accent-red); text-decoration:none; font-weight:600;">View Menu →</a>
                        </div>
                    `;
                    gridBox.appendChild(card);
                });
            }

            // Hide Loading, Show Results
            loadingState.classList.add('hidden');
            resultsContent.classList.remove('hidden');

        } catch (error) {
            console.error("Error fetching recommendations:", error);
            loadingState.classList.add('hidden');
            errorMessage.textContent = error.message;
            errorState.classList.remove('hidden');
        }
    });
});
