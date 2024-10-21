$(document).ready(function() {
  // Register page field manipulation
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

  // Initialize DataTables for the recommendation table
  $('#recommendationTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10,      // Set the default page length
    "order": [[15, "desc"]],  // Use the hidden "points" column (index 14) for sorting in descending order
    "columnDefs": [
      {
        "targets": [15], "visible": true
      },
    ]
  });

  // Initialize DataTables for the courses table
  $('#coursesTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the courses table
  $('#universityTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the occupation table
  $('#occupationTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the occupation manage table
  $('#occupationManageTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the living cost table
  $('#livingCostTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the applicant visa table
  $('#applicantVisaTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });

  // Initialize DataTables for the applicant study table
  $('#applicantStudyTable').DataTable({
    "paging": true,        // Enable pagination
    "searching": true,     // Enable searching
    "ordering": true,      // Enable column-based sorting
    "info": true,          // Show table information (e.g., "Showing X of Y entries")
    "pageLength": 10       // Set the default page length
  });
});