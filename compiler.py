#!/usr/bin/env python3

import os
import re
import datetime
import json

# Parses the md file, outputs html string
def createArticle(mdFileName, isBlog=True):
  """
  mdFileName: md file name

  return: article html
  """

  # TODO: Add tags to articles, maybe a custom syntax in the markdown file

  article = ""
  blogTitle = ""
  blogSubject = None
  global timeCreated
  timeCreated = datetime.datetime.now().strftime("%a %b %d %X %Y")

  def isHeader(line):
    return line[0:1] == "#" and line != ""

  def makeHeader(line):
    headerType, *text = line.split(" ")
    headerText = " ".join(text)
    headerId = "-".join(re.sub(r"[\W_]+", " ", headerText).strip().lower().split(" "))
    header = f"<h{len(headerType)} id=\"{headerId}\"><a href=\"#{headerId}\" class=\"topic\">{headerText}</a></h{len(headerType)}>"
    
    if len(headerType) == 1:
      global timeCreated
      title = headerText
      header += f"<p class=\"post-info\">{timeCreated}, Author: Vikram S. Negi</p>"
      return [header, title]
    else:
      return header

  def makeLink(line):
    foundLink = re.findall(r"\[(.+?)\]\((.+?)\)", line)
    # print(foundLink)

    for text, href in foundLink:
      if href[0:1] == "#":
        line = re.sub(r"\[(.+?)\]\((.+?)\)", f"<a href=\"{href}\">{text}</a>", line, count=1)
      else:
        line = re.sub(r"\[(.+?)\]\((.+?)\)", f"<a href=\"{href}\" target=\"_blank\">{text}</a>", line, count=1)

    if foundLink: 
      # print("found:", line, end="\n\n")
      return line

  def makeItalic(line):
    foundItalic = re.findall(r"\*(.+?)\*", line)
    
    for text in foundItalic:
      line = re.sub(r"\*(.+?)\*", f"<em>{text}</em>", line, count=1)
    
    if foundItalic:
      return line

  def makeBold(line):
    foundBold = re.findall(r"\*\*(.+?)\*\*", line)
    
    for text in foundBold:
      line = re.sub(r"\*\*(.+?)\*\*", f"<strong>{text}</strong>", line, count=1)
    
    if foundBold:
      return line

  def isListItem(line):
    return line[0:1] == "*" and line[1:2] == " "

  def makeList(line, init=True):
    list = ""
    bullet, *text = line.split(" ")
    listItem = " ".join(text)

    if init:
      list += "<ul>"
      list += f"<li>{listItem}</li>"
    else:
      list += f"<li>{listItem}</li>"

    return list

  def makeCode(line):
    foundCode = re.findall(r"\`([\w ]*?)\`", line)
    for text in foundCode:
      line = re.sub(r"\`[\w ]*?\`", f"<code>{text}</code>", line, count=1)

    if foundCode:
      return line

  def isCodeBlock(line):
    return line[0:3] == "```"

  def makeCodeBlock(line):
    codeBlock = ""
    lang = ""

    if len(line) > 3:
      lang = re.findall(r"^\`\`\`(\w+)", line)[0]
      codeBlock += f"<pre><code class=\"language-{lang}\">"
    else:
      codeBlock += f"<pre><code>"
    
    return codeBlock
  
  def isImg(line):
    return line[0:1] == "!"
  
  def makeImg(line):
    foundImg = re.findall(r"^\!\[(.+?)\]\((.+?)\)", line)
    
    for alt, link in foundImg:
      line = re.sub(r"\!\[(.+?)\]\((.+?)\)", f"<img src=\"{link}\" alt=\"{alt}\" loading=\"lazy\" />", line, count=1)

    if foundImg:
      return line
  
  def isHr(line):
    return line[0:3] == "---"

  def isBlockquote(line):
    return line[0:1] == ">"

  def makeBlockquote(line):
    sign, *text = line.split(" ")
    text = " ".join(text)
    return f"<blockquote><p class=\"quote\">{text}</p></blockquote>"
  
  # TODO: error handling if syntax does has None as the input: ![]() maybe add "" (blank sting) instead of None
  # TODO: mark
  # TODO: <!-- comments -->
  # TODO: some functions seem repetitive, refactor those!

  if isBlog:
    path = os.getcwd() + f"/articles/{mdFileName}"
  else:
    path = os.getcwd() + f"/root_files/{mdFileName}"
  
  with open(path, "r") as f:

    prevLine = ""
    inCodeBlock = False
    isFirstPara = True
    
    for line in f:
      # cross site scripting (xss) security reason
      # line = line.replace("<", "&lt;").replace(">", "&gt;")
      line = line.replace("<", "&lt;")

      if not inCodeBlock: line = line.strip()

      if isImg(line):
        article += makeImg(line)
        line = ""

      line = makeLink(line) or line
      line = makeBold(line) or line
      line = makeItalic(line) or line
      
      if isBlockquote(line):
        article += makeBlockquote(line)
        line = ""

      # print(index, line)

      if isHeader(line):
        headerOut = makeHeader(line)

        if type(headerOut) == list:
          headerTag = headerOut[0]
          blogTitle += headerOut[1]
        else:
          headerTag = headerOut

        article += headerTag
        line = ""

      unorderedList = ""
      if isListItem(line):
        try:
          if not isListItem(prevLine):
            unorderedList += makeList(line, init=True)
          else:
            unorderedList += makeList(line, init=False)
        except:
          print("err: prevLine blank or first in the file")
          unorderedList += makeList(line, init=True)

        prevLine = line
        line = ""

      elif not isListItem(line):
        try:
          if isListItem(prevLine):
            unorderedList += "</ul>"
        except:
          unorderedList += "</ul>"

        prevLine = line

      article += unorderedList

      codeBlock = ""

      if isCodeBlock(line) and not inCodeBlock:
        codeBlock += makeCodeBlock(line)
        inCodeBlock = True
        line = ""

      elif isCodeBlock(line) and inCodeBlock:
        inCodeBlock = False
        codeBlock += "</code></pre>"
        line = ""

      elif inCodeBlock:
        codeBlock += line.replace("<", "&lt;").replace(">", "&gt;")
        line = ""

      article += codeBlock

      line = makeCode(line) or line

      if isHr(line):
        article += "<hr noshade />"
        line = ""

      if line != "" and isFirstPara:
        blogSubject = line
        line = f"<p>{line}</p>"
        isFirstPara = False
      elif line != "" and not isFirstPara:
        line = f"<p>{line}</p>"

      article += line

    f.close()

  # print(article)

  return {
    "article": article,
    "blogTitle": blogTitle,
    "blogSubject": blogSubject,
    "timeCreated": timeCreated
  }

