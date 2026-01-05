let vecs = {};
let explored = new Set();

const targets = [
    "flag", "flags", "flagg", "fane", "banner",
    "spain", "spania", "germany", "tyskland", "france", "frankrike",
    "norway", "norge", "sweden", "sverige", "england",
    "english", "norsk", "svensk", "dansk",
    "symbol", "emblem", "nasjon", "nation", "merke",
    "country", "land", "rike", "stat", "state"
];

async function snap(vector) {
    const res = await fetch("/snap", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({vector: vector})
    });
    return res.json();
}

async function nearest(vector, topn = 100) {
    const res = await fetch("/nearest", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({vector: vector, topn: topn})
    });
    if (res.status === 403) {
        return {blocked: true};
    }
    return res.json();
}

async function combine(words) {
    const res = await fetch("/combine", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({words: words, operation: "add", topn: 100})
    });
    if (res.ok) return res.json();
    return null;
}

async function getFlag(vector) {
    const res = await fetch("/getflag", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({vector: vector})
    });
    return res.json();
}

function vecAdd(a, b) { return a.map((v, i) => v + b[i]); }
function vecSub(a, b) { return a.map((v, i) => v - b[i]); }
function vecScale(a, s) { return a.map(v => v * s); }

function collectFromNeighbors(data) {
    if (!data || !data.neighbors) return;
    for (const n of data.neighbors) {
        const w = n.word.toLowerCase();
        if (targets.includes(w) && !vecs[w]) {
            vecs[w] = n.vector;
            console.log(`✓ Found: ${n.word}`);
        }
    }
}

async function checkForFlagg(data) {
    if (!data || !data.neighbors) return false;
    for (const n of data.neighbors) {
        if (n.word.toLowerCase() === "flagg") {
            console.log("FOUND FLAGG!");
            const flag = await getFlag(n.vector);
            console.log("🚩 FLAG:", flag);
            return true;
        }
    }
    return false;
}

async function bfs(startVec, maxIter = 30) {
    let queue = [startVec];
    let visited = new Set();
    
    for (let i = 0; i < maxIter && queue.length > 0; i++) {
        const vec = queue.shift();
        const snapRes = await snap(vec);
        const word = snapRes.word.toLowerCase();
        
        if (visited.has(word)) continue;
        visited.add(word);
        
        console.log(`[${i}] Exploring: ${snapRes.word}`);
        
        const data = await nearest(vec, 100);
        
        if (data.blocked) {
            console.log("403 - Close to flag!");
            const flag = await getFlag(vec);
            console.log("🚩 FLAG:", flag);
            return true;
        }
        
        if (await checkForFlagg(data)) return true;
        collectFromNeighbors(data);
        
        // Add neighbors to queue
        for (const n of data.neighbors.slice(0, 5)) {
            queue.push(n.vector);
        }
        
        await new Promise(r => setTimeout(r, 50));
    }
    return false;
}

// Try many combine operations to find flag
async function findFlagViaCombine() {
    console.log("\nSearching for 'flag' via combine...");
    
    // Words that might combine to give us flag-related results
    const combos = [
        // Try country + symbol type words
        ["Norge", "symbol"],
        ["land", "symbol"],  
        ["nasjon", "merke"],
        ["stat", "symbol"],
        ["rike", "emblem"],
        ...visited.slice(0, 10).map(v => [v.word, "symbol"]),
        ...visited.slice(0, 10).map(v => [v.word, "nasjon"]),
    ];
    
    for (const combo of combos) {
        try {
            const data = await combine(combo);
            if (data && data.neighbors) {
                console.log(`${combo.join(" + ")}: ${data.neighbors.slice(0,5).map(n=>n.word).join(", ")}`);
                
                if (await checkForFlagg(data)) return true;
                collectFromNeighbors(data);
                
                // Also search from the combined vector
                if (data.combined_vector) {
                    const nearby = await nearest(data.combined_vector, 100);
                    if (await checkForFlagg(nearby)) return true;
                    collectFromNeighbors(nearby);
                }
            }
        } catch(e) {}
        await new Promise(r => setTimeout(r, 50));
    }
    return false;
}

async function trySolve() {
    console.log("\nAttempting solve with:", Object.keys(vecs));
    
    // Language pairs (Norwegian -> English)
    const pairs = [
        ["spania", "spain"],
        ["tyskland", "germany"],
        ["frankrike", "france"],
        ["norge", "norway"],
        ["sverige", "sweden"],
        ["norsk", "english"],
        ["dansk", "danish"],
        ["svensk", "swedish"]
    ];
    
    if (vecs.flag) {
        console.log("Have 'flag' vector, trying language shift...");
        for (const [no, en] of pairs) {
            if (vecs[no] && vecs[en]) {
                for (const scale of [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]) {
                    const shift = vecSub(vecs[no], vecs[en]);
                    const v = vecAdd(vecs.flag, vecScale(shift, scale));
                    
                    const data = await nearest(v, 50);
                    if (data.blocked) {
                        console.log(`flag + (${no}-${en})*${scale} triggered 403!`);
                        const flag = await getFlag(v);
                        console.log("🚩 FLAG:", flag);
                        return true;
                    }
                    if (await checkForFlagg(data)) return true;
                    
                    console.log(`flag + (${no}-${en})*${scale}: ${data.neighbors.slice(0,3).map(n=>n.word).join(", ")}`);
                }
            }
        }
    }
        
    console.log("\nSearching semantically near Norwegian words...");
    for (const noWord of ["norge", "nasjon", "symbol", "land", "merke"]) {
        if (vecs[noWord]) {
            console.log(`Searching near ${noWord}...`);
            const data = await nearest(vecs[noWord], 100);
            if (await checkForFlagg(data)) return true;
            collectFromNeighbors(data);
        }
    }
    
    return false;
}

async function main() {
    console.log("Starting comprehensive search...\n");
    
    // Step 1: BFS from current position
    console.log("----------- Step 1: BFS from current position");
    await bfs(current_vector, 20);
    
    // Step 2: Try combines
    console.log("\n----------- Step 2: Combine operations");
    if (await findFlagViaCombine()) return;
    
    // Step 3: Try solving with what we have
    console.log("\n----------- Step 3: Attempt solve");
    if (await trySolve()) return;
    
    // Step 4: Search from each found vector
    console.log("\n----------- Step 4: Deep search from found vectors");
    for (const [word, vec] of Object.entries(vecs)) {
        console.log(`\nSearching from ${word}...`);
        if (await bfs(vec, 10)) return;
    }

    console.log("\n----------- Could not find flag");
    console.log("\nCollected vectors:", Object.keys(vecs));
}

main();