$( function() {
    $('#ordendecompra').DataTable( {
        responsive: true,
        autoWidth: true,
        destroy: true,
        deferRender: true,
        ajax: {
            url: 'http://127.0.0.1:8000/api/ordendecompra/?format=json',
            type: 'GET',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {data : 'numero'},
            {data : 'fecha'},
            {data: 'nombre_proveedor'},
            {data: 'insumos'}
        ]
    } );
});