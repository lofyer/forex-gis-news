<?php
    function get_news($country){
// for php7
    try{
        $pdo = new PDO("mysql:host=127.0.0.1;dbname=rss;port=3306", "root", "pswd4mysql");
    } catch (PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }
    $pdo->query('set posts utf8;');
    $cur_date = date("d-M-Y");
    $pdo->query('create temporary table city_map_tmp select * from city_map group by country;');
    $sql = "select posts.*,rss_rating.country,city_map_tmp.country_iso,city_map_tmp.continent,city_map_tmp.country_currency,city_map_tmp.country_currency_iso from posts inner join rss_rating on posts.id=rss_rating.id inner join city_map_tmp on rss_rating.country=city_map_tmp.country where rss_rating.country='$country' and date like '23-Feb-2017%' group by content_hash;";
    //echo $sql . "</br>";
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
        echo "<a href=$url target=_blank>$url</a></br>";
        echo "$date</br>";
        echo "$content</br>";
        echo "$content_hash</br>";
    }
    echo $cur_date;
    //echo "</html>";
    }
    $param = htmlspecialchars($_GET["country"]);
    get_news($param);
?>
