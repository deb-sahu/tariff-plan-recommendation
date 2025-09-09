document.getElementById("loginBtn").addEventListener("click", async () => {
  const phone = document.getElementById("phoneInput").value.trim();
  const response = await fetch("http://localhost:5001/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone })
  });

  if (response.ok) {
    const data = await response.json();

    // Welcome
    document.getElementById("welcomeMessage").innerText =
      `Hello ${phone}, here are your details:`;

    // Current plan
    document.getElementById("current-plan").innerHTML =
      `<div class="p-4 bg-indigo-100 dark:bg-indigo-900 rounded-xl text-gray-900 dark:text-gray-100">
         <p><strong>${data.current_plan.name}</strong> (₹${data.current_plan.price})</p>
       </div>`;

    // Recommended
    document.getElementById("recommended-plans").innerHTML =
      data.recommendations.map(r => `
        <div class="p-4 bg-green-100 dark:bg-green-900 rounded-xl text-gray-900 dark:text-gray-100">
          <p><strong>${r.name}</strong> (₹${r.price})</p>
          <p class="text-sm text-gray-700 dark:text-gray-300">Distance: ${r.distance.toFixed(2)}</p>
        </div>
      `).join("");

    // Fetch all plans
    fetchAllPlans();

    // Toggle sections
    document.getElementById("login-section").classList.add("hidden");
    document.getElementById("dashboard-section").classList.remove("hidden");
  } else {
    document.getElementById("error-message").classList.remove("hidden");
  }
});

// Go back
document.getElementById("backBtn").addEventListener("click", () => {
  document.getElementById("dashboard-section").classList.add("hidden");
  document.getElementById("login-section").classList.remove("hidden");
  document.getElementById("error-message").classList.add("hidden");
  document.getElementById("phoneInput").value = "";
});

// Fetch all plans function
async function fetchAllPlans() {
  try {
    const response = await fetch("http://localhost:5001/api/plans");
    const data = await response.json();
    
    document.getElementById("all-plans").innerHTML = 
      data.plans.map(p => `
        <div class="p-4 bg-blue-50 dark:bg-blue-900 rounded-xl text-gray-900 dark:text-gray-100">
          <p><strong>${p.name}</strong> (₹${p.price})</p>
          <p class="text-sm text-gray-700 dark:text-gray-300">Plan ID: ${p.plan_id}</p>
        </div>
      `).join("");
  } catch (error) {
    document.getElementById("all-plans").innerHTML = 
      `<p class="text-red-500 dark:text-red-400">Error loading plans: ${error.message}</p>`;
  }
}

// KMeans prediction tester
async function sendData() {
  try {
    const response = await fetch("http://localhost:5001/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        "Day Mins": 200, 
        "Eve Mins": 150, 
        "Night Mins": 100, 
        "Intl Mins": 20, 
        "CustServ Calls": 2 
      })
    });
    const result = await response.json();
    document.getElementById("result").innerText =
      "Top Plans: " + result.recommendations.map(r => r.name + " (₹" + r.price + ")").join(", ");
  } catch (error) {
    document.getElementById("result").innerText = "Error: " + error.message;
  }
}