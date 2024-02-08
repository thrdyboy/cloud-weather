<?php


if(function_exists('sodium_crypto_secretbox')) {
    echo "Sodium extension is enabled";
} else {
    echo "Sodium extension is disabled";
}