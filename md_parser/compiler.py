#!/usr/bin/env python3

import os
import re

def createArticle(mdFileName):
  """
  mdFileName: md file name

  return: article html
  """

  article = ""

  def isHeader(line):
    return line[0:1] == "#" and line != ""

  def makeHeader(line):
    headerType, *text = line.split(" ")
    headerText = " ".join(text)
    headerId = "-".join(re.sub("[\W_]+", " ", headerText).strip().lower().split(" "))
    header = f"<h{len(headerType)} id=\"{headerId}\"><a href=\"#{headerId}\" class=\"topic\">{headerText}</a></h{len(headerType)}>"
    return header

  with open(os.getcwd() + f"/../articles/{mdFileName}", "r") as f:
    
    for index, line in enumerate(f):
      line = line.strip()

      print(index, line)

      if isHeader(line): article += makeHeader(line)

    f.close()

  return article

createArticle("this-is-a-test.md")

def createHTMLFile(isBlog:bool, articleHTML:str)->str:
  """
  Params: isBlog, articleHTML

  Returns: returns html string
  """

  stylePath = "../style.css"
  javascriptPath = "../js/main.js"

  if not isBlog:
    stylePath = stylePath[1:]
    javascriptPath = javascriptPath[1:]

  html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>lostvikx | Home</title>
  <link rel="stylesheet" href="{stylePath}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&display=swap" rel="stylesheet">
</head>
<body>

  <nav>
    <div class="nav-link">[ <a href="/">Home</a> ]</div>
    <div class="nav-link">[ <a href="/blog">Blog</a> ]</div>
    <div class="nav-link">[ <a href="/github" target="_blank">GitHub</a> ]</div>
    <div class="nav-link">[ <a href="/radio">Radio</a> ]</div>
  </nav>

  <div id="article">{articleHTML}</div>

  <footer></footer>

  <script src="{javascriptPath}" type="module"></script>
</body>
</html>"""

  return html

# with open(os.getcwd() + "/../public/blog/test.html", "w") as file_handle:
#   file_handle.write(createHTMLFile(True, createArticle("this-is-a-test.md")))
#   file_handle.close()

# print(os.getcwd() + "/../public/blog/test.html")