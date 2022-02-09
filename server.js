#!/usr/bin/env node

const express = require("express");
const app = express();

// This is perfect!
app.use("/", express.static(__dirname + "/public", {extensions:['html']}));

const HOST = "localhost";
const PORT = process.env.PORT | 3000;

app.listen(PORT, HOST, () => console.log(`listening on http://${HOST}:${PORT}`));

// send md file
// app.get("/about", (req, res) => {

//   res.sendFile(__dirname + "/about.md", (err) => {
//     if (err) {
//       console.log(err);
//     }
//   })

// });

app.get("/github", (req, res) => {
  res.redirect("https://github.com/lostvikx");
});

app.get("/blog/posts", (req, res) => {
  res.redirect("/blog");
});

// TODO: 404 Page
app.get("*", (req, res) => {

  res.status(404).send("nani? 404 not found");

});