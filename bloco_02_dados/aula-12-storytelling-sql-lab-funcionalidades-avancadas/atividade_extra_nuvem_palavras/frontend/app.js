// Tech Cloud Pulse - Frontend Interactive Engine

const TECH_CATEGORIES = {
    "IA & Machine Learning": "cat-ia",
    "Engenharia de Dados": "cat-data",
    "Cloud & DevOps": "cat-cloud",
    "Linguagens & Frameworks": "cat-dev",
    "Bancos de Dados & Storage": "cat-db"
};

// Base terms pool
let wordsData = [
    { palavra: "Inteligência Artificial", categoria: "IA & Machine Learning", frequencia: 115 },
    { palavra: "Apache Superset", categoria: "Engenharia de Dados", frequencia: 110 },
    { palavra: "SQL Lab", categoria: "Engenharia de Dados", frequencia: 105 },
    { palavra: "Storytelling com Dados", categoria: "Engenharia de Dados", frequencia: 100 },
    { palavra: "Python", categoria: "Linguagens & Frameworks", frequencia: 96 },
    { palavra: "PostgreSQL", categoria: "Bancos de Dados & Storage", frequencia: 94 },
    { palavra: "LLMs", categoria: "IA & Machine Learning", frequencia: 92 },
    { palavra: "Docker", categoria: "Cloud & DevOps", frequencia: 89 },
    { palavra: "Kubernetes", categoria: "Cloud & DevOps", frequencia: 85 },
    { palavra: "Row-Level Security", categoria: "Bancos de Dados & Storage", frequencia: 84 },
    { palavra: "Alerts & Reports", categoria: "Engenharia de Dados", frequencia: 82 },
    { palavra: "FastAPI", categoria: "Linguagens & Frameworks", frequencia: 78 },
    { palavra: "Machine Learning", categoria: "IA & Machine Learning", frequencia: 76 },
    { palavra: "Apache Kafka", categoria: "Engenharia de Dados", frequencia: 75 },
    { palavra: "Data Warehouse", categoria: "Engenharia de Dados", frequencia: 73 },
    { palavra: "AWS", categoria: "Cloud & DevOps", frequencia: 71 },
    { palavra: "TypeScript", categoria: "Linguagens & Frameworks", frequencia: 68 },
    { palavra: "Pandas", categoria: "IA & Machine Learning", frequencia: 65 },
    { palavra: "PyTorch", categoria: "IA & Machine Learning", frequencia: 64 },
    { palavra: "Redis", categoria: "Bancos de Dados & Storage", frequencia: 62 },
    { palavra: "Terraform", categoria: "Cloud & DevOps", frequencia: 60 },
    { palavra: "LangChain", categoria: "IA & Machine Learning", frequencia: 58 },
    { palavra: "ETL Pipeline", categoria: "Engenharia de Dados", frequencia: 56 },
    { palavra: "Linux", categoria: "Cloud & DevOps", frequencia: 54 }
];

// State
let selectedCategory = "ALL";
const TOTAL_CYCLE_SECONDS = 300; // 5 minutos
let remainingSeconds = TOTAL_CYCLE_SECONDS;
let timerInterval = null;

// DOM Elements
const canvas = document.getElementById("word-cloud-canvas");
const countdownDisplay = document.getElementById("countdown-timer");
const progressBar = document.getElementById("timer-progress-bar");
const totalWordsEl = document.getElementById("metric-total-words");
const topWordEl = document.getElementById("metric-top-word");
const topCategoryEl = document.getElementById("metric-top-category");
const topWeightEl = document.getElementById("metric-top-weight");
const lastSyncEl = document.getElementById("metric-last-sync");
const tableBody = document.getElementById("words-table-body");
const tableRowCount = document.getElementById("table-row-count");
const btnSyncNow = document.getElementById("btn-sync-now");
const btnReorder = document.getElementById("btn-reorder");

// Initialize Application
document.addEventListener("DOMContentLoaded", () => {
    initFilters();
    renderWordCloud();
    renderTable();
    updateMetrics();
    startCountdown();

    btnSyncNow.addEventListener("click", () => {
        simulateUpdateCycle();
    });

    btnReorder.addEventListener("click", () => {
        wordsData = shuffleArray([...wordsData]);
        renderWordCloud();
    });
});

// Category Filter handling
function initFilters() {
    const chips = document.querySelectorAll(".chip");
    chips.forEach(chip => {
        chip.addEventListener("click", () => {
            chips.forEach(c => c.classList.remove("active"));
            chip.classList.add("active");
            selectedCategory = chip.getAttribute("data-category");
            renderWordCloud();
        });
    });
}

