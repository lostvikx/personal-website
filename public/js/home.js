"use strict";

const article = document.getElementById("article");
const winLocRef = window.location.href;
console.log(winLocRef)

const fetchAbout = async () => {

  const res = await fetch("./markdown/hello-world.md");
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

  let header = "";

  const [headerType, ...text] = line.split(" ");
  
  const headerText = text.join(" ");
  const id = headerText.replace(/[\W_]+/g, " ").trim().toLowerCase().split(" ").join("-");

  // TODO: try to add hr after header
  header += `<h${headerType.length} id="${id}">${headerText}</h${headerType.length}>`;

  return header;

}

const createLink = (line) => {
  const found = line.match(/\[(\w+)\]\((.+)\)/);

  if (found !== null) {
    const [ fullMatch, text, href ] = found;
    return `<a href="${href}" target="_blank">${text}</a>`;
  } else {
    return null;
  }

}

const createList = (line, init=true) => {

  let list = "";
  const [bullet, ...text] = line.split(" ");
  let listItem = text.join(" ");

  listItem = createLink(listItem) || listItem;

  if (init) {
    list += "<ul>";
    list += `<li>${listItem}</li>`;
  } else {
    list += `<li>${listItem}</li>`;
  }

  return list;

}

let html = "";

for (let [i, line] of mdText.entries()) {

  if (isHeader(line)) {
    html += header(line);
    line = ""
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
    line = ""
  }

  html += line;

}

// console.log(html);
article.innerHTML = html;