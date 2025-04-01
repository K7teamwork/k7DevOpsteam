let participants = [];
let voteChart;

function addParticipant() {
    const nameInput = document.getElementById('participant-name');
    const name = nameInput.value.trim();

    if (name) {
        participants.push({ name, votes: 0 });
        nameInput.value = '';
        updateVoteSection();
        toggleVotingSection();
        updateChart();
    }
}

function incrementVote(index) {
    participants[index].votes++;
    updateVoteSection();
    updateChart();
}

function decrementVote(index) {
    if (participants[index].votes > 0) {
        participants[index].votes--;
        updateVoteSection();
        updateChart();
    }
}

function updateVoteSection() {
    const voteSection = document.getElementById('vote-section');
    voteSection.innerHTML = '';

    participants.forEach((participant, index) => {
        const participantDiv = document.createElement('div');
        participantDiv.className = 'participant';
        participantDiv.innerHTML = `
            <span>${participant.name} (${participant.votes})</span>
            <div>
                <button class="btn" onclick="incrementVote(${index})">Add Vote</button>
                <button class="btn" onclick="decrementVote(${index})">Remove Vote</button>
            </div>
        `;
        voteSection.appendChild(participantDiv);
    });
}

function updateChart() {
    const ctx = document.getElementById('vote-chart').getContext('2d');

    const labels = participants.map(p => p.name);
    const data = participants.map(p => p.votes);

    if (voteChart) {
        voteChart.destroy();
    }

    voteChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Votes',
                data: data,
                backgroundColor: '#68d391',
                borderColor: '#2f855a',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function toggleVotingSection() {
    const votingSection = document.getElementById('voting-section');
    if (participants.length > 0) {
        votingSection.style.display = 'block';
    }
}