// Word Cloud Render Engine
function renderWordCloud() {
    canvas.innerHTML = "";
    
    // Filter by Category
    const filtered = selectedCategory === "ALL" 
        ? wordsData 
        : wordsData.filter(item => item.categoria === selectedCategory);

    if (filtered.length === 0) {
        canvas.innerHTML = `<p style="color: var(--text-muted); font-size: 0.9rem;">Nenhum termo encontrado nesta categoria.</p>`;
        return;
    }

    // Determine min and max frequencies for scaling
    const freqs = filtered.map(w => w.frequencia);
    const maxFreq = Math.max(...freqs, 100);
    const minFreq = Math.min(...freqs, 40);

    filtered.forEach(item => {
        const tag = document.createElement("span");
        tag.className = "cloud-tag";
        tag.textContent = item.palavra;

        // Add Category Class
        const catClass = TECH_CATEGORIES[item.categoria] || "cat-data";
        tag.classList.add(catClass);

        // Calculate Proportional Font Size (from 0.85rem to 2.4rem)
        const ratio = (item.frequencia - minFreq) / (maxFreq - minFreq || 1);
        const fontSizeRem = 0.9 + (ratio * 1.5);
        tag.style.fontSize = `${fontSizeRem.toFixed(2)}rem`;

        // Tooltip title
        tag.title = `${item.palavra} (${item.categoria})\nFrequência: ${item.frequencia} pts`;

        tag.addEventListener("click", () => {
            alert(`🔍 Termo: ${item.palavra}\n📂 Categoria: ${item.categoria}\n📊 Métrica (Frequência): ${item.frequencia}\n⏰ Próxima atualização em: ${formatTime(remainingSeconds)}`);
        });

        canvas.appendChild(tag);
    });
}

// Populate Table
function renderTable() {
    tableBody.innerHTML = "";
    const sorted = [...wordsData].sort((a, b) => b.frequencia - a.frequencia);
    tableRowCount.textContent = `${sorted.length} termos carregados`;

    const now = new Date().toLocaleTimeString("pt-BR");

    sorted.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${item.palavra}</strong></td>
            <td><span class="badge">${item.categoria}</span></td>
            <td><code>${item.frequencia} pts</code></td>
            <td style="color: var(--text-muted); font-size: 0.8rem;">${now}</td>
        `;
        tableBody.appendChild(tr);
    });
}

// Update Top Metrics
function updateMetrics() {
    totalWordsEl.textContent = wordsData.length;

    const sorted = [...wordsData].sort((a, b) => b.frequencia - a.frequencia);
    if (sorted.length > 0) {
        const top = sorted[0];
        topWordEl.textContent = top.palavra;
        topCategoryEl.textContent = top.categoria;
        topWeightEl.textContent = `Peso de Relevância: ${top.frequencia} pts`;
    }
}

// 5-Minute Timer Engine
function startCountdown() {
    if (timerInterval) clearInterval(timerInterval);
    
    timerInterval = setInterval(() => {
        remainingSeconds--;
        if (remainingSeconds <= 0) {
            simulateUpdateCycle();
        }
        updateTimerDisplay();
    }, 1000);
    
    updateTimerDisplay();
}

function updateTimerDisplay() {
    countdownDisplay.textContent = formatTime(remainingSeconds);
    const progressPercent = (remainingSeconds / TOTAL_CYCLE_SECONDS) * 100;
    progressBar.style.width = `${progressPercent}%`;
}

function formatTime(totalSeconds) {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// Simulate 5-Minute Update Cycle
function simulateUpdateCycle() {
    btnSyncNow.disabled = true;
    btnSyncNow.innerHTML = `<span class="btn-icon">⏳</span> Sincronizando...`;

    // Apply new dynamic weights
    wordsData.forEach(item => {
        const variation = Math.floor(Math.random() * 21) - 10; // -10 to +10
        item.frequencia = Math.max(25, item.frequencia + variation);
    });

    // Randomize one hot trend
    const randomIndex = Math.floor(Math.random() * wordsData.length);
    wordsData[randomIndex].frequencia = Math.floor(Math.random() * 30) + 110;

    // Reset countdown
    remainingSeconds = TOTAL_CYCLE_SECONDS;
    updateTimerDisplay();

    setTimeout(() => {
        renderWordCloud();
        renderTable();
        updateMetrics();
        lastSyncEl.textContent = `Última carga: ${new Date().toLocaleTimeString("pt-BR")}`;

        btnSyncNow.disabled = false;
        btnSyncNow.innerHTML = `<span class="btn-icon">🔄</span> Sincronizar Agora`;

        // Pulse animation effect
        canvas.style.transform = "scale(0.98)";
        setTimeout(() => {
            canvas.style.transform = "scale(1)";
        }, 150);
    }, 600);
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
