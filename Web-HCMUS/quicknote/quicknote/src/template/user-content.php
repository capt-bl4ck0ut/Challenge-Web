<div class="card card-custom full-width-card">
    <div class="card-header bg-light">
        <h4 class="card-title mb-0">
            <i class="fas fa-plus-circle me-2 text-primary"></i>Create New Note
        </h4>
    </div>
    <div class="card-body">
        <form method="post">
            <div class="mb-4">
                <label class="form-label fw-bold fs-5">Note Content</label>
                <textarea name="note" class="form-control" rows="8" 
                          placeholder="Enter your note here..." 
                          style="font-size: 1.1rem;"></textarea>
                <div class="form-text mt-2">
                    <i class="fas fa-info-circle me-1"></i>
                    <?php if ($current_user->isPremium()): ?>
                        <span class="fw-bold">Premium mode: Up to 1000 characters allowed</span>
                    <?php else: ?>
                        User mode: Up to 500 characters allowed
                    <?php endif; ?>
                </div>
            </div>
            <input type="hidden" name="action" value="add_note">
            <button type="submit" class="btn btn-primary-custom btn-lg">
                <i class="fas fa-save me-2"></i>Save Note
            </button>
        </form>
    </div>
</div>