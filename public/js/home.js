"use strict";

const fetchAbout = async () => {

  const res = await fetch("/about");
  const data = await res.text();

  return data;
}

const mdText = (await fetchAbout()).trim().split("\n");
console.log(mdText);

const isHeader = (line) => {

  return (line[0] === "#" && line !== "") ? true : false;

}

const html = "";

for (const line of mdText) {

  if (isHeader(line)) {
    console.log(line);
  }

}