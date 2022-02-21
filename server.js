#!/usr/bin/env node

const express = require("express");
const fs = require("fs");
const { loadFile } = require("./apis/loadDB.js");

const app = express();

// This might not be so perfect!
app.use("/", express.static(__dirname + "/public", {extensions:['html']}));

const HOST = "localhost";
const PORT = process.env.PORT || 3000;

app.listen(PORT, HOST, () => console.log(`listening on http://${HOST}:${PORT}`));

// stream blog-info db data
app.get("/blog/all-posts", async (req, res) => {

  const blogInfoFilePath = __dirname + "/db/blog-info.json";

  // const stream = fs.createReadStream(blogInfoFilePath);
  // stream.pipe(res);

  const data = await loadFile(blogInfoFilePath);
  res.json(JSON.parse(data));

});

app.get("/blog/category-tags", (req, res) => {
  res.sendFile(__dirname + "/db/category-tags.json", (err) => {
    if (err) console.log(err);
  });
});

app.get("/github", (req, res) => {
  res.redirect("https://github.com/lostvikx");
});

app.get("/blog/posts", (req, res) => {
  res.redirect("/blog");
});

app.get("*", (req, res) => {
  res.redirect("/404.html");
});