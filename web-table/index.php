<html>


<!-----------------

results in sortable table

assumes data.csv in same directory

----------------->


<head>
	<link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/1.10.13/css/jquery.dataTables.min.css">
	<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
	<script src="https://cdn.datatables.net/1.10.13/js/jquery.dataTables.min.js"></script>
</head>
<body>





<script>

$(document).ready(function() {
    $('#example').DataTable();
} );


</script>

<?php

$row = 1;
if (($handle = fopen("data.csv", "r")) !== FALSE) {
    
    echo '<table id="example" class="display" cellspacing="0" width="100%">';
    
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $num = count($data);
        if ($row == 1) {
            echo '<thead><tr>';
        }else{
            echo '<tr>';
        }
        
        for ($c=0; $c < $num; $c++) {
            //echo $data[$c] . "<br />\n";
            if(empty($data[$c])) {
               $value = "0";
            }else{
               $value = $data[$c];
            }
            if ($row == 1) {
                echo '<th>'.$value.'</th>';
            }else{
                echo '<td>'.$value.'</td>';
            }
        }
        
        if ($row == 1) {
            echo '</tr></thead><tbody>';
        }else{
            echo '</tr>';
        }
        $row++;
    }
    
    echo '</tbody></table>';
    fclose($handle);
}
?>


</body></html>