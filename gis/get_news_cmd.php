<?php
    function get_news($country){
// for php7
    try{
        $pdo = new PDO("mysql:host=127.0.0.1;dbname=rss;port=3306", "root", "123456");
    } catch (PDOException $e) {
        echo 'Connection failed: ' . $e->getMessage();
    }
    $cur_date = date("d-M-Y");
    $sql = "select * from posts where date like '$cur_date%' limit 10";
    // From today news;
    //$sql = "select posts.*,rss_rating.country,city_map.country_iso,city_map.continent,city_map.country_currency,city_map.country_currency_iso from posts inner join rss_rating on posts.content_hash=rss_rating.content_hash inner join city_map on rss_rating.country=city_map.country where rss_rating.country='Canada' and date like '$cur_date%' limit 10;"
    // From city_map;
    //$sql = "select posts.*,rss_rating.country,city_map.country_iso,city_map.continent,city_map.country_currency,city_map.country_currency_iso from posts inner join rss_rating on posts.content_hash=rss_rating.content_hash inner join city_map on rss_rating.country=city_map.country where rss_rating.country='Canada' and date like '$cur_date%' limit 10;"
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
