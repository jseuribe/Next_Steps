	$(document).ready(function(){
		<!--First name must contain a character-->
		$('#inputFirst').on('input', function() {
			var input=$(this);
			var name=input.val();
			if(name){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});		

		<!--Last name must contain a character-->
		$('#inputLast').on('input', function() {
			var input=$(this);
			var last=input.val();
			if(last){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});				

		<!--Address must contain a character-->
		$('#inputStreet').on('input', function() {
			var input=$(this);
			var street=input.val();
			if(street){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});		
		<!--State must have choice from dropdown-->
		$('#inputState').on('input', function() {
			var input=$(this);
			var state=input.val();

			if(state && state != "-1"){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});		
		<!--City must have a character-->
		$('#inputCity').on('input', function() {
			var input=$(this);
			var city=input.val();

			if(city){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});	
		<!--ZIP must be entered-->
		$('#inputZIP').on('input', function() {
			var input=$(this);
			var zip=input.val();

			if(zip && zip.length == 5){
				input.removeClass("invalid").addClass("valid");
			}
			else{
				input.removeClass("valid").addClass("invalid");
			}
		});	
		<!--Check whole form -->
		$("#submitPage1").click(function(event){
			var formData=$("#page1").serializeArray();
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
		
		<!--Class limits to alphabets only-->
		$('.alphaonly').bind('keyup blur',function(){ 
			$(this).val( $(this).val().replace(/[^A-Za-z]/g,'') );
		});
		<!--Class limits to numeric only-->
		$('.numericonly').bind('keyup blur',function(){ 
			$(this).val( $(this).val().replace(/[^0-9]/g,'') );
		});
	});
