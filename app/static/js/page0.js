	$(document).ready(function(){
		<!--Check email input -->
		$('#inputEmail').on('input', function() {
			var input=$(this);
			var validate = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
			var isEmail=validate.test(input.val());
			if(isEmail){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});

		$('input').blur(function(){
			var pass = $('input[name=Password]').val();
			var repass = $('input[name=Repassword]').val();

			if(pass!=repass){
				$('#inputPassword').removeClass("valid").addClass("invalid");
				$('#inputRepassword').removeClass("valid").addClass("invalid");				
			}

			else{
				$('#inputPassword').removeClass("invalid").addClass("valid");
				$('#inputRepassword').removeClass("invalid").addClass("valid");		
			}

			if(($('input[name=Password]').val().length < 3) || ($('input[name=Repassword]').val().length < 3)){
				$('#inputPassword').removeClass("valid").addClass("invalid");
				$('#inputRepassword').removeClass("valid").addClass("invalid");
			}
		});

		<!--Check whole form -->
		$("#submitPage0").click(function(event){
			var formData=$("#page0").serializeArray();
			var zeroErrors=true;
			for (var input in formData){
				var element=$("#input"+formData[input]['name']);
				var valid=element.hasClass("valid");
				var errorAt=$("span", element.parent());
				if (!valid){
					errorAt.removeClass("error").addClass("errorShow");
					element.removeClass("valid").addClass("invalid");
					zeroErrors=false;
				}
				else{
					errorAt.removeClass("errorShow").addClass("error");
				}
			}
			if (!zeroErrors){
				event.preventDefault(); 
			}
		});
	});