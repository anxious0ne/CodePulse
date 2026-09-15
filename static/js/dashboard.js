async function loadDashboard() {
    const res = await fetch('/api/dashboard/');
    const data = await res.json();

    document.getElementById('current-rating').textContent = data.current_rating ?? '—';
    document.getElementById('max-rating').textContent = data.max_rating ?? '—';
    document.getElementById('problems-solved').textContent = data.problems_solved ?? '—';
}

async function loadRatingChart() {
    const res = await fetch('/api/contests/');
    const contests = await res.json();

    const labels = contests.map(c => c.contest_name);
    const ratings = contests.map(c => c.new_rating);

    new Chart(document.getElementById('ratingChart'), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Rating',
                data: ratings,
                borderColor: '#3b82f6',
                tension: 0.2
            }]
        }
    });
}

async function loadTopics() {
    const res = await fetch('/api/analytics/topics/');
    const topics = await res.json();

    const tbody = document.getElementById('topics-body');
    topics.forEach(t => {
        const row = document.createElement('tr');
        row.className = 'border-b';
        row.innerHTML = `
            <td class="py-2">${t.tag}</td>
            <td class="py-2">${t.attempted}</td>
            <td class="py-2">${t.solved}</td>
            <td class="py-2">${(t.solve_rate * 100).toFixed(0)}%</td>
        `;
        tbody.appendChild(row);
    });
}

loadDashboard();
loadRatingChart();
loadTopics();