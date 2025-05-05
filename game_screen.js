fetch("/fly_to", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    destination: ""
  })
})
.then(response => response.json())
.then(data => console.log(data));