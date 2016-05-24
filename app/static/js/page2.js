$(document).ready(function(){
	<!--GPA must contain a value-->
	$('#inputGPA').on('input', function() {
		var input=$(this);
		var gpa=input.val();
		if(gpa){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});		

	<!--SAT Reading must contain a value-->
	$('#inputSATR').on('input', function() {
		var input=$(this);
		var satR=input.val();
		if(satR){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});				

	<!--SAT Writing must contain a value-->
	$('#inputSATW').on('input', function() {
		var input=$(this);
		var satW=input.val();
		if(satW){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});		
	<!--SAT Math must contain a value-->
	$('#inputSATM').on('input', function() {
		var input=$(this);
		var satM=input.val();

		if(satM){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});		

	<!--Major-->
	$('#inputMajor').on('input', function() {
		var input=$(this);
		var major=input.val();
		if(major && major != ""){
			input.addClass("valid");
		}
		else{
			input.removeClass("valid");
		}
	});	

	<!--Degree must be selected-->
	$('#inputDegree').on('input', function() {
		var input=$(this);
		var degree=input.val();

		if(degree && degree != "degree_empty"){
			input.removeClass("invalid").addClass("valid");
		}
		else{
			input.removeClass("valid").addClass("invalid");
		}
	});	
	<!--Check whole form -->
	$("#submitPage2").click(function(event){
		var formData=$("#page2").serializeArray();
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

		var checkSATM= $("#inputSATM").hasClass("invalid");
		var checkSATR= $("#inputSATR").hasClass("invalid");
		var checkSATW= $("#inputSATW").hasClass("invalid");
		if(checkSATM || checkSATR || checkSATW){
			var sat = $('#inputSAT');
			var satError = $("span", sat.parent());
			satError.removeClass("error").addClass("errorShow");
		}
		else{
			var sat = $('#inputSAT');
			var satError = $("span", sat.parent());
			satError.removeClass("errorShow").addClass("error");
		}
		if (!zeroErrors){
			event.preventDefault(); 
		}
	});
});
function limitSAT(input){
	if(input.value < 0)
		input.value = 0;

	if(input.value > 800)
		input.value = 800;
}
function limitGrade(input){
	if(input.value < 0)
		input.value = 0;

	if(input.value > 100)
		input.value = 100;			
}
function limitACT(input){
	if(input.value < 0)
		input.value = 0;
	if(input.value > 36)
		input.value = 36;
}

$('.numericonly').bind('keyup blur',function(){ 
	$(this).val( $(this).val().replace(/[^0-9]/g,'') );
});


//Code for selecting majors
var majors = ["ComputerScience", "Homelessness","Math","Pastafarian","LiberalArts"];
majors.sort();
var appendList = document.getElementById("rightValues");
for(var i = 0; i < majors.length; i++){
	var opt = document.createElement("option");
	opt.text = majors[i];
	appendList.appendChild(opt);
}
function leftClick(){
    var selectedValue = document.getElementById("rightValues");
    var selectedItem = selectedValue.options[selectedValue.selectedIndex].text;
    var insertValue = document.getElementById("leftValues");
    var option = document.createElement("option");
    option.text = selectedItem;
    insertValue.add(option);          
    selectedValue.remove(selectedValue.selectedIndex);  
	}

	function rightClick(){
	    var selectedValue = document.getElementById("leftValues");
	    var selectedItem = selectedValue.options[selectedValue.selectedIndex].text;
	    var insertValue = document.getElementById("rightValues");
	    var option = document.createElement("option");
	    option.text = selectedItem;
	    insertValue.add(option);			
	    selectedValue.remove(selectedValue.selectedIndex);
	}					
	function inputClick(){
		var getText = document.getElementById("txtRight").value;
        var inputLeft = document.getElementById("leftValues");
        var inputRight = document.getElementById("rightValues");
        var txt = document.createElement("option");

        for(var i = 0; i < majors.length; i++){
          	if(getText == majors[i]){
          		txt.text = majors[i];
          		document.getElementById("txtRight").value = ''; //deletes text from input

          		ParseRight:
          		for(var j = 0; j < inputRight.options.length; j++ ){

			for(var k = 0; k < inputLeft.options.length; k++){
				if(inputLeft.options[k].innerHTML == getText){
					alert("Selection already exists!");
					break ParseRight;
				}
			}
          			if(inputRight.options[j].innerHTML == getText){
          				inputLeft.appendChild(txt);
          				inputRight.selectedIndex = j;
          				inputRight.remove(inputRight.selectedIndex);
          				break;
          			}
          		}
          		break;
          	}
          }
	}
