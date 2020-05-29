
function readURL(input, obj) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#blah')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }

    var file = obj.value;
    var fileName = file.split("\\");
    document.getElementById("img").innerHTML = fileName[fileName.length - 1];
    document.myForm.submit();
    event.preventDefault();
    
};

function getFile() {
    document.getElementById("profile-image").click();
};

function submit() {
    document.getElementById("submit").click();
};
  