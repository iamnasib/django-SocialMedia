function readURLTales(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      fileName = document.querySelector('#file').value;
      extension = fileName.split('.').pop();
      console.log(extension)
      var a=null
      var b= null
      reader.onload = function (e) {
        if(extension=='mp4')
      {
        $('#preview').css("display","none");
        $('#vid').css("display","block");
        $('#vid').attr('src', e.target.result).width(380).height(400);

      }
      else{
        b=$('#vid').css("display","none");
        $('#preview').css("display","block");
        $('#preview').attr('src', e.target.result).width(380).height(400);
      }
        
       
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }