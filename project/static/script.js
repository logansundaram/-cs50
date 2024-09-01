let count = 0;

for (let i = 1; i < 51; i++) {
  if (document.getElementById(String(i))) {
    count++;
  }
}


let day = "Monday";
let description = "default value";
let create = document.getElementById("create");
let status = "Incomplete"

// Create a JSON object with the variables


create.addEventListener("submit", function(event) {
  event.preventDefault();
  description = document.getElementById("description").value
  let button = document.getElementById("create_button")
  let table = document.getElementById("table_body");
  let row = document.createElement("tr");
  count++;
  row.id = "" + count;
  let html = `
                  <th scope="row">${count}</th>
                  <td>${description}</td>
                  <td>${day}</td>
                  <td><button type="button" class="btn btn-danger"onclick="change(event)">Incomplete</button></td>
  `;
  row.innerHTML = html;
  table.appendChild(row);

  let data = {
    id: count,
    day: day,
    description: description,
    status: status,
  };

  // Send the data to the Flask server
  fetch('https://stunning-giggle-w5wp76gvj5ghgx6j-5000.app.github.dev/agenda', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
        return response.text().then(text => { throw new Error(text) });
    }

    const contentType = response.headers.get('Content-Type');
    //if (contentType.includes('application/json')) {
        return response.json();
    //} else {
        //return response.text().then(text => { throw new Error('Response is not JSON: ' + text) });
    //}
})
.then(data => {
    console.log(data.message);  // Log the response from the Flask server
})
.catch(error => {
    console.error('Error:', error);  // Log any errors
});
  // Log the values to the console (or process them as needed)
  // Further processing, such as sending data to a server, can be done here
})

function deleteTask(event){
  let button = event.target;
  let row = document.getElementById(""+count);

  let data = {
    count: count,
  }
  fetch('https://stunning-giggle-w5wp76gvj5ghgx6j-5000.app.github.dev/delete', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())  // Use response.json() to parse the JSON response
  .then(data => {
    console.log('Success:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });

  if (count>0)
    count--;
  row.remove();

}


function changeDate(event){
    let button = event.target;
    day = button.innerHTML;
    button.setAttribute("class", "btn btn-success");
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
    days.forEach(d => {
        if (document.getElementById(d) !== button) {
            document.getElementById(d).setAttribute("class", "btn btn-danger");
        }
    });
}

function change(event){
    let button = event.target;
    let status;


    if (button.innerHTML == "Incomplete"){
      status = "Complete";
      button.innerHTML = "Complete"
      button.className = "btn btn-success";
    }
    else if (button.innerHTML == "Complete"){
      status = "Incomplete";
      button.innerHTML = "Incomplete"
      button.className = "btn btn-danger";
    }

    let count = Number(button.name);

    let data = {
      count: count,
      status: status,
    }
    fetch('https://stunning-giggle-w5wp76gvj5ghgx6j-5000.app.github.dev/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())  // Use response.json() to parse the JSON response
    .then(data => {
      console.log('Success:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }
