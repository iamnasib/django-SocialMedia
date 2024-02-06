function myFunction(){
    document.getElementById('submit').click();
}
function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function (e) {
        $('#preview').attr('src', e.target.result).width(125).height(125);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }

