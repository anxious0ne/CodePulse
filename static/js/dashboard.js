// CodePulse Dashboard Client Scripts - Coders' Compass Colorful Edition

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value;

function showAlert(message, type = 'success') {
    const banner = document.getElementById('alert-banner');
    if (!banner) return;

    const isSuccess = type === 'success';
    banner.className = `p-4 rounded-lg text-sm flex items-center justify-between border-2 shadow-brutal font-bold ${
        isSuccess ? 'bg-compass-green text-compass-brown border-compass-brown' : 'bg-compass-error text-white border-compass-brown'
    }`;
    banner.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fa-solid ${isSuccess ? 'fa-circle-check text-base' : 'fa-triangle-exclamation text-base'}"></i>
            <span>${message}</span>
        </div>
        <button onclick="document.getElementById('alert-banner').classList.add('hidden')" class="text-xs opacity-80 hover:opacity-100">
            <i class="fa-solid fa-xmark text-sm"></i>
        </button>
    `;
    banner.classList.remove('hidden');

    setTimeout(() => {
        banner.classList.add('hidden');
    }, 8000);
}

// Chart Instances
let ratingChartInstance = null;
let verdictChartInstance = null;
let difficultyChartInstance = null;

// 1. Dashboard Summary
async function loadSummary() {
    try {
        const res = await fetch('/api/dashboard/');
        if (!res.ok) return;
        const data = await res.json();

        // Handle
        const displayHandle = document.getElementById('display-handle');
        const handleStatus = document.getElementById('handle-status-badge');
        if (displayHandle) {
            displayHandle.textContent = data.codeforces_handle || 'Not configured';
        }
        if (handleStatus) {
            if (data.is_handle_verified) {
                handleStatus.innerHTML = '<i class="fa-solid fa-circle-check"></i><span>Verified</span>';
                handleStatus.className = 'px-2.5 py-1 rounded text-xs font-bold flex items-center space-x-1.5 bg-compass-green text-compass-brown border-2 border-compass-brown shadow-[2px_2px_0px_#392518]';
            } else if (data.codeforces_handle) {
                handleStatus.innerHTML = '<i class="fa-solid fa-clock"></i><span>Pending Sync</span>';
                handleStatus.className = 'px-2.5 py-1 rounded text-xs font-bold flex items-center space-x-1.5 bg-compass-amber text-compass-brown border-2 border-compass-brown shadow-[2px_2px_0px_#392518]';
            } else {
                handleStatus.innerHTML = '<span>Unlinked</span>';
                handleStatus.className = 'px-2.5 py-1 rounded text-xs font-bold bg-compass-navyDeep text-compass-offWhite/60 border border-compass-offWhite/30';
            }
        }

        // Current Rating & Rank
        const currentRatingEl = document.getElementById('current-rating');
        const rankBadge = document.getElementById('rank-badge');
        if (currentRatingEl) {
            currentRatingEl.textContent = data.current_rating ?? '-';
            if (data.rank_color) currentRatingEl.style.color = data.rank_color;
        }
        if (rankBadge) {
            rankBadge.textContent = data.rank_title || 'Unrated';
            if (data.rank_color) {
                rankBadge.style.backgroundColor = data.rank_color;
                rankBadge.style.color = '#ffffff';
                rankBadge.style.borderColor = '#0e2433';
            }
        }

        // Delta
        const deltaContainer = document.getElementById('rating-delta-container');
        if (deltaContainer) {
            const delta = data.rating_delta;
            if (delta > 0) {
                deltaContainer.innerHTML = `<span class="px-2 py-0.5 rounded bg-compass-green text-compass-brown font-extrabold border border-compass-brown shadow-[1px_1px_0px_#392518]"><i class="fa-solid fa-arrow-trend-up"></i> +${delta}</span> <span class="text-compass-offWhite/80 ml-1">last round</span>`;
            } else if (delta < 0) {
                deltaContainer.innerHTML = `<span class="px-2 py-0.5 rounded bg-compass-error text-white font-extrabold border border-compass-brown shadow-[1px_1px_0px_#392518]"><i class="fa-solid fa-arrow-trend-down"></i> ${delta}</span> <span class="text-compass-offWhite/80 ml-1">last round</span>`;
            } else {
                deltaContainer.innerHTML = `<span class="text-compass-offWhite/60">No recent delta</span>`;
            }
        }

        // Max Rating
        const maxRatingEl = document.getElementById('max-rating');
        const maxRankBadge = document.getElementById('max-rank-badge');
        if (maxRatingEl) {
            maxRatingEl.textContent = data.max_rating ?? '-';
            if (data.max_rank_color) maxRatingEl.style.color = data.max_rank_color;
        }
        if (maxRankBadge) {
            maxRankBadge.textContent = `Peak Rank: ${data.max_rank_title || '-'}`;
        }

        // Solved & Rate
        const psEl = document.getElementById('problems-solved');
        if (psEl) psEl.textContent = data.problems_solved ?? '0';

        const srEl = document.getElementById('solve-rate');
        if (srEl) srEl.textContent = `${data.solve_rate ?? 0}% solve rate`;

        const tsEl = document.getElementById('total-submissions');
        if (tsEl) tsEl.textContent = data.total_submissions ?? '0';

        // Contests
        const ccEl = document.getElementById('contests-count');
        if (ccEl) ccEl.textContent = data.contests_count ?? '0';

        if (data.last_contest_date) {
            const d = new Date(data.last_contest_date);
            const lcEl = document.getElementById('last-contest-text');
            if (lcEl) lcEl.innerHTML = `<i class="fa-solid fa-calendar-days text-compass-amber"></i> Last contest: <strong>${d.toLocaleDateString()}</strong>`;
        }
    } catch (err) {
        console.error('Failed to load dashboard summary:', err);
    }
}

// 2. Rating Progression Line Chart (Vibrant Sky Blue & Gradient)
async function loadRatingChart() {
    try {
        const res = await fetch('/api/contests/?ordering=rating_update_time');
        if (!res.ok) return;
        const contests = await res.json();

        const canvas = document.getElementById('ratingChart');
        if (!canvas) return;

        if (ratingChartInstance) {
            ratingChartInstance.destroy();
        }

        if (contests.length === 0) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.font = 'bold 13px "Work Sans", sans-serif';
            ctx.fillStyle = '#efbf80';
            ctx.textAlign = 'center';
            ctx.fillText('No contest history available. Click "Sync Now" to load your Codeforces rating history.', canvas.width / 2, canvas.height / 2);
            return;
        }

        const labels = contests.map(c => {
            const dt = new Date(c.rating_update_time);
            return `${dt.getMonth() + 1}/${dt.getFullYear().toString().slice(-2)}`;
        });
        const ratings = contests.map(c => c.new_rating);

        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height || 260);
        gradient.addColorStop(0, 'rgba(123, 212, 255, 0.35)');
        gradient.addColorStop(0.7, 'rgba(239, 191, 128, 0.1)');
        gradient.addColorStop(1, 'rgba(23, 65, 92, 0.0)');

        ratingChartInstance = new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Rating',
                    data: ratings,
                    borderColor: '#7bd4ff',
                    backgroundColor: gradient,
                    borderWidth: 3,
                    fill: true,
                    tension: 0.25,
                    pointBackgroundColor: '#f8d7b0',
                    pointBorderColor: '#392518',
                    pointBorderWidth: 2,
                    pointRadius: contests.length > 30 ? 2.5 : 4.5,
                    pointHoverRadius: 7,
                    pointHoverBackgroundColor: '#7bd4ff',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#17415c',
                        titleColor: '#f8d7b0',
                        bodyColor: '#f3f2f2',
                        borderColor: '#efbf80',
                        borderWidth: 1.5,
                        padding: 10,
                        callbacks: {
                            title: (items) => contests[items[0].dataIndex]?.contest_name || '',
                            label: (item) => {
                                const c = contests[item.dataIndex];
                                const sign = c.delta >= 0 ? '+' : '';
                                return `Rating: ${c.new_rating} (${sign}${c.delta}) | Rank: #${c.rank}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(242, 240, 236, 0.06)' },
                        ticks: { color: '#efbf80', font: { family: '"Work Sans", sans-serif', weight: 'bold', size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(242, 240, 236, 0.06)' },
                        ticks: { color: '#efbf80', font: { family: '"Work Sans", sans-serif', weight: 'bold', size: 10 } }
                    }
                }
            }
        });
    } catch (err) {
        console.error('Failed to load rating chart:', err);
    }
}

