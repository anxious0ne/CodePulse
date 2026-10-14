// CodePulse Dashboard Client Scripts

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
    banner.className = `p-4 rounded-xl text-sm flex items-center justify-between border ${
        isSuccess ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
    }`;
    banner.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fa-solid ${isSuccess ? 'fa-circle-check text-emerald-400' : 'fa-circle-exclamation text-rose-400'} text-base"></i>
            <span>${message}</span>
        </div>
        <button onclick="document.getElementById('alert-banner').classList.add('hidden')" class="text-xs opacity-70 hover:opacity-100">
            <i class="fa-solid fa-xmark"></i>
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
                handleStatus.innerHTML = '<i class="fa-solid fa-circle-check text-emerald-400"></i><span class="text-emerald-400">Verified</span>';
            } else if (data.codeforces_handle) {
                handleStatus.innerHTML = '<i class="fa-solid fa-clock text-amber-400"></i><span class="text-amber-400">Pending Sync</span>';
            } else {
                handleStatus.innerHTML = '<span class="text-slate-500">Unlinked</span>';
            }
        }

        // Current Rating & Rank
        const currentRatingEl = document.getElementById('current-rating');
        const rankBadge = document.getElementById('rank-badge');
        if (currentRatingEl) {
            currentRatingEl.textContent = data.current_rating ?? '—';
            if (data.rank_color) currentRatingEl.style.color = data.rank_color;
        }
        if (rankBadge) {
            rankBadge.textContent = data.rank_title || 'Unrated';
            if (data.rank_color) {
                rankBadge.style.borderColor = data.rank_color;
                rankBadge.style.color = data.rank_color;
            }
        }

        // Delta
        const deltaContainer = document.getElementById('rating-delta-container');
        if (deltaContainer) {
            const delta = data.rating_delta;
            if (delta > 0) {
                deltaContainer.innerHTML = `<span class="text-emerald-400 font-semibold"><i class="fa-solid fa-arrow-trend-up"></i> +${delta}</span> <span class="text-slate-500">from previous round</span>`;
            } else if (delta < 0) {
                deltaContainer.innerHTML = `<span class="text-rose-400 font-semibold"><i class="fa-solid fa-arrow-trend-down"></i> ${delta}</span> <span class="text-slate-500">from previous round</span>`;
            } else {
                deltaContainer.innerHTML = `<span class="text-slate-400">No change</span>`;
            }
        }

        // Max Rating
        const maxRatingEl = document.getElementById('max-rating');
        const maxRankBadge = document.getElementById('max-rank-badge');
        if (maxRatingEl) {
            maxRatingEl.textContent = data.max_rating ?? '—';
            if (data.max_rank_color) maxRatingEl.style.color = data.max_rank_color;
        }
        if (maxRankBadge) {
            maxRankBadge.textContent = data.max_rank_title || '—';
            if (data.max_rank_color) {
                maxRankBadge.style.borderColor = data.max_rank_color;
                maxRankBadge.style.color = data.max_rank_color;
            }
        }

        // Solved & Rate
        document.getElementById('problems-solved').textContent = data.problems_solved ?? '0';
        document.getElementById('solve-rate').textContent = `${data.solve_rate ?? 0}% rate`;
        document.getElementById('total-submissions').textContent = data.total_submissions ?? '0';

        // Contests
        document.getElementById('contests-count').textContent = data.contests_count ?? '0';
        if (data.last_contest_date) {
            const d = new Date(data.last_contest_date);
            document.getElementById('last-contest-text').textContent = `Last contest: ${d.toLocaleDateString()}`;
        }
    } catch (err) {
        console.error('Failed to load dashboard summary:', err);
    }
}

// 2. Rating Progression Line Chart
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
            ctx.font = '14px Inter';
            ctx.fillStyle = '#64748b';
            ctx.textAlign = 'center';
            ctx.fillText('No contest history available. Click "Sync Now" above to load data.', canvas.width / 2, 100);
            return;
        }

        const labels = contests.map(c => {
            const dt = new Date(c.rating_update_time);
            return `${dt.getMonth() + 1}/${dt.getFullYear().toString().slice(-2)}`;
        });
        const ratings = contests.map(c => c.new_rating);

        ratingChartInstance = new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Rating',
                    data: ratings,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    borderWidth: 2.5,
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#818cf8',
                    pointRadius: contests.length > 30 ? 2 : 4,
                    pointHoverRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
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
                        grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        ticks: { color: '#94a3b8', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        ticks: { color: '#94a3b8', font: { size: 10 } }
                    }
                }
            }
        });
    } catch (err) {
        console.error('Failed to load rating chart:', err);
    }
}

// 3. Verdict Doughnut Chart
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
        if (breakdown.length === 0) {
            return;
        }

        const colorMap = {
            'OK': '#10b981',                  // Green
            'WRONG_ANSWER': '#f43f5e',        // Red
            'TIME_LIMIT_EXCEEDED': '#f59e0b', // Amber
            'RUNTIME_ERROR': '#8b5cf6',       // Purple
            'COMPILATION_ERROR': '#64748b',   // Slate
            'OTHER': '#38bdf8',               // Sky
        };

        const labels = breakdown.map(b => b.label);
        const counts = breakdown.map(b => b.count);
        const colors = breakdown.map(b => colorMap[b.key] || '#94a3b8');

        verdictChartInstance = new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: colors,
                    borderColor: '#0f172a',
                    borderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '70%'
            }
        });

        const legendContainer = document.getElementById('verdict-legend');
        if (legendContainer) {
            legendContainer.innerHTML = breakdown.map(b => `
                <span class="inline-flex items-center space-x-1 mr-2">
                    <span class="w-2.5 h-2.5 rounded-full" style="background-color: ${colorMap[b.key] || '#94a3b8'}"></span>
                    <span>${b.label}: ${b.count} (${b.percentage}%)</span>
                </span>
            `).join('');
        }
    } catch (err) {
        console.error('Failed to load verdict chart:', err);
    }
}

