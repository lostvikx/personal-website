#!/usr/bin/env node

const express = require("express");
const app = express();

app.use("/", express.static(__dirname + "/public"));

// 404 Page
app.get("*", (req, res) => {

  res.status(404).send("nani?")

})

const HOST = "localhost"
const PORT = process.env.PORT | 3000;

app.listen(PORT, HOST, () => console.log(`listening on http://${HOST}:${PORT}`));

