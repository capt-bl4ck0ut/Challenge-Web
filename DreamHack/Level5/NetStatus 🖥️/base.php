<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="src/css/bootstrap.min.css">
    <link rel="stylesheet" href="src/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="src/css/non-responsive.css">
    <title><?php if (isset($title)) echo $title; ?> NetStatus</title>
    <?php if (isset($head)) echo $head; ?>
  </head>
<body>

    <!-- Fixed navbar -->
    <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="/">NetStatus</a>
        </div>
        <div id="navbar">
          <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
          </ul>

          <ul class="nav navbar-nav navbar-right">
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
      <?php if (isset($content)) echo $content; ?>
    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript -->
    <script src="src/js/jquery.min.js"></script>
    <script src="src/js/bootstrap.min.js"></script> 
</body>
</html>
