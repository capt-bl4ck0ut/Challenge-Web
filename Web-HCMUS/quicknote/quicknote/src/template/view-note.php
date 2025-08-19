<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $page_title ?? 'QuickNote'; ?></title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="template/view-note.css">
</head>
<body>
    <div class="main-container">
        <nav class="navbar navbar-custom">
            <div class="container-fluid px-4">
                <span class="navbar-brand mb-0 h1 text-white">
                    <i class="fas fa-sticky-note me-2"></i>
                    <?php echo $navbar_title ?? 'QuickNote'; ?>
                </span>
                <a href="index.php" class="btn btn-back">
                    <i class="fas fa-arrow-left me-2"></i>Back to QuickNote
                </a>
            </div>
        </nav>
        
        <?php include $content_template; ?>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>