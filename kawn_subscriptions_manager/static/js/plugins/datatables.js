let jquery_datatable =
    $("#table1").dataTable({
        "dom": "<'row'<'col-sm-12 col-md-6'l><'col-sm-12 col-md-6'f>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        "buttons": [
            'excel',
            'csv',
            'pdf'
        ],
        "lengthMenu": [
            [10, 25, 50, 100, -1],
            [10, 25, 50, 100, "All"]
        ],
        "iDisplayLength": 10,
        "pagingType": 'full_numbers',
        "language": {
            'paginate': {
                'first': '<i class="fa-solid fa-angles-left"></i>',
                'previous': '<i class="fa-solid fa-angle-left"></i>',
                'next': '<i class="fa-solid fa-angle-right"></i>',
                'last': '<i class="fa-solid fa-angles-right"></i>',
            }
        },
        // "responsive": true,
        // "autoWidth": false,
    });