<?php
   // $sname = $_REQUEST["sensorName"];
	$lastSec = $_REQUEST["lastSec"];
	$lastUSec = $_REQUEST["lastUSec"];
      
	$m = new MongoClient("mongodb://127.0.0.1");
   // echo "Connection to database successfully".PHP_EOL;
	$db = $m->rskills;
   // echo "Database android_test selected".PHP_EOL;
	date_default_timezone_set('Europe/Rome'); 
   //$colName = date('y.m.d.T'); // get current data in Rome
	$collection =  $db->resultlog; // Connect to DB
    $current= new MongoDate(time());
    $past = new MongoDate($lastSec, $lastUSec);
    if ($lastSec) {
        $resultCursor = $collection->find(array("timestamp" => array('$gt' => $past)))->sort(array("timestamp" => 1))->limit(1);
        }
        else {
           $resultCursor = $collection->find()->sort(array("timestamp" => -1))->limit(1);

        }
//		    $resultCursor->sort(array("sensorName" => 1));
	$result = decodeMongoData(iterator_to_array($resultCursor), $lastSec);
//	$result = iterator_to_array($resultCursor);
	echo json_encode($result);
?>

<?php

// Turn MongoData into 2-dimentional array
function decodeMongoData( $mongoData, $lastSec ) {
   $data = array();
   $count = 0;
   foreach ($mongoData as $key1 => $value1) {
      $data[$count] = array();
      $data[$count]["id"] = $key1;
      foreach ($value1 as $key2 => $value2) {
         if ($key2 == "nodes") {
            $data[$count]["nodes"] = $value2;
         }
         elseif ($key2 == "edges") {
            $data[$count]["edges"] = $value2;
         } 
         elseif ($key2 == "timestamp") {
            $data[$count]["timeSec"] = $value2->sec; 
            $data[$count]["timeUSec"] = $value2->usec; 
         } 
      }
      $count++; 
   }
   return $data; 
}

?>