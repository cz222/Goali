//Fill display with text
var fillDisplayDetails = function(title, description, priv, complete, date_created, date_completed, last_updated, complete_by) {
	$("#visual_detailsPage1").html("");
	$("#visual_detailsPage1").append('<br><h3>'+title+'</h3><br>');
	$("#visual_detailsPage1").append('<p>Description: '+description+'</p>');
	$("#visual_detailsPage1").append('<p>Private: '+priv+'</p>');
	$("#visual_detailsPage2").html("");
	$("#visual_detailsPage2").append('<br><h3>'+title+'</h3><br>');
	$("#visual_detailsPage2").append('<p>Date Created: '+date_created+'</p>');
	if (complete) {
		$("#visual_detailsPage2").append('<p>Completed: True</p>');
	} else {
		$("#visual_detailsPage2").append('<p>Completed: False</p>');
	};
	if (complete) {
		$("#visual_detailsPage2").append('<p>Date Completed: '+date_completed+'</p>');
	};
	$("#visual_detailsPage2").append('<p>Last Updated: '+last_updated+'</p>');
	$("#visual_details").show();
};
var fillDisplayNote = function(title, notes, msID, isGoal) {
	$("#note-container").html("");
	$("#note-container").append('<br><h3>'+title+' Notes</h3><br>');
	for (var i=0; i<notes.length; i++) {
		var id = notes[i].note_id;
		var note = notes[i].note_note;
		if (isGoal) {
			$("#note-container").append('<li id="ugnote'+id+'">'+note+'<br><a id="egnote-btn'+id+'" href="#">Edit</a>\t<a id="dgnote-btn'+id+'" href="#">Delete</a></li>');
		} else {
			$("#note-container").append('<li id="unote'+id+'">'+note+'<br><a id="enote-btn'+id+'" href="#">Edit</a>\t<a id="dnote-btn'+id+'" href="#">Delete</a></li>');
		}
		addNoteBtnAction(id, note, isGoal);
	};
	$("#visual_notes").hide();
	if (isGoal) {
		$("#nadd").click(function() {
			$("#gnote-form-btn").click();
		});
		$("#nsettings").click(function() {
		});
	} else {
		$("#id_milestone_id", "#note-form").val(msID)
		$("#id_milestone_id", "#enote-form").val(msID)
		$("#id_milestone_id", "#dnote-form").val(msID)
		$("#nadd").click(function() {
			$("#note-form-btn").click();
		});
		$("#nsettings").click(function() {
		});
	}
};
var addNoteBtnAction = function(id, note, isGoal) {
	if (isGoal) {
		$("#egnote-btn"+id).click(function() {
			$("#id_note_id", "#egnote-form").val(id); //add id
			$("#id_note", "#egnote-form").val(note); //update note form
			$("#egnote-form-btn").click();
		});
		$("#dgnote-btn"+id).click(function() {
			$("#id_note_id", "#dgnote-form").val(id);
			$("#dgnote-form-btn").click();
		});
	} else {
		$("#enote-btn"+id).click(function() {
			$("#id_milestone_note_id", "#enote-form").val(id); //add id
			$("#id_note", "#enote-form").val(note); //update note form
			$("#enote-form-btn").click();
		});
		$("#dnote-btn"+id).click(function() {
			$("#id_milestone_note_id", "#dnote-form").val(id);
			$("#dnote-form-btn").click();
		});
	};
};
var fillDisplayJournal = function(ttl, journals, msID, isGoal) {
	$("#journal-list").html("");
	$("#journal-entries").html("");
	$("#journal-list").append('<br><h3>'+ttl+' Journal</h3><br>');
	for (var i=0; i<journals.length; i++) {
		var id = journals[i].journal_id;
		var entry = journals[i].journal_entry;
		var title = journals[i].journal_title;
		var date = journals[i].journal_date;
		var jgoal = journals[i].journal_isGoal;
		var jmsID = journals[i].journal_msID;
		if (jgoal) {
			if ((title == null)||(title == '')) {
				$("#journal-list").append('<li id="ugjournal'+id+'"><a class="journallink" id="gentry-btn'+id+'" href="#">'+date+'</a></li>');
				$("#journal-entries").append('<div id="gentry'+id+'"></div>');
				$("#gentry"+id).append('<br><h3>'+date+'</h3><br>');
				$("#gentry"+id).append('<p>'+entry+'</p>');
			} else {
				$("#journal-list").append('<li id="ugjournal'+id+'"><a class="journallink" id="gentry-btn'+id+'" href="#">'+date+': '+title+'</a></li>');
				$("#journal-entries").append('<div id="gentry'+id+'"></div>');
				$("#gentry"+id).append('<br><h3>'+date+': '+title+'</h3><br>');
				$("#gentry"+id).append('<p>'+entry+'</p>');
			};
			$("#gentry"+id).hide();
		} else {
			if ((title == null)||(title == '')) {
				$("#journal-list").append('<li id="ujournal'+id+'"><a class="journallink" id="entry-btn'+id+'" href="#">'+date+'</a></li>');
				$("#journal-entries").append('<div id="entry'+id+'"></div>');
				$("#entry"+id).append('<br><h3>'+date+'</h3><br>');
				$("#entry"+id).append('<p>'+entry+'</p>');
			} else {
				$("#journal-list").append('<li id="ujournal'+id+'"><a class="journallink" id="entry-btn'+id+'" href="#">'+date+': '+title+'</a></li>');
				$("#journal-entries").append('<div id="entry'+id+'"></div>');
				$("#entry"+id).append('<br><h3>'+date+': '+title+'</h3><br>');
				$("#entry"+id).append('<p>'+entry+'</p>');
			};
			$("#entry"+id).hide();
		}
		journalLink(journals[i], i, journals);
	};
	$("#journal-list").show();
	$("#journalbottom").show();
	$("#journal-entries").hide();
	$("#entrybottom").hide();
	$("#visual_journal").hide();
	
	//journal add button
	if (isGoal) {
		$("#jadd").click(function() {
			$("#gjournal-form-btn").click();
		});
		$("#jsettings").click(function() {
		});
	} else {
		$("#id_milestone_id", "#journal-form").val(msID)
		$("#id_milestone_id", "#ejournal-form").val(msID)
		$("#id_milestone_id", "#djournal-form").val(msID)
		$("#jadd").click(function() {
			$("#journal-form-btn").click();
		});
		$("#jsettings").click(function() {
		});
	}
};
var journalLink = function(obj, count, journals) {
	var id = obj.journal_id;
	var isGoal = obj.journal_isGoal;
	if (isGoal) {
		$("#gentry-btn"+id).click(function() {
			addJournalBtnAction(obj, count, journals);
			$("#journal-list").hide();
			$("#journalbottom").hide();
			$("#journal-entries").show();
			$('#gentry'+id).fadeIn();
			$("#entrybottom").fadeIn();
		});
	} else {
		$("#entry-btn"+id).click(function() {
			addJournalBtnAction(obj, count, journals);
			$("#journal-list").hide();
			$("#journalbottom").hide();
			$("#journal-entries").show();
			$('#entry'+id).fadeIn();
			$("#entrybottom").fadeIn();
		});
	}
};
var addJournalBtnAction = function(obj, count, journals) {
	var id = obj.journal_id;
	var entry = obj.journal_entry;
	var title = obj.journal_title;
	var isGoal = obj.journal_isGoal;
	var msID = obj.journal_msID;
	//console.log(title);
	//set bottom bar buttons
	if (count == 0) {
		$("#entryarrowl").hide();
	} else {
		$("#entryarrowl").show();
		var prevObj = journals[count-1];
		var prevID = prevObj.journal_id;
		var prevGoal = prevObj.journal_isGoal;
		$("#entryarrowl").off('click').on('click', function() {
			if (isGoal) {
				$("#gentry"+id).hide();
			} else {
				$("#entry"+id).hide();
			};
			if (prevGoal) {
				$("#gentry"+prevID).fadeIn();
			} else {
				$("#entry"+prevID).fadeIn();
			};
			addJournalBtnAction(prevObj, count-1, journals);
		});
	};
	if (count == (journals.length-1)) {
		$("#entryarrowr").hide();
	} else {
		$("#entryarrowr").show();
		var nextObj = journals[count+1];
		var nextID = nextObj.journal_id;
		var nextGoal = nextObj.journal_isGoal;
		$("#entryarrowr").off('click').on('click', function() {
			if (isGoal) {
				$("#gentry"+id).hide()
			} else {
				$("#entry"+id).hide()
			};
			if (nextGoal) {
				$("#gentry"+nextID).fadeIn();
			} else {
				$("#entry"+nextID).fadeIn();
			}
			addJournalBtnAction(nextObj, count+1, journals);
		});
	};
	$("#entrytrash").show();
	$("#entryedit").show();
	$("#entryhome").show();
	$("#entrytrash").off('click').on('click', function() {
		if (isGoal) {
			$("#id_journal_id", "#dgjournal-form").val(id);
			$("#dgjournal-form-btn").click();
		} else {
			$("#id_milestone_id", "#djournal-form").val(msID);
			$("#id_milestone_journal_id", "#djournal-form").val(id);
			$("#djournal-form-btn").click();
		};
	});
	$("#entryedit").off('click').on('click', function() {
		if (isGoal) {
			$("#id_journal_id", "#egjournal-form").val(id);
			if ((title == null)||(title == '')) {
				title = '';
			}
			if ((entry == null)||(entry == '')) {
				entry = '';
			}
			$("#id_entry", "#egjournal-form").val(entry);
			$("#id_title", "#egjournal-form").val(title);
			$("#egjournal-form-btn").click();
		} else {
			$("#id_milestone_id", "#ejournal-form").val(msID);
			$("#id_milestone_journal_id", "#ejournal-form").val(id);
			if ((title == null)||(title == '')) {
				title = '';
			}
			if ((entry == null)||(entry == '')) {
				entry = '';
			}
			$("#id_entry", "#ejournal-form").val(entry);
			$("#id_title", "#ejournal-form").val(title);
			$("#ejournal-form-btn").click();
		};
	});
	$("#entryhome").off('click').on('click', function () {			
		$("#entrybottom").hide();
		$("#journal-entries").hide();
		if (isGoal) {
			$('#gentry'+id).hide();
		} else {
			$('#entry'+id).hide();
		}
		$("#journalbottom").fadeIn();
		$("#journal-list").fadeIn();					
	});
};