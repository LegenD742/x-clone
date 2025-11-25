// ------------------------------
// GLOBAL LOADER
// ------------------------------
const loader = document.getElementById("loader");

function showLoader(text = "Processing...") {
    loader.querySelector("p").textContent = text;
    loader.classList.add("show");
}
function hideLoader() {
    loader.classList.remove("show");
}


// ------------------------------
// UPDATE PROGRESS BARS
// ------------------------------
function updateBars(t1, t2, t3base) {

    // Type 1
    document.getElementById("barT1").style.width = t1 + "%";
    document.getElementById("percentT1").textContent = t1 + "%";

    // Type 2
    document.getElementById("barT2").style.width = t2 + "%";
    document.getElementById("percentT2").textContent = t2 + "%";

    // Type 3 Base
    document.getElementById("barT3").style.width = t3base + "%";
    document.getElementById("percentT3").textContent = t3base + "%";
}


// ------------------------------
// COMPARE BUTTON
// ------------------------------
document.getElementById("runCompare").onclick = async () => {
    const codeA = document.getElementById("codeA").value;
    const codeB = document.getElementById("codeB").value;
    const mode = document.getElementById("cloneTypeSelect").value;

    if (!codeA.trim() || !codeB.trim()) {
        alert("Please enter both code snippets");
        return;
    }

    showLoader("Comparing code...");

    try {
        const res = await fetch("/api/compare", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codeA, codeB, mode })
        });

        const data = await res.json();
        hideLoader();

        if (data.error) {
            alert(data.error);
            return;
        }

        updateUI(data, mode);

    } catch (err) {
        console.error("Compare API Error:", err);
        hideLoader();
        alert("Error comparing code!");
    }
};


// ------------------------------
// UPDATE UI BASED ON ANALYSIS TYPE
// ------------------------------
function updateUI(data, mode) {

    const rowT1 = document.getElementById("rowT1");
    const rowT2 = document.getElementById("rowT2");
    const rowT3 = document.getElementById("rowT3");

    // Hide all first
    rowT1.style.display = "none";
    rowT2.style.display = "none";
    rowT3.style.display = "none";

    // Mode = Type 1 only
    if (mode === "t1") {
        rowT1.style.display = "flex";
        updateBars(data.t1, 0, 0);
    }

    // Mode = Type 2 only
    else if (mode === "t2") {
        rowT2.style.display = "flex";
        updateBars(0, data.t2, 0);
    }

    // Mode = Type 3 only
    else if (mode === "t3") {
        rowT3.style.display = "flex";
        updateBars(0, 0, data.t3base);
    }

    // Mode = ALL
    else {
        rowT1.style.display = "flex";
        rowT2.style.display = "flex";
        rowT3.style.display = "flex";
        updateBars(data.t1, data.t2, data.t3base);
    }
}


// ------------------------------
// GITHUB SEARCH
// ------------------------------
document.getElementById("runGithubSearch").onclick = async () => {
    const code = document.getElementById("githubCode").value;

    if (!code.trim()) {
        alert("Please paste code first!");
        return;
    }

    const statusBox = document.getElementById("githubStatus");
    statusBox.textContent = "Searching DuckDuckGo…";

    try {
        const res = await fetch("/api/github/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code })
        });

        const data = await res.json();

        if (data.error) {
            statusBox.textContent = "Error: " + data.error;
            return;
        }

        let out = "Keywords: " + data.keywords.join(", ") + "\n\n";

        if (data.results.length === 0) {
            out += "No GitHub matches found.";
        } else {
            out += "Matches:\n";
            data.results.forEach(r => {
                out += `🔗 ${r.url} (T3: ${r.t3}%)\n`;
            });
        }

        statusBox.textContent = out;

    } catch (err) {
        statusBox.textContent = "Search failed!";
        console.error(err);
    }
};
