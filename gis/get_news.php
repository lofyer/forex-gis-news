<?php
    function get_news(){
// for php7
    try{
        $pdo = new PDO("mysql:host=localhost;dbname=rss;port=3306", "root", "pswd4mysql");
    } catch (PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }
    $cur_date = date("d-M-Y");
    $sql = "select * from posts where date like '$cur_date%'";
    #$sql = 'select * from posts where date_format(str_to_date(date, "%d-%M-%Y"), "%Y%m%d")="$cur_date";';
    //$sql = "select id,src_title,src_link,url,content_hash,title,content,date_format(str_to_date(date, '%d-%M-%Y'), '%Y%m%d') as date_new from posts where date_to_str(date_new)='2016-07-02';";
    #$sql = "select distinct(src_title) from posts order by src_title;"
    echo $sql . "</br>";
    $pdo->query('set posts utf8;');
    $result = $pdo->query($sql);
    $rows = $result->fetchAll();
    //echo "<html>";
    foreach ($rows as $row) {
        $id = $row[0];
        $src_title = $row[1];
        $src_link = $row[2];
        $date = $row[3];
        $content = $row[4];
        $content_hash = $row[5];
        $url = $row[6];

        // display
        $title = $row[7];
        echo "$id</br>";
        echo "<h2>$title</h2></br>";
        echo "$src_title</br>";
        echo "$src_link</br>";
        echo "$url</br>";
        echo "$date</br>";
        echo "$content</br>";
        echo "$content_hash</br>";
    }
    echo $cur_date;
    //echo "</html>";
    }
?>
