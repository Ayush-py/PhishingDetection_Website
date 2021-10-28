<?php
header("Access-Control-Allow-Origin: *");

$site=$_POST['url'];

//$html = file_get_contents($site);
$bytes=file_put_contents('markup.txt', $site);

$decision = exec("C:\Python27\python.exe FeatureExtraction.py $site 2>&1 ");
echo $decision;
?>
