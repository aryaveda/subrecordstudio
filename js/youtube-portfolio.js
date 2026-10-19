/**
 * YouTube Portfolio Engine for Sub-Record Studio
 * Automatically loads and renders videos from data/youtube-portfolio.json
 * Supports filtering by category, search, and inline modal video player.
 */

(function () {
    'use strict';

    let allVideos = [];
    let currentCategory = 'all';

    // Video modal DOM elements
    let modalEl = null;
    let iframeEl = null;

    function initVideoModal() {
        if (document.getElementById('srs-video-modal')) return;

        const modalHtml = `
            <div id="srs-video-modal" class="srs-modal-overlay" style="display:none;">
                <div class="srs-modal-dialog">
                    <button class="srs-modal-close" aria-label="Close modal">&times;</button>
                    <div class="srs-video-responsive">
                        <iframe id="srs-modal-iframe" src="" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </div>
                    <div class="srs-modal-info">
                        <h4 id="srs-modal-title">Video Title</h4>
                        <p id="srs-modal-meta">Artist / Release</p>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        modalEl = document.getElementById('srs-video-modal');
        iframeEl = document.getElementById('srs-modal-iframe');
        const closeBtn = modalEl.querySelector('.srs-modal-close');

        function closeModal() {
            modalEl.style.display = 'none';
            iframeEl.src = '';
            document.body.style.overflow = '';
        }

        closeBtn.addEventListener('click', closeModal);
        modalEl.addEventListener('click', function (e) {
            if (e.target === modalEl) closeModal();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && modalEl.style.display !== 'none') {
                closeModal();
            }
        });
    }

    function openModal(video) {
        if (!modalEl) initVideoModal();
        const titleEl = document.getElementById('srs-modal-title');
        const metaEl = document.getElementById('srs-modal-meta');

        titleEl.textContent = video.title;
        metaEl.textContent = `${video.artist} • ${video.category_label || video.category} • ${video.formatted_date || ''}`;
        iframeEl.src = `https://www.youtube.com/embed/${video.id}?autoplay=1&rel=0`;
        modalEl.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function getCategoryBadgeColor(category) {
        switch (category) {
            case 'original':
                return '#e53637'; // Studio red
            case 'live':
                return '#009688'; // Teal
            case 'cover':
                return '#3f51b5'; // Indigo
            case 'tutorial':
                return '#ff9800'; // Amber
            default:
                return '#e53637';
        }
    }

    function createVideoCard(video) {
        const badgeColor = getCategoryBadgeColor(video.category);
        const card = document.createElement('div');
        card.className = 'col-12 col-sm-6 col-md-4 col-lg-3 mb-4 srs-portfolio-card';
        card.setAttribute('data-category', video.category);

        card.innerHTML = `
            <div class="single-album-area h-100 srs-video-card" style="background:#151515; border-radius:10px; overflow:hidden; border:1px solid #282828; display:flex; flex-direction:column; transition:transform 0.3s ease, box-shadow 0.3s ease;">
                <div class="srs-thumb-wrap" style="position:relative; width:100%; aspect-ratio:16/9; overflow:hidden; cursor:pointer;">
                    <img src="${video.thumbnail}" alt="${video.title}" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s ease;" class="srs-card-img" loading="lazy">
                    <span style="position:absolute; top:10px; left:10px; background:${badgeColor}; color:#fff; font-size:11px; font-weight:700; text-transform:uppercase; padding:3px 8px; border-radius:4px; letter-spacing:0.5px;">
                        ${video.category_label || video.category}
                    </span>
                    <div class="srs-play-overlay" style="position:absolute; inset:0; background:rgba(0,0,0,0.45); display:flex; align-items:center; justify-content:center; opacity:0; transition:opacity 0.3s ease;">
                        <span style="width:50px; height:50px; border-radius:50%; background:#e53637; color:#fff; display:flex; align-items:center; justify-content:center; font-size:18px; box-shadow:0 0 20px rgba(229,54,55,0.8);">
                            <i class="fa fa-play" style="margin-left:3px;"></i>
                        </span>
                    </div>
                </div>
                <div class="album-info p-3" style="flex:1; display:flex; flex-direction:column; justify-content:space-between;">
                    <div>
                        <h6 style="color:#fff; font-size:14px; line-height:1.4; margin-bottom:6px; font-weight:600; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden;" title="${video.title}">
                            ${video.title}
                        </h6>
                        <p style="color:#aaa; font-size:12px; margin-bottom:4px;">
                            <i class="fa fa-user-circle-o mr-1"></i> ${video.artist}
                        </p>
                        <p style="color:#777; font-size:11px; margin-bottom:12px;">
                            <i class="fa fa-calendar mr-1"></i> ${video.formatted_date || ''}
                        </p>
                    </div>
                    <div class="d-flex align-items-center justify-content-between pt-2" style="border-top:1px solid #222;">
                        <button class="btn btn-sm btn-outline-danger srs-play-btn" style="font-size:11px; padding:4px 10px; border-radius:4px;">
                            <i class="fa fa-play mr-1"></i> Putar Video
                        </button>
                        <a href="${video.youtube_url}" target="_blank" rel="noopener noreferrer" style="color:#888; font-size:16px; transition:color 0.2s ease;" title="Tonton di YouTube">
                            <i class="fa-brands fa-youtube" style="color:#ff0000; font-size:18px;"></i>
                        </a>
                    </div>
                </div>
            </div>
        `;

        // Click handlers to open video modal
        const thumbWrap = card.querySelector('.srs-thumb-wrap');
        const playBtn = card.querySelector('.srs-play-btn');

        thumbWrap.addEventListener('click', () => openModal(video));
        playBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            openModal(video);
        });

        // Hover effect for play overlay
        thumbWrap.addEventListener('mouseenter', () => {
            const overlay = thumbWrap.querySelector('.srs-play-overlay');
            const img = thumbWrap.querySelector('.srs-card-img');
            overlay.style.opacity = '1';
            img.style.transform = 'scale(1.05)';
        });
        thumbWrap.addEventListener('mouseleave', () => {
            const overlay = thumbWrap.querySelector('.srs-play-overlay');
            const img = thumbWrap.querySelector('.srs-card-img');
            overlay.style.opacity = '0';
            img.style.transform = 'scale(1)';
        });

        return card;
    }

    function renderPortfolio(containerId, limit = 0) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = '';

        let filtered = allVideos;
        if (currentCategory !== 'all') {
            filtered = allVideos.filter(v => v.category === currentCategory);
        }

        if (limit > 0) {
            filtered = filtered.slice(0, limit);
        }

        if (filtered.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <p style="color:#888; font-size:16px;">Tidak ada video ditemukan untuk kategori ini.</p>
                </div>
            `;
            return;
        }

        filtered.forEach(video => {
            container.appendChild(createVideoCard(video));
        });
    }

    function setupFilterButtons() {
        const filterBtns = document.querySelectorAll('.srs-portfolio-filter button');
        if (!filterBtns.length) return;

        filterBtns.forEach(btn => {
            btn.addEventListener('click', function () {
                filterBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                currentCategory = this.getAttribute('data-filter') || 'all';
                renderPortfolio('srs-portfolio-grid');
            });
        });
    }

    // Load data from JSON
    async function loadPortfolioData() {
        try {
            // Add cache-busting timestamp to avoid stale browser cache
            const resp = await fetch('data/youtube-portfolio.json?t=' + Date.now());
            if (!resp.ok) throw new Error(`HTTP error! status: ${resp.status}`);
            const data = await resp.json();
            allVideos = data.videos || [];
            
            // Render on latest releases page if present
            if (document.getElementById('srs-portfolio-grid')) {
                renderPortfolio('srs-portfolio-grid');
                setupFilterButtons();
            }

            // Render on homepage if present (top 6 releases)
            if (document.getElementById('srs-home-portfolio-grid')) {
                renderPortfolio('srs-home-portfolio-grid', 6);
            }
        } catch (err) {
            console.warn('Could not load dynamic YouTube portfolio, falling back to static markup:', err);
        }
    }

    // Auto initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initVideoModal();
            loadPortfolioData();
        });
    } else {
        initVideoModal();
        loadPortfolioData();
    }

})();