// 4. Difficulty Rating Bar Chart
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

        difficultyChartInstance = new Chart(canvas, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Problems Solved',
                    data: counts,
                    backgroundColor: '#06b6d4',
                    borderRadius: 6,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#94a3b8', font: { size: 10 } }
                    },
                    y: {
                        grid: { color: 'rgba(51, 65, 85, 0.3)' },
                        ticks: { color: '#94a3b8', font: { size: 10 }, stepSize: 1 }
                    }
                }
            }
        });
    } catch (err) {
        console.error('Failed to load difficulty chart:', err);
    }
}

// 5. Topic-Wise Weak Areas Table
async function loadTopics() {
    try {
        const res = await fetch('/api/analytics/topics/');
        if (!res.ok) return;
        const topics = await res.json();

        const tbody = document.getElementById('topics-body');
        if (!tbody) return;

        tbody.innerHTML = '';
        if (topics.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="py-4 text-center text-slate-500">No topic data available yet.</td></tr>`;
            return;
        }

        topics.slice(0, 15).forEach(t => {
            const pct = Math.round(t.solve_rate * 100);
            let barColor = 'bg-rose-500';
            if (pct >= 70) barColor = 'bg-emerald-500';
            else if (pct >= 40) barColor = 'bg-amber-500';

            const row = document.createElement('tr');
            row.className = 'hover:bg-slate-800/40 transition';
            row.innerHTML = `
                <td class="py-2.5 px-3 font-medium text-slate-200">
                    <span class="px-2 py-0.5 rounded-md bg-slate-800 text-sky-400 font-mono text-[11px] border border-slate-700/60">
                        ${t.tag}
                    </span>
                </td>
                <td class="py-2.5 px-3 text-slate-300 font-semibold">${t.attempted}</td>
                <td class="py-2.5 px-3 text-slate-300 font-semibold">${t.solved}</td>
                <td class="py-2.5 px-3">
                    <div class="flex items-center space-x-2">
                        <div class="flex-1 bg-slate-800 rounded-full h-1.5 w-16 overflow-hidden">
                            <div class="${barColor} h-1.5 rounded-full" style="width: ${pct}%"></div>
                        </div>
                        <span class="font-bold text-[11px] w-9 text-right text-slate-300">${pct}%</span>
                    </div>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (err) {
        console.error('Failed to load topics:', err);
    }
}

// 6. Recent Submissions Table
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
            tbody.innerHTML = `<tr><td colspan="4" class="py-4 text-center text-slate-500">No submissions matching criteria.</td></tr>`;
            return;
        }

        const verdictStyles = {
            'OK': 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
            'WRONG_ANSWER': 'bg-rose-500/10 text-rose-400 border-rose-500/20',
            'TIME_LIMIT_EXCEEDED': 'bg-amber-500/10 text-amber-400 border-amber-500/20',
            'RUNTIME_ERROR': 'bg-purple-500/10 text-purple-400 border-purple-500/20',
            'COMPILATION_ERROR': 'bg-slate-500/10 text-slate-400 border-slate-500/20',
        };

        submissions.forEach(s => {
            const badgeClass = verdictStyles[s.verdict] || 'bg-slate-700 text-slate-300 border-slate-600';
            const problemLink = s.contest_id 
                ? `https://codeforces.com/contest/${s.contest_id}/problem/${s.problem_index}`
                : `https://codeforces.com/problemset`;

            const row = document.createElement('tr');
            row.className = 'hover:bg-slate-800/40 transition';
            row.innerHTML = `
                <td class="py-2.5 px-3">
                    <a href="${problemLink}" target="_blank" rel="noopener noreferrer"
                        class="text-indigo-400 hover:text-indigo-300 font-medium hover:underline flex items-center space-x-1">
                        <span>${s.contest_id || ''}${s.problem_index} - ${s.problem_name || 'Problem'}</span>
                        <i class="fa-solid fa-arrow-up-right-from-square text-[9px] opacity-70"></i>
                    </a>
                </td>
                <td class="py-2.5 px-3">
                    ${s.problem_rating ? `<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 border border-slate-700 text-slate-300">${s.problem_rating}</span>` : '—'}
                </td>
                <td class="py-2.5 px-3">
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-bold border ${badgeClass}">
                        ${s.verdict}
                    </span>
                </td>
                <td class="py-2.5 px-3 text-slate-400 text-[11px] font-mono">
                    ${s.language || '—'}
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

        const data = await res.json();
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

    try {
        const res = await fetch('/api/codeforces/handle/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ handle, sync: true })
        });

        const data = await res.json();
        if (res.ok) {
            showAlert(`Handle set to "${handle}" and synchronized successfully!`, 'success');
            await refreshAllData();
        } else {
            showAlert(data.error || 'Failed to update handle.', 'error');
        }
    } catch (err) {
        showAlert(`Error updating handle: ${err.message}`, 'error');
    } finally {
        btn.disabled = false;
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