# Test func
# print(createArticle("fintech-info.md"))

# Create entire HTML string
def createHTMLFile(isBlog:bool, articleHTML:list)->str:
  """
  Params: isBlog, articleHTML

  Returns: returns html string
  """

  stylePath = "./style.css"
  javascriptPath = "./js/main.js"
  codeBlockTags = {
    "css": "<link rel=\"stylesheet\" href=\"./css/dark.min.css\">",
    "js": "<script src=\"./js/highlight.min.js\"></script>"
  }

  if isBlog:
    stylePath = "../../style.css"
    javascriptPath = "../../js/main.js"
    codeBlockTags["css"] = "<link rel=\"stylesheet\" href=\"../../css/dark.min.css\">"
    codeBlockTags["js"] = "<script src=\"../../js/highlight.min.js\"></script>"

  html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{articleHTML["blogTitle"] or "Home"} | lostvikx</title>
  <link rel="stylesheet" href="{stylePath}">
  {codeBlockTags["css"] or ""}
  {codeBlockTags["js"] or ""}
</head>
<body>

  <nav>
    <div class="nav-link">[ <a href="/">Home</a> ]</div>
    <div class="nav-link">[ <a href="/blog">Blog</a> ]</div>
    <div class="nav-link">[ <a href="/github" target="_blank">GitHub</a> ]</div>
    <div class="nav-link">[ <a href="/radio">Radio</a> ]</div>
  </nav>

  <div id="article">{articleHTML["article"]}</div>

  <footer></footer>

  <script src="{javascriptPath}" type="module"></script>
</body>
</html>"""

  return html

# Input md file
while True:

  fileName = input("Enter md file to convert: ")

  if "." in fileName:
    print("Please enter the file name without the extension.")
    continue
  else:
    break


def saveHTMLFile(path, isBlog):

  with open(path, "w") as file_handle:
    file_handle.write(createHTMLFile(isBlog, createArticle(f"{fileName}.md", isBlog)))
    file_handle.close()

  print(f"Your file: {path}")

# Is a blog post or not
while True:

  confirm = ["yes", "y", "yup", "yeah"]

  isBlog = input("Is Blog? (y/N): ").lower() or "n"

  if isBlog in confirm:

    saveHTMLFile(f"{os.getcwd()}/public/blog/posts/{fileName}.html", True)
    break
  else:
    
    saveHTMLFile(f"{os.getcwd()}/public/{fileName}.html", False)
    break

# json db
def saveToDB(pathToDB, data):

  blogInfo = None

  # read and load json as dict
  with open(pathToDB, "r") as db:
    blogInfo = json.load(db)

  # TODO: append each blog post information, except the html string
  blogInfo["results"].append(data)

  # clear the data and re-write everything 
  with open(pathToDB, "w") as db:
    json.dump(blogInfo, db)

  return blogInfo


# print(saveToDB(f"{os.getcwd()}/db/blog_info.json", {
#   "articleName": "test",
#   "tags": ["fintech", "india", "finance"],
#   "articlePath": "./blog/posts/test.html"
# }))

def clearResults():
  with open(f"{os.getcwd()}/db/blog_info.json", "w") as db:
    json.dump({"results": []}, db)

# clearResults()