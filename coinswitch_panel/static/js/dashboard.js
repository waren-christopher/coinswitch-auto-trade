document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("apiForm");
    const loading = document.getElementById("loading");
    const responseSection = document.getElementById("responseSection");
    const responseBox = document.getElementById("responseBox");
    const statusCodeBox = document.getElementById("statusCode");
    const inputFields = document.getElementById("inputFields");

    /* --- MODAL ELEMENTS --- */
    const modal = document.getElementById("customModal");
    const modalConfirmBtn = document.getElementById("modalConfirm");
    const modalCancelBtn = document.getElementById("modalCancel");
    let pendingApiString = null; // Stores the API call while waiting for "Yes"

    /* ================================
       TRANSACTION DEFAULTS
    ================================= */
    const transactionDefaults = {
        crypto_withdrawal: { amount: "", assetName: "USDT", chain: "BSC", address: "ledger address", subaddress: "" },
        transfer_broker_to_master: { amount: "", assetName: "USDT", fromID: "brokerid", toID: 'masterid' },
        transfer_master_to_broker: { amount: "", assetName: "INR", fromID: "masterid", toID: 'brokerid' },
        create_market_order: { quantity: "", bestQuantity: "", type: "market", side: "BUY", instrument: "USDT/INR", quantityType: "QUOTE", bestQuantityType: "QUOTE", username: "warenx1" },
        create_limit_order: { limitPrice: "", quantity: "", type: "limit", side: "BUY", instrument: "USDT/INR", quantityType: "QUOTE", username: "warenx1" },
        cancel_order: { orderId: "" }
    };

    const optionalFields = ["subaddress"];

    /* ================================
       JSON SYNTAX HIGHLIGHTER
    ================================= */
    function syntaxHighlight(json) {
        json = json.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(\.\d+)?)/g, match => {
            let cls = "json-number";
            if (/^"/.test(match)) cls = /:$/.test(match) ? "json-key" : "json-string";
            else if (/true|false/.test(match)) cls = "json-boolean";
            else if (/null/.test(match)) cls = "json-null";
            return `<span class="${cls}">${match}</span>`;
        });
    }

    /* ================================
       DISPLAY RESPONSE (With Corrected Regex)
    ================================= */
    function displayFormattedResponse(rawData, httpStatus) {
        loading.style.display = "none";
        responseSection.style.display = "block";

        let finalStatus = httpStatus;
        let jsonObject = rawData;

        // 1. Parse JSON to find internal status
        try {
            if (typeof rawData === "string") {
                jsonObject = JSON.parse(rawData);
            }
            if (jsonObject && jsonObject.status !== undefined) {
                finalStatus = parseInt(jsonObject.status);
            }
        } catch (e) {
            console.log("Response was not JSON", e);
        }

        // 2. Status Badge
        const isSuccess = finalStatus === 200;
        statusCodeBox.textContent = finalStatus + (isSuccess ? " OK" : "");
        statusCodeBox.style.color = isSuccess ? "#22c55e" : "#ef4444";
        statusCodeBox.style.borderColor = isSuccess ? "#22c55e" : "#ef4444";

        // 3. Render Highlighting + Inject Copy Button
        try {
            const jsonString = typeof jsonObject === "object" ? JSON.stringify(jsonObject, null, 2) : jsonObject;
            let htmlContent = syntaxHighlight(jsonString);

            // --- ✅ FIXED REGEX HERE ---
            // This now correctly expects the colon (:) inside the span
            htmlContent = htmlContent.replace(
                /<span class="json-key">"orderId":<\/span>\s*<span class="json-string">"(.*?)"<\/span>/g, 
                function(match, idValue) {
                    return `${match} <button class="copy-icon-btn" onclick="window.copyText('${idValue}')" title="Copy Order ID"><i class="fas fa-copy"></i></button>`;
                }
            );

            responseBox.innerHTML = htmlContent;
        } catch {
            responseBox.textContent = rawData;
        }
    }

    /* ================================
       API CALL
    ================================= */
    async function performApiCall(formData) {
        loading.style.display = "block";
        responseSection.style.display = "none";

        const response = await fetch("", {
            method: "POST",
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                "X-Requested-With": "XMLHttpRequest"
            },
            body: formData
        });

        const data = await response.text();
        displayFormattedResponse(data, response.status);
    }

    function validateRequiredFields(formData) {
        for (let [key, value] of formData.entries()) {
            if (key === "api") continue;
            if (!optionalFields.includes(key) && (value === null || value.trim() === "")) {
                alert(`❌ Please fill the required field: ${key}`);
                document.querySelector(`[name="${key}"]`)?.focus();
                return false;
            }
        }
        return true;
    }

    function renderInputs(apiName, defaults) {
        inputFields.innerHTML = "";
        let apiInput = document.querySelector("input[name='api']");
        if (!apiInput) {
            apiInput = document.createElement("input");
            apiInput.type = "hidden";
            apiInput.name = "api";
            form.prepend(apiInput);
        }
        apiInput.value = apiName;

        for (const [key, value] of Object.entries(defaults)) {
            const isOptional = optionalFields.includes(key);
            const group = document.createElement("div");
            group.className = "form-group";
            const isLocked = key === "address" || key == "fromID" || key == "toID";
            group.innerHTML = `
                <span class="input-label">
                    ${key.toUpperCase()} ${isOptional ? "<span style='color:#94a3b8;font-size:0.65rem;'>(optional)</span>" : "<span style='color:#ef4444;'> *</span>"}
                </span>
                <input name="${key}" value="${value}" placeholder="${isOptional ? 'Optional' : 'Required'}" ${isLocked ? "readonly" : ""} />
            `;
            inputFields.appendChild(group);
        }
        inputFields.style.display = "grid";
        inputFields.scrollIntoView({ behavior: "smooth" });
    }

    /* ================================
       MODAL LOGIC
    ================================= */
    function closeModal() {
        modal.style.display = "none";
        pendingApiString = null;
    }

    modalCancelBtn.addEventListener("click", closeModal);

    modalConfirmBtn.addEventListener("click", () => {
        if (pendingApiString) {
            inputFields.style.display = "none";
            const fd = new FormData();
            fd.append("api", pendingApiString);
            performApiCall(fd);
        }
        closeModal();
    });

    // Close on outside click
    modal.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });

    /* ================================
       MAIN CLICK HANDLER
    ================================= */
    document.addEventListener("click", e => {
        const btn = e.target.closest("[data-api]");
        if (!btn) return;

        // 1. Highlight Button
        document.querySelectorAll(".quick-btn, .transaction-btn").forEach(b => b.classList.remove("active-btn"));
        btn.classList.add("active-btn");

        const api = btn.dataset.api;
        const baseApi = api.split("+")[0];
        const needsConfirm = btn.dataset.confirm === "true";

        // 2. Intercept "Cancel All" for Custom Modal
        if (needsConfirm) {
            pendingApiString = api; // Save API string
            modal.style.display = "flex"; // Open Modal
            return; // STOP execution here
        }

        // 3. Normal Logic
        if (btn.classList.contains("quick-btn")) {
            inputFields.style.display = "none";
            const fd = new FormData();
            fd.append("api", api);
            performApiCall(fd);
            return;
        }

        if (btn.classList.contains("transaction-btn") || baseApi === "cancel_order") {
            renderInputs(api, transactionDefaults[baseApi]);
        }
    });

    form.addEventListener("submit", e => {
        e.preventDefault();
        const formData = new FormData(form);
        if (!validateRequiredFields(formData)) return;
        performApiCall(formData);
    });

    /* ================================
       HELPER: COPY TEXT
       (Attached to window so HTML onclick can see it)
    ================================= */
    window.copyText = function(text) {
        navigator.clipboard.writeText(text).then(() => {
            console.log("Copied ID:", text);
        }).catch(err => {
            console.error("Failed to copy:", err);
        });
    };
});