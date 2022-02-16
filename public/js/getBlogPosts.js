"use strict";

const getAllBlogPosts = async () => {

  const res = await fetch("/blog/all-posts");
  const data = await res.json();
  console.log(data);

}

export { getAllBlogPosts }