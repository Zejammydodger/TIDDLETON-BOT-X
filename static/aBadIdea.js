
function writeUniqueMessages(jsonText) {
			console.log("THIS IS A TEST LOOK MA IT WORKED");
			for (const [name , opinion] of Object.entries(jsonText)){
				var li = document.createElement("LI");
				var ul = document.getElementById("aReallyDumbIdea");
				var textnode = document.createTextNode(name + "'s opinion of us is: '" + opinion + "'");
				li.appendChild(textnode);
				ul.appendChild(li);
			}
		}