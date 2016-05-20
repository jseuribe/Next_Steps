$(document).ready(function(){
	<!--GPA must contain a value-->
	$('#inputTuition').on('input', function() {
		var input=$(this);
		var tuition=input.val();
		if(tuition && tuition != "tuition_limit_empty"){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});		

	<!--State must contain a value-->
	$('#inputState').on('input', function() {
		var input=$(this);
		var state=input.val();
		if(state && state != "state_empty"){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});	

	<!--Check whole form -->
	$("#submitPage3").click(function(event){
		var formData=$("#page3").serializeArray();
		var zeroErrors=true;

		var prefCheck = jQuery("input[name=Pref]:checked").val();
		var prefInput=$('#inputPref2');
		var prefError=$("span", prefInput.parent());

		if(!prefCheck){
			prefError.removeClass("error").addClass("errorShow");
		}
		else{
			prefError.removeClass("errorShow").addClass("error");
		}

		var costCheck = jQuery("input[name=Cost]:checked").val();
		var costInput=$('#inputCost2');
		var costError=$("span", costInput.parent());

		if(!costCheck){
			costError.removeClass("error").addClass("errorShow");
		}
		else{
			costError.removeClass("errorShow").addClass("error");
		}

		var distCheck = jQuery("input[name=Dist]:checked").val();
		var distInput=$('#inputDist2');
		var distError=$("span", distInput.parent());

		if(!distCheck){
			distError.removeClass("error").addClass("errorShow");
		}
		else{
			distError.removeClass("errorShow").addClass("error");
		}

		var acadCheck = jQuery("input[name=Acad]:checked").val();
		var acadInput=$('#inputAcad2');
		var acadError=$("span", acadInput.parent());

		if(!acadCheck){
			acadError.removeClass("error").addClass("errorShow");
		}
		else{
			acadError.removeClass("errorShow").addClass("error");
		}



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
