function CreateTable(jsonText) {
  const element = document.getElementById("doc");
  console.log("Working")
  var table = document.createElement("table") // table
  var row = document.createElement("tr") // row
  var header = document.createElement("th") // heading box
  const width = (100 / (jsonText.Headers.length + 1)).toString() + "%" 
  row.style.height = "50px"
  header.style.width = width
  header.appendChild(document.createTextNode(" "))
  row.appendChild(header)
  
  for (const day of jsonText.Headers) {
    var header = document.createElement("th")
    header.style.width = width
    header.appendChild(document.createTextNode(day))
    row.appendChild(header)

  }
  table.appendChild(row)
  
  var row = document.createElement("tr")
  var header = document.createElement("th")

  header.style.width = width
  row.style.height = "680px"

  header.appendChild(document.createTextNode("Events"))
  row.appendChild(header)

  for (const event of jsonText.Events) {
    var cell = document.createElement("td")
    cell.style.width = width
    cell.appendChild(document.createTextNode(event))
    row.appendChild(cell)
  }
  table.appendChild(row)
  element.appendChild(table)
  console.log("done")
}
//where are the semi colonssssssssssssssssssssssssssssssssss

/*
this post made by neo is a really old boomer;
oh hi wace
B R U H with a capital bruh
o shit this got bigger
i see
might be quite hard
*/

/* 
this post made by wace is not a boomer;
theres one last thing i wanna figure out
we should be able to do :
    | 1  | 2  |
----|----|----|
    | E1 |    |
 Ev |----| E3 |
    | E2 |    |
so we can have multiple events in a day,
dunno how to do that tho
i know "rowspan=x" exists
*/