@extends('templatingLayout.main')

@section('container')
<head>
    <link rel="stylesheet" href="home.css">
</head>
<body>
    <h1 class="opening-words">Welcome</h1>
    <h2 class="second-words">Here's about the weather today</h2>
    <div class="desain-for-table">
        <p class="for-normal-text">What About the Weather Condition today, so lets check the button Below</p>
    </div>
    <button>
        <a href="/monitoring">Monitoring for Weather</a>
    </button>

    <p class="About-Design-Sentence">This is about the maker of Web</p>
    <button>
        <a href="/about">About Us</a>
    </button>
</body>

@endsection