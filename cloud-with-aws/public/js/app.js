async function fetchWeatherData() {
  // Dapatkan data terbaru dari Firestore
  const snapshot = await db.collection("weather_data").orderBy("ts", "desc").limit(1).get();

  const row = document.createElement("tr");
  if (snapshot.docs.length > 0) {
    const list = snapshot.docs[0].data();

    // const timeCell = document.createElement("td");
    // timeCell.textContent = Intl.DateTimeFormat("id-ID", {
    //   dateStyle: "long",
    //   timeStyle: "short",
    // }).format(new Date(list.ts.seconds * 1000));

    const humidityCell = document.createElement("td");
    humidityCell.textContent = list.hum + " %";

    const windCell = document.createElement("td");
    windCell.textContent = list.anemo + " km/h";

    // const rainfallCell = document.createElement("td");
    // rainfallCell.textContent = list.r + " mm";

    const soilCell = document.createElement("td");
    soilCell.textContent = list.soil;

    const tempCell = document.createElement("td");
    tempCell.textContent = list.temp + " C";

    // row.appendChild(timeCell);
    row.appendChild(humidityCell);
    row.appendChild(windCell);
    // row.appendChild(rainfallCell);
    row.appendChild(soilCell);
    row.appendChild(tempCell);

    const body = document.getElementById("weather-table").querySelector("tbody");
    body.appendChild(row);
  } else {
    const noDataCell = document.createElement("td");
    noDataCell.textContent = "Tidak ada data cuaca";
    noDataCell.colSpan = 4;
    row.appendChild(noDataCell);
    body.appendChild(row);
  }
}

fetchWeatherData();

db.collection("weather_data").orderBy("ts", "desc").limit(1).onSnapshot((snapshot) => {
  const body = document.getElementById("weather-table").querySelector("tbody");
  body.innerHTML = "";
  fetchWeatherData();
});