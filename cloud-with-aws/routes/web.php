<?php

use App\Http\Controllers\IntervalController;
use App\Models\Flight;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Http;
use App\Http\Controllers\RaspberryController;
use App\Http\Controllers\SignInController;
use App\Http\Controllers\RegisterController;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/home', function() {
    return view('home', [
        "title" => "Home"
    ]);
});

Route::get('/monitoring', function() {
    return view('For_monitoring', [
        "title" => "Monitoring"
    ]);
});

Route::get('/about', function() {
    return view('About', [
        "title" => "About"
    ]);
});
