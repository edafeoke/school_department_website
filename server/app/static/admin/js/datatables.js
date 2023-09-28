console.log("Worknf");
$(document).ready(function() {
    var table = $('#studentTable').DataTable({
        // DataTables configuration options
    });

    // Add level filtering functionality
    $('#level-filter').on('change', function() {
        var selectedLevel = $(this).val();
        console.log(selectedLevel);
        table.column(3).search(selectedLevel).draw();
    });
});
