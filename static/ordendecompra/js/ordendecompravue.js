Vue.createApp({
            data() {
                return {
                    titulo: 'Hola',
                    fecha: '11-11-2021',
                    insumos: [],
                    proveedor: 'Artisan',
                    condiciones: '',
                };
            },
            computed:{
                neto(){
                    let total = 0;
                    this.insumos.forEach(insumo => {
                        total+=(insumo.cantidad*insumo.neto)
                    });
                    return total;
                },
                iva(){
                    let total = this.neto;
                    return total * 0.19;
                },
                total(){
                    return this.neto + this.iva;
                }
            },
            methods: {
                upperCase(string){
                    return string.toUpperCase();
                },
                formatoCLP(numero){
                    return formatter.format(numero);
                },
                remplazarModal(numero){;
                    let url = '{%url "ordendecompra-detail" 1%}';
                    axios
                    .get(url.replace('1',numero))
                    .then(response => {
                        this.titulo = "Orden de compra: " + response.data.numero;
                        this.insumos = response.data.insumos;
                        this.fecha = response.data.fecha;
                        this.proveedor = response.data.nombre_proveedor;
                        this.condiciones = response.data.condiciones;
                    })
                }
            },
            mounted() {
                feather.replace();
            },
            delimiters: ['{$', '$}']
        }).mount('#app');