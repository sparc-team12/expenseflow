async function submitClaim() {
  const body = {
    employee: document.getElementById("employee").value,
    amount: parseFloat(document.getElementById("amount").value || "0"),
    category: document.getElementById("category").value,
    description: document.getElementById("description").value,
  };

  const res = await fetch("/api/claims", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const errorList = document.getElementById("errors");
  errorList.innerHTML = "";

  if (!res.ok) {
    const data = await res.json();
    const messages = Array.isArray(data.detail) ? data.detail : [data.detail];
    messages.forEach((m) => {
      const li = document.createElement("li");
      li.textContent = m;
      errorList.appendChild(li);
    });
    return;
  }

  document.getElementById("description").value = "";
  document.getElementById("amount").value = "";
  loadClaims();
}

async function act(id, action) {
  await fetch(`/api/claims/${id}/${action}`, { method: "POST" });
  loadClaims();
}

async function loadClaims() {
  const claims = await (await fetch("/api/claims")).json();
  const rows = document.getElementById("rows");
  rows.innerHTML = "";

  claims.forEach((c) => {
    const tr = document.createElement("tr");
    const actions =
      c.status === "submitted"
        ? `<button onclick="act('${c.id}','approve')">Approve</button>
           <button onclick="act('${c.id}','reject')">Reject</button>`
        : "&mdash;";
    tr.innerHTML = `<td>${c.id}</td><td>${c.employee}</td><td>${c.amount}</td>
                    <td>${c.category}</td><td>${c.status}</td><td>${actions}</td>`;
    rows.appendChild(tr);
  });
}

loadClaims();