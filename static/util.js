
		$(document).ready(function() {
			$(':input').addClass("idleField");
       		$(':input').focus(function() {
       			$(this).removeClass("idleField").addClass("focusField");
				if(this.value != this.defaultValue){
	    			this.select();
	    		}
    		});
    		$(':input').blur(function() {
    			$(this).removeClass("focusField").addClass("idleField");
    		    if ($.trim(this.value) == ''){
			    	this.value = (this.defaultValue ? this.defaultValue : '');
				}
    		});
		});			
