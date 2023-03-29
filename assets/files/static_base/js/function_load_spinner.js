const spinner = document.getElementById("spinner");
spinner.classList.remove("visually-hidden");
$(window).on('load', function () {
    spinner.classList.add("visually-hidden");
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
        complete: function () {
                $('#spinner-div').hide();//Request is complete so hide spinner
            }
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


$('#nav-home').on("click", function(){
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

$('#nav-dados').on("click", function(){
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

$('#nav-alteracoes').on("click", function(){
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

$('#nav-cadastros').on("click", function(){
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
// 
$('#lista-completa-cad').on("click", function(){
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


