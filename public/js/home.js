"use strict";

const article = document.getElementById("article");
const winLocRef = window.location.href;

const fetchAbout = async () => {

  const res = await fetch("./markdown/about-me.md");
  const data = await res.text();

  return data;
}

const mdText = (await fetchAbout()).split("\n").map(line => line.trim());
console.log(mdText);

const isHeader = (line) => {
  return (line[0] === "#" && line !== "") ? true : false;
}

const isList = (line) => {
  return (line[0] === "*" && line[1] === " ") ? true : false;
}

const header = (line) => {

  const [headerType, ...text] = line.split(" ");
  
  const headerText = text.join(" ");
  const id = headerText.replace(/[\W_]+/g, " ").trim().toLowerCase().split(" ").join("-");

  return `<h${headerType.length} id="${id}"><a href="${winLocRef}#${id}" class="topic">${headerText}</a></h${headerType.length}>`;

}

const createList = (line, init=true) => {

  let list = "";
  const [bullet, ...text] = line.split(" ");
  const listItem = text.join(" ");

  if (init) {
    list += "<ul>";
    list += `<li>${listItem}</li>`;
  } else {
    list += `<li>${listItem}</li>`;
  }

  return list;

}

let html = "";

for (const [i, line] of mdText.entries()) {

  if (isHeader(line)) {
    html += header(line);
  }
  
  if (isList(line)) {
    try {
      if (!isList(mdText[i - 1])) {
        html += createList(line);
      } else {
        html += createList(line, false);
      }
    } catch (error) {
      html += createList(line);
    }
    try {
      if (!isList(mdText[i + 1])) {
        html += "</ul>"
      }
    } catch (error) {
      html += "</ul>"
    }
  }
  

}

console.log(html);
article.innerHTML = html;