// 3. Verdict Doughnut Chart (Coders' Compass Vivid Palette)
async function loadVerdictChart() {
    try {
        const res = await fetch('/api/analytics/verdicts/');
        if (!res.ok) return;
        const data = await res.json();

        const canvas = document.getElementById('verdictChart');
        if (!canvas) return;

        if (verdictChartInstance) {
            verdictChartInstance.destroy();
        }

        const breakdown = data.breakdown || [];
        if (breakdown.length === 0) return;

        const colorMap = {
            'OK': '#90ee90',                  // Mint Green
            'WRONG_ANSWER': '#ff6b6b',        // Coral Red
            'TIME_LIMIT_EXCEEDED': '#efbf80', // Warm Amber
            'RUNTIME_ERROR': '#ff90e8',       // Electric Pink
            'COMPILATION_ERROR': '#c9a0ec',   // Lavender Violet
            'OTHER': '#7bd4ff',               // Sky Blue
        };

        const labels = breakdown.map(b => b.label);
        const counts = breakdown.map(b => b.count);
        const colors = breakdown.map(b => colorMap[b.key] || '#f8d7b0');

        verdictChartInstance = new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: colors,
                    borderColor: '#17415c',
                    borderWidth: 3,
                    hoverOffset: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '65%'
            }
        });

        const legendContainer = document.getElementById('verdict-legend');
        if (legendContainer) {
            legendContainer.innerHTML = breakdown.map(b => {
                const c = colorMap[b.key] || '#f8d7b0';
                return `
                    <span class="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded text-[11px] font-bold border-2 border-compass-brown shadow-[1px_1px_0px_#0e2433]" style="background-color: ${c}; color: #392518;">
                        <span>${b.label}: ${b.count} (${b.percentage}%)</span>
                    </span>
                `;
            }).join('');
        }
    } catch (err) {
        console.error('Failed to load verdict chart:', err);
    }
}

