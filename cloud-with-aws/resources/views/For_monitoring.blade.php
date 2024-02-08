@extends('templatingLayout.main')

@section('container')



<head>
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore-compat.js"></script>
</head>

<body>
    <table id="weather-table" class="table-design">
        <thead>
            <tr class="active-row">
                <!-- <th>Waktu</th> -->
                <th>Kelembapan Udara</th>
                <th>Kecepatan Angin</th>
                <!-- <th>Curah Hujan</th> -->
                <th>Kelembapan Tanah</th>
                <th>Suhu</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>


    <div>
        <h6 class="d-inline-block me-1">Interval Waktu</h6><br>
        <div class="d-inline-block me-1">
            <label for="customRange3">Waktu Interval (Menit):</label> <input type="range" class="form-control-range" min="1" max="60" step="1" value="30" id="customRange3" style="width: 150%;" onInput="updateRangeValue(this.value)"><br>
            <span id="rangeval">30</span> Menit
        </div>
    </div>


    <div class="ButtonDesign">
        <button id="toggleBtn" onclick="toggleButton()" class="btn btn-primary">Activate</button>

        <p>Current State: <span id="statePlacing"></span></p>
    </div>
    <script type="module">


    </script>
    <script src="{{ asset('js/buttonWithCookies.js') }}"></script>
    <script src="{{ asset('js/app.js') }}"></script>


</body>
@endsection