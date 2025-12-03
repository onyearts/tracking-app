// static/admin/js/shipment_admin.js - UPDATED VERSION
document.addEventListener('DOMContentLoaded', function() {
    // Wait for Django jQuery to be available
    function waitForjQuery() {
        if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
            initTrackingGenerator();
        } else {
            setTimeout(waitForjQuery, 100);
        }
    }
    
    function initTrackingGenerator() {
        var $ = django.jQuery;
        
        // Find elements
        var generateBtn = $('#generate-tracking');
        var carrierField = $('#id_carrier');
        var trackingField = $('#id_shipment_number');
        
        if (generateBtn.length && carrierField.length && trackingField.length) {
            console.log('Tracking generator initialized');
            
            // Click handler for generate button
            generateBtn.on('click', function(e) {
                e.preventDefault();
                console.log('Generate button clicked');
                
                var carrierId = carrierField.val();
                var carrierText = carrierField.find('option:selected').text();
                
                console.log('Carrier ID:', carrierId, 'Carrier Text:', carrierText);
                
                if (!carrierId) {
                    alert('Please select a carrier first!');
                    carrierField.focus();
                    return;
                }
                
                // Show loading
                var originalText = generateBtn.text();
                generateBtn.text('Generating...').prop('disabled', true);
                
                // Get the current form URL to construct the correct generate URL
                var formAction = $('form#shipment_form').attr('action') || window.location.pathname;
                var baseUrl = formAction.replace('/add/', '/').replace('/change/', '/');
                if (baseUrl.endsWith('/')) {
                    baseUrl = baseUrl.slice(0, -1);
                }
                var generateUrl = baseUrl + '/generate-tracking/';
                
                console.log('Making request to:', generateUrl);
                
                // Make AJAX request
                $.ajax({
                    url: generateUrl,
                    type: 'GET',
                    data: {
                        'carrier_id': carrierId,
                        'carrier_name': carrierText
                    },
                    success: function(data) {
                        console.log('Success response:', data);
                        if (data.success) {
                            trackingField.val(data.tracking_number);
                            
                            // Add success indicator
                            var indicator = $('<span>')
                                .addClass('success-indicator')
                                .text(' ✓ Auto-generated')
                                .css({
                                    'color': 'green',
                                    'margin-left': '10px',
                                    'font-size': '12px'
                                });
                            
                            // Remove existing indicator
                            $('.success-indicator').remove();
                            trackingField.after(indicator);
                            
                            // Hide indicator after 3 seconds
                            setTimeout(function() {
                                indicator.fadeOut(500, function() {
                                    $(this).remove();
                                });
                            }, 3000);
                        } else {
                            alert('Error: ' + (data.error || 'Unknown error'));
                        }
                    },
                    error: function(xhr, status, error) {
                        console.log('AJAX Error:', status, error, xhr.responseText);
                        alert('Error generating tracking number. Check console for details.');
                    },
                    complete: function() {
                        generateBtn.text(originalText).prop('disabled', false);
                    }
                });
            });
            
            // Auto-generate when carrier changes (if tracking field is empty)
            carrierField.on('change', function() {
                if (!trackingField.val().trim()) {
                    setTimeout(function() {
                        if (!trackingField.val().trim() && carrierField.val()) {
                            generateBtn.click();
                        }
                    }, 500);
                }
            });
        } else {
            console.log('Required elements not found');
        }
    }
    
    waitForjQuery();
});
