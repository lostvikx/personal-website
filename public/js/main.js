"use strict";

import { getAllBlogPosts } from "./getBlogPosts.js";

console.log(window.location);

// pre code hightlights
hljs.highlightAll();

// Article reading time
const calcReadingTime = () => {
  const articleText = document.getElementById("article").innerText;
  const wordsPerMinute = 180; // This is a good reading speed to understand the content.
  const nWords = articleText.trim().split(/\s+/).length;
  const time = Math.ceil(nWords / wordsPerMinute)

  return `${time} ${time == 1 ? "minute" : "minutes"}`;
}
const updatePostInfo = () => {
  const postInfo = document.getElementById("post-info");
  const readingTime = document.createElement("p")
  readingTime.className = "post-meta";
  readingTime.textContent = `Reading Time: ${calcReadingTime()}`
  postInfo.appendChild(readingTime);
}

try {
  updatePostInfo();
} catch (err) {
  console.log("Reading time was not shown.");
  // console.log(err);
}

const pathName = window.location.pathname;

if (pathName === "/blog/" || pathName === "/blog/index.html" || pathName === "/blog/index") {
  console.log("hello blog index")
  // run the function to get all posts
  getAllBlogPosts();
}