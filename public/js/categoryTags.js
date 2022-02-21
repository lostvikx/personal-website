"use strict";

import { getTagPosts } from "./blogPosts.js";


const getCategoryTags = async () => {

  try {
    const res = await fetch("/blog/category-tags");
    const data = await res.json();
    
    return data;
  } catch (err) {
    console.error(err, "getCategoryTags failed!");
  }

}

// TODO [ ]: add some colors to tags
const createTag = (name, frequency) => {

  const div = document.createElement("div");
  div.textContent = `#${name} `;
  div.className = "tag";

  const span = document.createElement("span");
  span.textContent = `${frequency}`;
  span.className = "freq";

  div.appendChild(span);

  div.addEventListener("click", (evt) => {

    evt.preventDefault();
    const tagName = evt.target.textContent.slice(1,).split(" ")[0];

    // console.log(tagName);
    getTagPosts(tagName);

  });

  return div;

}

export { getCategoryTags, createTag };