// 4. Difficulty Rating Bar Chart (Multi-color Tiers)
async function loadDifficultyChart() {
    try {
        const res = await fetch('/api/analytics/ratings/');
        if (!res.ok) return;
        const brackets = await res.json();

        const canvas = document.getElementById('difficultyChart');
        if (!canvas) return;

        if (difficultyChartInstance) {
            difficultyChartInstance.destroy();
        }

        const labels = brackets.map(b => b.range);
        const counts = brackets.map(b => b.count);

        // Rotating rainbow bar colors from Coders' Compass
        const barColors = ['#90ee90', '#7bd4ff', '#efbf80', '#ff90e8', '#c9a0ec', '#f8d7b0'];
        const assignedColors = brackets.map((_, i) => barColors[i % barColors.length]);

        difficultyChartInstance = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Problems Solved',
                    data: counts,
                    backgroundColor: assignedColors,
                    borderColor: '#392518',
                    borderWidth: 2,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#17415c',
                        titleColor: '#f8d7b0',
                        bodyColor: '#f3f2f2',
                        borderColor: '#efbf80',
                        borderWidth: 1.5
                    }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#efbf80', font: { family: '"Work Sans", sans-serif', weight: 'bold', size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(242, 240, 236, 0.06)' },
                        ticks: { color: '#efbf80', font: { family: '"Work Sans", sans-serif', weight: 'bold', size: 10 }, stepSize: 1 }
                    }
                }
            }
        });
    } catch (err) {
        console.error('Failed to load difficulty chart:', err);
    }
}

