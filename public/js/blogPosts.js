"use strict";

const getAllBlogPosts = async () => {

  try {
    const res = await fetch("/blog/all-posts");
    const data = await res.json();
    
    return data["results"];
  } catch (err) {
    console.error(err, "getAllBlogPosts failed!");
  }

}

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

const getTagPosts = async (tagName) => {

  const urlEndPoint = `/blog/tag?name=${tagName}`;

  try {
    const res = await fetch(urlEndPoint);
    console.log(res);
    // const data = await res.json();
    // console.log(data);

  } catch (err) {
    console.error(err, "getTagPosts failed!");
  }

}

export { getAllBlogPosts, createPost, getTagPosts };