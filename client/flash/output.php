<?php
$kv = new SaeKV();
$ret = $kv->init();

if (!isset($_POST["code"]))
{
	$ret = $kv->get('main.py');
	echo $ret;
	exit;
}
$data = $_POST["code"];


$ret = $kv->set('main.py', $data);
$ret = $kv->get('main.py');
echo "sucess";

?>
