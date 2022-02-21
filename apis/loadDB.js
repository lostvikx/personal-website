#!/usr/bin/env node

const fs = require("fs");

const loadFile = (filePath) => {

  const stream = fs.createReadStream(filePath);
  let blogInfoData = [];

  return new Promise((resolve, reject) => {

    stream.on("data", (chunk) => blogInfoData.push(Buffer.from(chunk)));

    stream.on("error", (err) => reject(err));

    stream.on("end", () => resolve(Buffer.concat(blogInfoData).toString("utf-8")));

  });

}

// test func
// (async () => {
//   const results = await loadFile(__dirname + "/../db/blog-info.json");
//   const data = JSON.parse(results);

//   console.log(data.results);
//   // return data.results;
// })();

module.exports = { loadFile };