async function send() {
  const pm25 = document.getElementById("pm25").value;
  const pm10 = document.getElementById("pm10").value;
  const no2 = document.getElementById("no2").value;
  const so2 = document.getElementById("so2").value;
  const co = document.getElementById("co").value;
  const temp = document.getElementById("temp").value;
  const hum = document.getElementById("hum").value;

  const payload = {
    PM2_5: pm25,
    PM10: pm10,
    NO2: no2,
    SO2: so2,
    CO: co,
    Temperature: temp,
    Humidity: hum
  };

  const out = document.getElementById("out");
  out.style.display = "block";
  out.innerHTML = "Predicting...";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json();
      out.innerHTML = "<b>Error:</b> " + (err.error || res.statusText);
      return;
    }
    const data = await res.json();
    const label = data.prediction;
    const suggestion = data.suggestion;
    let color = "#d0f0c0"; // good
    if (label === "Moderate") color = "#fff1b8";
    if (label === "Unhealthy") color = "#ffd6d6";

    out.style.background = color;
    out.innerHTML = `<div><span class="badge">${label}</span></div>
                     <div style="margin-top:8px;"><b>Suggestion:</b> ${suggestion}</div>
                     <div style="margin-top:8px;"><b>Inputs:</b> PM2.5=${data.inputs.PM2_5}, PM10=${data.inputs.PM10}, NO2=${data.inputs.NO2}, SO2=${data.inputs.SO2}, CO=${data.inputs.CO}</div>`;
  } catch (e) {
    out.innerHTML = "Error: " + e.message;
  }
}
