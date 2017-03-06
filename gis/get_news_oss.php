<?php require_once './oss-php-client/vendor/autoload.php';
function get_news($country){
$url        = 'https://search.fusionworks.cn';
$app_key    = '1a5f74ab3f4df6ce883c4c158540e25e';
$login      = 'search';
$oss_api = new OpenSearchServer\Handler(array('url' => $url, 'key' => $app_key, 'login' => $login));

//$cur_date = date("Ymd", time() - 60 * 60 * 24);
$cur_date = date("Ymd", time());
$yesterday = date("Ymd", time() - 60 * 60 * 24);
$request = new OpenSearchServer\Search\Field\Search();
$request->index('db_crawl')
        ->query(urlencode($country))
        ->template('search')
        ->operator(OpenSearchServer\Search\Search::OPERATOR_OR)
        ->emptyReturnsAll()
        ->rows(9999)
        ->sort('date_news', OpenSearchServer\Search\Search::SORT_DESC)
        ->sort('title', OpenSearchServer\Search\Search::SORT_DESC)
        //->searchField('title')
        //->searchField('content')
        ->filterField('date', "[$yesterday TO $cur_date]")
        ->returnedFields('title')
        ->returnedFields('date')
        ->returnedFields('date_news')
        ->returnedFields('url')
        ->returnedFields('content')
        ->returnedFields('content_hash');
$results = $oss_api->submit($request);

echo "News from $yesterday to $cur_date</br>";
echo 'Total number of results: ' . $results->getTotalNumberFound() . '<br/>';
echo 'Number of results in this set of results: ' . $results->getNumberOfResults();

foreach($results as $key => $result) {
    //echo '<hr/>Result #'.$key.': <br/>';
    echo '<hr/>';
    echo "<h2><a href=".$result->getField("url"). " target=_blank>" .$result->getField('title').'</a></h2>';
    echo "<em>";
    echo $result->getField('content_hash');
    echo "</br>";
    echo $result->getField('date');
    echo "</br>";
    echo $result->getField('date_news');
    echo "</em>";
    echo "</br>";
    //echo "</br><a href=$result->getField('url') target=_blank>".$result->getField('url').'</a></br>';
    echo $result->getField('content');
    echo '</ul>';
}  
}
    $param = htmlspecialchars($_GET["country"]);
    get_news($param);
?>
