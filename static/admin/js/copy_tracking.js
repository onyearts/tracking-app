// static/admin/js/copy_tracking.js
django.jQuery(document).ready(function($) {
    // Copy tracking number functionality
    $(document).on('click', '.copy-tracking-btn', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        var $btn = $(this);
        var trackingNumber = $btn.data('tracking');
        
        // Copy to clipboard
        navigator.clipboard.writeText(trackingNumber).then(function() {
            // Show success feedback
            var originalText = $btn.html();
            $btn.html('✓ Copied');
            $btn.css('background', '#32CD32');
            
            // Revert after 2 seconds
            setTimeout(function() {
                $btn.html(originalText);
                $btn.css('background', '#417690');
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            alert('Failed to copy tracking number');
        });
    });
    
    // Make tracking numbers selectable on click
    $(document).on('click', '.tracking-number', function() {
        var range = document.createRange();
        range.selectNodeContents(this);
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    });
});