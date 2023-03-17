 const spinner = document.getElementById("spinner");

    console.log(spinner);
    $.ajax({
    type:'GET',
    url:'/',
    success: function(res){
    spinner.classList.add("visually-hidden")

    },
   });


$('#button-busca').on("click", function(){
    let busca_valor = $('#busca').val();
    console.log(busca_valor);
     if(busca_valor == ""){
        console.log("Please Enter Name");
    }else{
     $.ajax({
        type:"POST",
         beforeSend: function() {
        spinner.classList.remove("visually-hidden");
        },
        success: function(){
            spinner.classList.add("visually-hidden");
            },
    });
    }
});


$('#bairroDataList').on("change", function(){
     $.ajax({
        type:"POST",
         beforeSend: function() {
        spinner.classList.remove("visually-hidden");
        },
        success: function(){
            spinner.classList.add("visually-hidden");
            },
    });
});
$('#abrangenciaSelect').on("change", function(){
    spinner.classList.remove("visually-hidden");

    $.ajax({
        type:"POST",
         beforeSend: function() {
        spinner.classList.remove("visually-hidden");
        },
        success: function(){
            spinner.classList.add("visually-hidden");
            },
    });
});

$('#rucSelect').on("change", function(){
    spinner.classList.remove("visually-hidden");

    $.ajax({
        type:"POST",
         beforeSend: function() {
        spinner.classList.remove("visually-hidden");
        },
        success: function(){
            spinner.classList.add("visually-hidden");
            },
    });
});




$('#buttonLogar').on("click", function(){
let user = $('#id_username').val();
let password = $('#id_password').val();

 if(user == "" || password == ""){
        console.log("Please Enter Name");
    }else{
    $.ajax({
        type:"POST",
        beforeSend: function() {
        spinner.classList.remove("visually-hidden");
        },
        success: function(){
            spinner.classList.add("visually-hidden");
            },
    });
}
});


