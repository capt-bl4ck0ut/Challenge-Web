<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuickNote</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="template/style.css">
</head>
<body>
    <div class="main-container">
        <nav class="navbar navbar-custom">
            <div class="container-fluid px-4">
                <span class="navbar-brand mb-0 h1 text-white">
                    <i class="fas fa-sticky-note me-2"></i>
                    QuickNote
                </span>
                <?php 
                if ($current_user->username === 'anonymous') {
                    include 'template/navbar-anonymous.php';
                } else {
                    $username = htmlspecialchars($current_user->username ?? '');
                    include 'template/navbar-logged-in.php';
                }
                ?>
            </div>
        </nav>
        
        <div class="main-content">
            <div class="content-grid">
                <?php if (isset($message)): ?>
                    <div class="alert alert-info alert-custom d-flex align-items-center full-width-card" role="alert">
                        <i class="fas fa-info-circle me-2"></i>
                        <div><?php echo $message; ?></div>
                    </div>
                <?php endif; ?>
                
                <?php if ($current_user->username === 'anonymous'): ?>
                    <?php include 'template/anonymous-form.php'; ?>
                <?php else: ?>
                    <?php include 'template/user-content.php'; ?>
                <?php endif; ?>
            </div>
        </div>
    </div>

    <?php include 'template/login-modal.php'; ?>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        function openLoginModal() {
            const modal = new bootstrap.Modal(document.getElementById('loginModal'));
            modal.show();
        }
        
        
        document.getElementById('loginModal').addEventListener('shown.bs.modal', function () {
            document.getElementById('loginUsername').focus();
        });
    </script>
</body>
</html>