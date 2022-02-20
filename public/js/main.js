"use strict";

import { getAllBlogPosts, createPost } from "./blogPosts.js";
import { getCategoryTags, createTag } from "./categoryTags.js";

console.log(window.location);

// pre code hightlights
hljs.highlightAll();

const pathName = window.location.pathname;
const isBlogPost = /^\/blog\/[\S]+/.test(pathName);

if (isBlogPost) {
  console.log("is a blog post!");
  // Article reading time
  const calcReadingTime = () => {
    const articleText = document.getElementById("article").innerText;
    const wordsPerMinute = 180; // This is a good reading speed to understand the content.
    const nWords = articleText.trim().replace(/[^\w\s\d]/g, "").split(/\s+/).length;
    const time = Math.ceil(nWords / wordsPerMinute)

    return `${time} ${time == 1 ? "minute" : "minutes"}`;
  }
  
  const updatePostInfo = () => {
    const postInfo = document.getElementById("post-info");
    const readingTime = document.createElement("p");
    readingTime.className = "post-meta";
    readingTime.textContent = `Reading Time: ${calcReadingTime()}`;
    postInfo.appendChild(readingTime);
  }

  try {
    updatePostInfo();
  } catch (err) {
    console.log("Reading time was not shown.");
    // console.log(err);
  }
}

const renderPosts = (posts) => {
  const allPostsDiv = document.getElementById("all-posts");

  for (const post of posts) {
    allPostsDiv.appendChild(createPost(post));
  }
}

if (pathName === "/blog/" || pathName === "/blog/index.html" || pathName === "/blog/index") {
  
  // TODO [ ]: create meta-attribute for article tags, filtering
  // TODO [ ]: don't get all posts, get about 20 posts, use url query

  const [ allPosts, allTags ] = await Promise.all([getAllBlogPosts(), getCategoryTags()]);

  // Posts
  renderPosts(allPosts);

  // Tags
  // TODO [*]: sorting by latest
  const tagFrequencyArray = Object.entries(allTags.tagFrequency).sort((a, b) => (a[1] < b[1]) ? 1 : (a[1] === b[1]) ? 0 : -1);

  console.log(tagFrequencyArray);
  const postTags = document.getElementById("post-tags");

  for (const [ name, frequency ] of tagFrequencyArray) {
    postTags.appendChild(createTag(name, frequency));
  }

  // TODO [ ]: show only the top 5 tags, rest in show more drop down

}