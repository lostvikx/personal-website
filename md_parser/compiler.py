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
    headerId = "-".join(re.sub(r"[\W_]+", " ", headerText).strip().lower().split(" "))
    header = f"<h{len(headerType)} id=\"{headerId}\"><a href=\"#{headerId}\" class=\"topic\">{headerText}</a></h{len(headerType)}>"
    return header

  def makeLink(line):
    foundLink = re.findall(r"\[(\w+?)\]\((.+?)\)", line)
    # print(foundLink)

    for text, href in foundLink:
      if href[0:1] == "#":
        line = re.sub(r"\[(\w+?)\]\((.+?)\)", f"<a href=\"{href}\">{text}</a>", line, count=1)
      else:
        line = re.sub(r"\[(\w+?)\]\((.+?)\)", f"<a href=\"{href}\" target=\"_blank\">{text}</a>", line, count=1)

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

    # makeLink(line)

    if init:
      list += "<ul>"
      list += f"<li>{listItem}</li>"
    else:
      list += f"<li>{listItem}</li>"

    return list

  def makeCode(line):
    foundCode = re.findall(r"\`(\w+?)\`", line)
    for text in foundCode:
      line = re.sub(r"\`(\w+?)\`", f"<code>{text}</code>", line, count=1)

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
    text, imgLink = re.findall(r"\!\[(.+)\]\((.+)\)", line)[0]
    return f"<img src=\"{imgLink}\" alt=\"{text}\" />"
  
  def isHr(line):
    return line[0:3] == "---"
  
  # blockquote
  # mark
  
  with open(os.getcwd() + f"/../articles/{mdFileName}", "r") as f:

    prevLine = ""
    inCodeBlock = False
    
    for line in f:
      line = line.replace("<", "&lt;").replace(">", "&gt;")
      if not inCodeBlock: line = line.strip()

      line = makeLink(line) or line
      line = makeBold(line) or line
      line = makeItalic(line) or line
      line = makeCode(line) or line

      # print(index, line)

      if isHeader(line):
        article += makeHeader(line)
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

      if isImg(line):
        article += makeImg(line)
        line = ""

      if isHr(line):
        article += "<hr noshade />"
        line = ""

      if line != "":
        line = f"<p>{line}</p>"

      article += line

    f.close()

  return article

# createArticle("this-is-a-test.md")

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
  <link rel="stylesheet" href="../css/dark.min.css">
  <script src="../js/highlight.min.js"></script>
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

with open(os.getcwd() + "/../public/blog/test.html", "w") as file_handle:
  file_handle.write(createHTMLFile(True, createArticle("this-is-a-test.md")))
  file_handle.close()

print(os.getcwd() + "/../public/blog/test.html")
