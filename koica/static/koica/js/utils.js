function update_rating(koica_base_url, operator, question_slug, question_id, token) {
	var url = "/"+koica_base_url+"/"+question_slug+"/rating/"+operator+"/";
	var question_rating_url = "/"+koica_base_url+"/"+question_slug+"/rating/";
    $.ajax({
        type: "POST",
        url: url,
        data: {
            operator: operator,
            question_slug: question_slug,
            csrfmiddlewaretoken: token,
        },
        success: function(data) {
        	$("#rating_number").load(question_rating_url ,function(data){
        	    //console.log('Rating updated');
        	    if (operator == 'plus') {
        	    	$("#"+question_id+'_up').attr("src","/static/koica/img/up_active.png");      	    	
        	    	setTimeout(
        	    			  function() 
        	    			  {
        	    			  $("#"+question_id+'_up').fadeOut('slow');
        	    			  $("#"+question_id+'_up').attr("src","/static/koica/img/up.png");
        	    			  $("#"+question_id+'_up').fadeIn('fast');
        	    			  }, 1500);
        	    }
        	    else {
        	    	$("#"+question_id+'_down').attr("src","/static/koica/img/down_active.png");
        	    	setTimeout(
      	    			  function() 
      	    			  {
      	    			  $("#"+question_id+'_down').fadeOut('slow');
      	    			  $("#"+question_id+'_down').attr("src","/static/koica/img/down.png");
      	    			  $("#"+question_id+'_down').fadeIn('fast');
      	    			  }, 1500);
        	    }
        	});
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

function update_answer_rating(koica_base_url, operator, answer_pk, token) {
	var url = "/"+koica_base_url+"/answer/"+answer_pk+"/rating/"+operator+"/";
	var success_url = "/"+koica_base_url+"/answer/"+answer_pk+"/rating/";
    $.ajax({
        type: "POST",
        url: url,
        data: {
            operator: operator,
            answer_pk: answer_pk,
            csrfmiddlewaretoken: token,
        },
        success: function(data) {
        	$("#"+answer_pk+"_answer_rating").load(success_url ,function(data){
        	    //console.log('Rating updated');
        	    if (operator == 'plus') {
        	    	$("#"+answer_pk+"_answer_rating_up").attr("src","/static/koica/img/up_active.png");      	    	
        	    	setTimeout(
        	    			  function() 
        	    			  {
        	    			  $("#"+answer_pk+"_answer_rating_up").fadeOut('slow');
        	    			  $("#"+answer_pk+"_answer_rating_up").attr("src","/static/koica/img/up.png");
        	    			  $("#"+answer_pk+"_answer_rating_up").fadeIn('fast');
        	    			  }, 1500);
        	    }
        	    else {
        	    	$("#"+answer_pk+"_answer_rating_down").attr("src","/static/koica/img/down_active.png");
        	    	setTimeout(
      	    			  function() 
      	    			  {
      	    			  $("#"+answer_pk+"_answer_rating_down").fadeOut('slow');
      	    			  $("#"+answer_pk+"_answer_rating_down").attr("src","/static/koica/img/down.png");
      	    			  $("#"+answer_pk+"_answer_rating_down").fadeIn('fast');
      	    			  }, 1500);
        	    }
        	});
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

function approve_answer(koica_base_url, answer_id, token) {
	var url = "/"+koica_base_url+"/"+answer_id+"/approve/";
	var answer_approved_url = "/"+koica_base_url+"/"+answer_id+"/approved/";
    $.ajax({
        type: "POST",
        url: url,
        data: {
        	answer_id: answer_id,
            csrfmiddlewaretoken: token,
        },
        success: function(data) {
        	$('#'+answer_id+'_approve').load(answer_approved_url);
        },
        error: function(xhr, textStatus, errorThrown) {
        	console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}