"use strict";

const getCategoryTags = async () => {

  try {
    const res = await fetch("/blog/category-tags");
    const data = await res.json();
    
    return data;
  } catch (err) {
    console.error(err, "getCategoryTags failed!");
  }

}

const createTag = (name, frequency) => {

  const div = document.createElement("div");
  div.textContent = `#${name} ${frequency}`;
  div.className = "tag";

  return div;

}

export { getCategoryTags, createTag }