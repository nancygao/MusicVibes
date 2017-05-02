<?php
$checkVars = array("Push", "One", "Init", "Lower", "Strength", "Term", "Clear", "Enqueue", "Dequeue");
$bytestream = "";
if(isset($_GET['Mode']) and in_array($_GET['Mode'], $checkVars)){
	$mode = $_GET['Mode'];
	switch ($mode) {
	case "One":
        if(isset($_GET['Data']) and $_GET['Data']!=''){
            $bytestream .= hex2bin("01");
            $bytestream .= $_GET['Data'];
        }
        break;
    case "Push":
        if(isset($_GET['Data']) and $_GET['Data']!=''){
            $bytestream .= hex2bin("00");
            $bytestream .= $_GET['Data'];
        }
        break;
    case "Init":
        if(isset($_GET['Data']) and $_GET['Data']!=''){
            $bytestream .= hex2bin("02");
            $bytestream .= $_GET['Data'];
        }
        break;
    case "Lower":
        if(isset($_GET['Data']) and $_GET['Data']!=''){
            $bytestream .= hex2bin("03");
            $bytestream .= $_GET['Data'];
        }
        break;
    case "Enqueue":
        if(isset($_GET['Data']) and $_GET['Data']!=''){
            $bytestream .= hex2bin("05");
            $bytestream .= $_GET['Data'];
        }
        break;
    case "Dequeue":
        $bytestream .= hex2bin("06");
        break;
    case "Strength":
        if(isset($_GET['Data']) and $_GET['Data']!='' and is_numeric($_GET['Data'])){
            $my_int = intval($_GET['Data']);
            if($my_int>=0 and $my_int <=255){
                $bytestream .= hex2bin("04");
                $bytestream .= hex2bin(dechex($my_int));
            }
        }
        break;
    case "Clear":
        $bytestream .= hex2bin("0100");
        break;
    case "Term":
        $bytestream .= hex2bin("FF");
        break;
    default:
        echo "FAILURE<br>";
	}
}

echo "$bytestream\n";

$address = '127.0.0.1';
$port = 9874;

$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
if($socket===false){
	echo"socket_create() failed: reason: ".socket_strerror(socket_last_error())."\n";
} else {
	echo "OK.\n";
}
$result = socket_connect($socket, $address, $port);
/*while($result === false){
    sleep(.1);
    $result = socket_connect($socket, $address, $port);
}*/

socket_write($socket, $bytestream, strlen($bytestream));

socket_close($socket);

?>

//if ($_SERVER['REQUEST_METHOD'] == "POST") {
//
//}
