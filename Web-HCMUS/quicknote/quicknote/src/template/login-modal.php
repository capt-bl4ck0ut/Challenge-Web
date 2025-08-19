<div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="loginModalLabel">
                    <i class="fas fa-sign-in-alt me-2"></i>Login to QuickNote
                </h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form method="post" id="loginForm">
                    <div class="mb-3">
                        <label for="loginUsername" class="form-label fw-bold">
                            <i class="fas fa-user me-1 text-primary"></i>Username
                        </label>
                        <input type="text" class="form-control" id="loginUsername" name="username" required 
                               placeholder="Enter your username">
                    </div>
                    <div class="mb-4">
                        <label for="loginPremiumKey" class="form-label fw-bold">
                            <i class="fas fa-key me-1 text-warning"></i>Premium Key
                            <small class="text-muted">(optional)</small>
                        </label>
                        <input type="text" class="form-control" id="loginPremiumKey" name="premium_key" 
                               placeholder="Enter premium key for extended features">
                    </div>
                    <input type="hidden" name="action" value="login">
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary-custom">
                            <i class="fas fa-sign-in-alt me-2"></i>Login Now
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>