// 5. Topic-Wise Weak Areas Table with Rotating Rainbow Badges
async function loadTopics() {
    try {
        const res = await fetch('/api/analytics/topics/');
        if (!res.ok) return;
        const topics = await res.json();

        const tbody = document.getElementById('topics-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        if (topics.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="py-6 text-center text-compass-offWhite/60 font-semibold">No topic data available yet. Click "Sync Now" above.</td></tr>`;
            return;
        }

        const tagColorClasses = [
            'bg-compass-sky text-compass-brown border-compass-brown',
            'bg-compass-green text-compass-brown border-compass-brown',
            'bg-compass-amber text-compass-brown border-compass-brown',
            'bg-compass-pink text-compass-brown border-compass-brown',
            'bg-compass-violet text-compass-purpleDeep border-compass-purpleDeep',
            'bg-compass-peach text-compass-brown border-compass-brown'
        ];

        topics.slice(0, 15).forEach((t, i) => {
            const pct = Math.round(t.solve_rate * 100);
            let barColor = 'bg-compass-error';
            let pctColor = 'text-compass-error';
            if (pct >= 70) {
                barColor = 'bg-compass-green';
                pctColor = 'text-compass-green';
            } else if (pct >= 40) {
                barColor = 'bg-compass-amber';
                pctColor = 'text-compass-amber';
            }

            const tagClass = tagColorClasses[i % tagColorClasses.length];

            const row = document.createElement('tr');
            row.className = 'hover:bg-compass-navyDeep/60 transition';
            row.innerHTML = `
                <td class="py-2.5 px-3 font-medium">
                    <span class="inline-block px-2.5 py-0.5 rounded text-[11px] font-extrabold uppercase border-2 shadow-[1px_1px_0px_#0e2433] ${tagClass}">
                        ${t.tag}
                    </span>
                </td>
                <td class="py-2.5 px-3 text-center text-compass-offWhite font-bold">${t.attempted}</td>
                <td class="py-2.5 px-3 text-center text-compass-green font-bold">${t.solved}</td>
                <td class="py-2.5 px-3 text-right">
                    <div class="flex items-center justify-end space-x-2">
                        <div class="bg-compass-navyDarker rounded-full h-2 w-16 overflow-hidden border border-compass-brown/30">
                            <div class="${barColor} h-2 rounded-full" style="width: ${pct}%"></div>
                        </div>
                        <span class="font-extrabold text-xs w-10 text-right ${pctColor}">${pct}%</span>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error('Failed to load topics:', err);
    }
}

// 6. Recent Submissions Table with Vivid Neo-Brutalist Verdict Badges
async function loadRecentSubmissions(verdict = '') {
    try {
        let url = '/api/submissions/recent/?limit=15';
        if (verdict) {
            url += `&verdict=${encodeURIComponent(verdict)}`;
        }
        const res = await fetch(url);
        if (!res.ok) return;
        const submissions = await res.json();

        const tbody = document.getElementById('submissions-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        if (submissions.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="py-6 text-center text-compass-offWhite/60 font-semibold">No submissions matching criteria.</td></tr>`;
            return;
        }

        const verdictStyles = {
            'OK': 'bg-compass-green text-compass-brown border-compass-brown',
            'WRONG_ANSWER': 'bg-compass-error text-white border-compass-brown',
            'TIME_LIMIT_EXCEEDED': 'bg-compass-amber text-compass-brown border-compass-brown',
            'RUNTIME_ERROR': 'bg-compass-pink text-compass-brown border-compass-brown',
            'COMPILATION_ERROR': 'bg-compass-violet text-compass-purpleDeep border-compass-purpleDeep',
        };

        submissions.forEach(s => {
            const badgeClass = verdictStyles[s.verdict] || 'bg-compass-navyDeep text-compass-offWhite border-compass-brown';
            const problemLink = s.contest_id 
                ? `https://codeforces.com/contest/${s.contest_id}/problem/${s.problem_index}`
                : `https://codeforces.com/problemset`;

            const row = document.createElement('tr');
            row.className = 'hover:bg-compass-navyDeep/60 transition';
            row.innerHTML = `
                <td class="py-2.5 px-3">
                    <a href="${problemLink}" target="_blank" rel="noopener noreferrer"
                        class="text-compass-sky hover:text-compass-peach font-bold hover:underline flex items-center space-x-1.5">
                        <span>${s.contest_id || ''}${s.problem_index} - ${s.problem_name || 'Problem'}</span>
                        <i class="fa-solid fa-arrow-up-right-from-square text-[9px] opacity-70"></i>
                    </a>
                </td>
                <td class="py-2.5 px-3 text-center">
                    ${s.problem_rating ? `<span class="px-2 py-0.5 rounded text-[11px] font-extrabold bg-compass-amber text-compass-brown border border-compass-brown shadow-[1px_1px_0px_#0e2433]">${s.problem_rating}</span>` : '<span class="text-compass-offWhite/40">-</span>'}
                </td>
                <td class="py-2.5 px-3 text-center">
                    <span class="inline-block px-2.5 py-0.5 rounded text-[10px] font-extrabold border-2 shadow-[2px_2px_0px_#0e2433] ${badgeClass}">
                        ${s.verdict}
                    </span>
                </td>
                <td class="py-2.5 px-3 text-right text-compass-offWhite/70 text-[11px] font-mono">
                    ${s.language || '-'}
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error('Failed to load recent submissions:', err);
    }
}

// Refresh all sections
async function refreshAllData() {
    await Promise.all([
        loadSummary(),
        loadRatingChart(),
        loadVerdictChart(),
        loadDifficultyChart(),
        loadTopics(),
        loadRecentSubmissions(document.getElementById('submission-verdict-filter')?.value || '')
    ]);
}

// 7. Sync Handler
async function handleSync() {
    const btn = document.getElementById('btn-sync');
    const icon = document.getElementById('sync-icon');
    const text = document.getElementById('sync-text');

    btn.disabled = true;
    icon.classList.add('fa-spin');
    text.textContent = 'Syncing...';

    try {
        const handle = document.getElementById('handle-input')?.value.trim();
        const res = await fetch('/api/codeforces/sync/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ handle })
        });

        const rawText = await res.text();
        let data = {};
        try {
            data = JSON.parse(rawText);
        } catch (e) {
            data = { error: `Server response (${res.status}): ${res.statusText || 'Sync error'}` };
        }
        if (res.ok) {
            showAlert(`Codeforces synced! Created/Updated: ${data.contests_created + data.contests_updated} contests, ${data.problems_created + data.problems_updated} problems, ${data.submissions_created} submissions.`, 'success');
            await refreshAllData();
        } else {
            showAlert(data.error || 'Sync failed. Please check handle.', 'error');
        }
    } catch (err) {
        showAlert(`Error during sync: ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
        icon.classList.remove('fa-spin');
        text.textContent = 'Sync Now';
    }
}

// 8. Update Handle Handler
async function handleUpdateHandle() {
    const handleInput = document.getElementById('handle-input');
    const handle = handleInput?.value.trim();
    if (!handle) {
        showAlert('Please enter a valid Codeforces handle.', 'error');
        return;
    }

    const btn = document.getElementById('btn-update-handle');
    btn.disabled = true;
    btn.textContent = 'Saving...';

    try {
        const res = await fetch('/api/codeforces/handle/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ handle: handle, sync: true })
        });

        const rawText = await res.text();
        let data = {};
        try {
            data = JSON.parse(rawText);
        } catch (e) {
            data = { error: `Server error (${res.status}): Please check handle format.` };
        }

        if (res.ok) {
            showAlert(`Handle updated to "${handle}" and synced!`, 'success');
            await refreshAllData();
        } else {
            showAlert(data.error || data.message || `Failed to update handle (Status ${res.status}).`, 'error');
        }
    } catch (err) {
        showAlert(`Error updating handle: ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Save';
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    refreshAllData();

    document.getElementById('btn-sync')?.addEventListener('click', handleSync);
    document.getElementById('btn-update-handle')?.addEventListener('click', handleUpdateHandle);
    document.getElementById('submission-verdict-filter')?.addEventListener('change', (e) => {
        loadRecentSubmissions(e.target.value);
    });
});
