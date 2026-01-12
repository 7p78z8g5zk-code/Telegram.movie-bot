<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET');
header('Access-Control-Allow-Headers: Content-Type');

// Get movie query from GET parameter
$query = isset($_GET['query']) ? strtolower(trim($_GET['query'])) : '';

// Path to JSON data file
$dataFile = 'movies.json';

// Load movies data from JSON
$moviesData = [];
if (file_exists($dataFile)) {
    $jsonContent = file_get_contents($dataFile);
    $moviesData = json_decode($jsonContent, true) ?: [];
}

// Case-insensitive search
$found = false;
$link = '';

foreach ($moviesData as $movieName => $movieLink) {
    if (strtolower($movieName) === $query) {
        $found = true;
        $link = $movieLink;
        break;
    }
}

// Return JSON response
if ($found) {
    echo json_encode([
        'status' => 'found',
        'link' => $link
    ]);
} else {
    echo json_encode([
        'status' => 'not_found'
    ]);
}
?>
