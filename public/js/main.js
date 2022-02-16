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

const createPost = (data) => {

  const post = document.createElement("div");
  post.className = "post";
  
  const a = document.createElement("a");
  a.href = data.pathToHTMLFile;

  post.append(a);
  
  const postDiv = document.createElement("div");
  postDiv.className = "post-div";
  a.append(postDiv);

  const info = document.createElement("div");
  info.className = "post-info";

  const h3 = document.createElement("h3");
  h3.textContent = data.postTitle;
  h3.className = "post-title";
  const p = document.createElement("p");
  p.textContent = data.postSubject;
  p.className = "post-subject";
  const time = document.createElement("p");
  time.textContent = data.timeCreated;
  time.className = "time-created";

  info.append(h3, p, time);

  const img = document.createElement("img");
  img.src = data.thumbnail;
  img.alt = "blog post thumbnail";

  const postImg = document.createElement("div");
  postImg.className = "post-img";
  postImg.append(img);

  postDiv.append(postImg, info);

  return post;
}

if (pathName === "/blog/" || pathName === "/blog/index.html" || pathName === "/blog/index") {
  
  // get all posts
  const allPosts = await getAllBlogPosts();
  console.log(allPosts);

  const allPostsUl = document.getElementById("all-posts");

  for (const post of allPosts) {
    allPostsUl.appendChild(createPost(post));
  }

  
}