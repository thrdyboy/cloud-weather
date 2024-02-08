<?php

namespace App\Models;
use Faker\Provider\Lorem;


class Flight
{
    private static $about_post = [
        [
            "title" => "Tentang Penulis Pertama",
            "author" => "Fahmi Rafif Tiansyah",
            "post_story" => "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Hic consequuntur rerum labore. Suscipit ipsum fugit tempore aliquam nesciunt nisi debitis, quaerat provident modi cupiditate, placeat quia consequatur earum sapiente! Asperiores, deleniti optio nihil sequi cumque expedita excepturi voluptate omnis quam quidem necessitatibus minus natus animi quaerat iusto fuga ipsa quis dolorum repudiandae maiores dolorem delectus et rerum. Est excepturi doloremque nemo nisi, voluptas alias rem eveniet quisquam totam accusantium. Non maiores magni id vel cum beatae exercitationem facilis iure ea."
        ],
        [
            "title" => "Tentang Penulis Kedua",
            "author" => "Alvin Nur Fajrin",
            "post_story" => "Lorem ipsum, dolor sit amet consectetur adipisicing elit.
            Hic consequuntur rerum labore.
            Suscipit ipsum fugit tempore aliquam nesciunt nisi debitis, quaerat provident modi cupiditate, placeat quia consequatur earum sapiente! Asperiores, deleniti optio nihil sequi cumque expedita excepturi voluptate omnis quam quidem necessitatibus minus natus animi quaerat iusto fuga ipsa quis dolorum repudiandae maiores dolorem delectus et rerum. Est excepturi doloremque nemo nisi, voluptas alias rem eveniet quisquam totam accusantium. Non maiores magni id vel cum beatae exercitationem facilis iure ea."
        ]
    ];

    public static function all(){
        return self::$about_post;
    }
}
