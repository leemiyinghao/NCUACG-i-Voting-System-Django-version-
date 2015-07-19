<?php
ini_set('display_errors',"0");
session_start();
require_once('twitteroauth/twitteroauth.php');
require_once('config.php');
$screen_name;
if(empty($_SESSION['screen_name'])){
    if(!empty($_SESSION['access_token']) && !empty($_SESSION['access_token']['oauth_token']) && !empty($_SESSION['access_token']['oauth_token_secret'])) {
        $access_token = $_SESSION['access_token'];
        $connection = new TwitterOAuth(CONSUMER_KEY, CONSUMER_SECRET, $access_token['oauth_token'], $access_token['oauth_token_secret']);
        $content = $connection->get('account/verify_credentials');
        $_SESSION['screen_name'] = $content->screen_name;
        $screen_name=$content->screen_name;
    }
}else{
    $screen_name = $_SESSION['screen_name'];
}
$id = empty($_GET['id'])?"none":$_GET['id'];
require_once('db.php');
?>
<!DOCTYPE html>
<html>
  <head>
    <title>NCUACG i-Voting System BETA</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <meta name="description" content="" />
    <meta name="copyright" content="" />
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <link rel="stylesheet" type="text/css" href="style.css" media="all" />
    <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css">
    <style>
      li{
      line-height: 230%;
      list-style: none;
      }
      li span{
      margin-left: 15px;
      }
    </style>
  </head>
  <body>
    <div class="page-container">
    <div class="navbar navbar-inverse">
	<div class="container">
	  <a href="./" class="navbar-brand">NCUACG i-Voting<span style="color: cyan"> BETA</span></a>
<?php if(empty($screen_name)) : ?>
	  <p class="navbar-right navbar-text">You have not yet login.</p>
<?php else : ?>
          <span class="navbar-right navbar-text">Logged as: <a href="https://twitter.com/<?php echo $screen_name?>" target="_blank" class="navbar-link"><?php echo $screen_name?></a></span>
<?php endif; ?>
	    </div>
      </div>
    </div>
    <div class="container">
<?php if(empty($screen_name)) : ?>
      <h3>Please Sign in with your Twitter account.</h3>
      <a href="./redirect.php"><img src="./images/lighter.png" alt="Sign in with Twitter"/></a>
<?php elseif($db_votableList->contain($screen_name)) : ?>
<?php if(!file_exists("list.db")) : ?>
    <h1>FATAL ERROR: 'list.db' not found.</h1>
<?php else : ?>
<?php
$listFile = fopen("list.db","r");
?>
    <ul class="votelist">
<?php while($buffer=fgets($listFile)) : ?>
<?php
$bfArr = split(",",$buffer);
$votedFile = fopen("voted.$bfArr[0].db","r");
$hasVoted = false;
while($votedUser=fgets($votedFile)){
    if($screen_name == substr($votedUser,0,-1)){
        $hasVoted = true;
        break;
    }
}
fclose($votedFile);
?>
<li<?php if($hasVoted) echo " class=\"hasvoted\""?>><i class="fa fa-check-square-o"></i> <a href="voteroom.php?id=<?php echo $bfArr[0];?>"><?php echo $bfArr[1];?></a><?php if($hasVoted) echo "<span>VOTED</span>"?></li>
<?php endwhile; ?>
<?php endif; ?>
<?php endif; ?>
    </ul>
    </div>
    <div class="clear"></div>
    <div id="footer">
      <i>NCUACG, All Right Reserve.</i>
      <br>
      <i>by catLee,leemiyinghao@gmx.com</i>
    </div>
</div>
</body></html>
