$(document).ready(function() {
  const eduIdField = $('#edu_id');
  const abnField = $('#abn');
  const addressField = $('#address');
  const eduIdLabel = $('label[for="edu_id"]');
  const abnLabel = $('label[for="abn"]');
  const addressLabel = $('label[for="address"]');

  // Hide fields initially
  eduIdField.hide();
  eduIdLabel.hide();
  abnField.hide();
  abnLabel.hide();
  addressField.hide();
  addressLabel.hide();

  $('#user_role').change(function() {
    const selectedRole = $(this).val();
    
    if (selectedRole === 'education') {
      eduIdField.show();
      eduIdLabel.show();
      eduIdField.prop('required', true);  // Make the field required
      abnField.hide();
      abnLabel.hide();
      abnField.prop('required', false); // Make the field not required
      addressField.hide();
      addressLabel.hide();
      addressField.prop('required', false); // Make the field not required
    } else if (selectedRole === 'agency') {
      eduIdField.hide();
      eduIdLabel.hide();
      eduIdField.prop('required', false); // Make the field not required
      abnField.show();
      abnLabel.show();
      abnField.prop('required', true);  // Make the field required
      addressField.show();
      addressLabel.show();
      addressField.prop('required', true);  // Make the field required
    } else {
      eduIdField.hide();
      eduIdLabel.hide();
      eduIdField.prop('required', false); // Make the field not required
      abnField.hide();
      abnLabel.hide();
      abnField.prop('required', false); // Make the field not required
      addressField.hide();
      addressLabel.hide();
      addressField.prop('required', false); // Make the field not required
    }
  });
});
