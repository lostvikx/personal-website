#!/usr/bin/env python3

import os
import re
import datetime
import json
import copy

# Parses the md file, outputs html string
def createArticle(mdFileName:str, isBlog=True):
  """
  mdFileName: md file name

  return: { article, blogTitle, blogSubject, timeCreated }
  """

  # TODO: Add tags to articles, maybe a custom syntax in the markdown file

  article = ""
  blogTitle = ""
  blogSubject = None
  # global variables
  global timeCreated
  timeCreated = datetime.datetime.now().strftime("%a %b %d %X %Y")
  global thumbnail
  thumbnail = ""

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
        line = re.sub(r"\[(.+?)\]\((.+?)\)", f"<a href=\"{href}\" target=\"_blank\" rel=\"noopener noreferrer\">{text}</a>", line, count=1)

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
    foundImg = re.findall(r"\!\[(.+?)\]\((.+?)\)", line)

    for alt, link in foundImg:
      global thumbnail
      if thumbnail == "": 
        # print("thumbnail is blank", link)
        thumbnail = link

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

  print(f"reading {mdFileName}...")
  
  with open(path, "r") as f:

    prevLine = ""
    inCodeBlock = False
    isFirstPara = True
    
    for line in f:
      # cross site scripting (xss) security reason
      # line = line.replace("<", "&lt;").replace(">", "&gt;")
      line = line.replace("<", "&lt;")

      if not inCodeBlock: line = line.strip()

      # if isImg(line):
      #   article += makeImg(line)
      #   line = ""

      # Check this, if any errors regarding imgs
      line = makeImg(line) or line

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
        # blogSubject = line

        if len(line) > 50:
          blogSubject = line[:47].strip() + "..."
        else:
          blogSubject = line

        line = f"<p>{line}</p>"
        isFirstPara = False
      elif line != "" and not isFirstPara:
        line = f"<p>{line}</p>"

      article += line

    f.close()

  # print(article)

  fileCom = mdFileName.split(".")
  fileName = "".join(fileCom[:-1])

  if isBlog:
    pathToHTMLFile = f"./blog/{fileName}.html"
  else:
    pathToHTMLFile = f"./{fileName}.html"

  return {
    "article": article,
    "pathToHTMLFile": pathToHTMLFile,
    "blogTitle": blogTitle,
    "blogSubject": blogSubject,
    "timeCreated": timeCreated,
    "thumbnail": thumbnail
  }

# Test func
# print(createArticle("fintech-info.md"))

def enterTags(nTags=3):
  
  tags = []
  # TODO: add confirmation of tags
  while nTags > 0:

    tag = input("HashTag: ").strip()
    # testing
    if tag == "":
      return "testing"

    tags.append(tag)

    nTags -= 1 
  
  return tags

# json db
def saveToBlogDB(data):

  pathToDB = f"{os.getcwd()}/db/blog-info.json"
  blogInfo = None

  # read and load json as dict
  with open(pathToDB, "r") as db:
    blogInfo = json.load(db)

  results = blogInfo["results"]

  articlePathHTML = data["pathToHTMLFile"]
  HTMLFileName = articlePathHTML.split("/")[-1]

  blogFound = False
  i = 0
  while i < len(results):

    if articlePathHTML == results[i]["pathToHTMLFile"]:

      # check if the HTML file exists in the /blog dir
      entirePath = f"{os.getcwd()}/public/{articlePathHTML[2:]}"

      if not os.path.exists(entirePath):
        print(f"\nFile doesn't exists! Removing it from the DB...\n")
        results.pop(i)
        break

      print("\nUpdating the blog post...\n")
      blogFound = True
      # copy the tag from previously saved data
      tags = copy.deepcopy(results[i]["tags"])
      data["tags"] = tags
      # rest everything gets updated
      results[i] = data
      break

    i += 1

  # /blog/index.html doesn't get entered into the db
  if not blogFound and HTMLFileName != "index.html":
    print("Adding article tags...")
    data["tags"] = enterTags()
    results.append(data)

  # update length
  blogInfo["length"] = len(results)
  print(f"\nNumber of posts saved in DB: {len(results)}\n")

  # clear the data and re-write everything 
  with open(pathToDB, "w") as db:
    json.dump(blogInfo, db)

  # return blogInfo


# print(saveToBlogDB({
#   "articleName": "test",
#   "articlePath": "./blog/posts/test.html"
# }))

# !Important: Only for testing, clearing the blog_info.json
def clearResults():
  with open(f"{os.getcwd()}/db/blog_info.json", "w") as db:
    json.dump({"results": []}, db)

# clearResults()

# Create entire HTML string
def makeHTMLString(isBlog:bool, articleHTML:dict)->str:
  """
  Params: isBlog, articleHTML

  Returns: returns html string
  """

  print("\ncreating html string...\n")

  stylePath = "./style.css"
  javascriptPath = "./js/main.js"
  codeBlockTags = {
    "css": "<link rel=\"stylesheet\" href=\"./css/dark.min.css\">",
    "js": "<script src=\"./js/highlight.min.js\"></script>"
  }

  if isBlog:
    stylePath = "../style.css"
    javascriptPath = "../js/main.js"
    codeBlockTags["css"] = "<link rel=\"stylesheet\" href=\"../css/dark.min.css\">"
    codeBlockTags["js"] = "<script src=\"../js/highlight.min.js\"></script>"

  html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>lostvikx | {articleHTML["blogTitle"] or "Home"}</title>
  <link rel="stylesheet" href="{stylePath}">
  <link 
    rel="icon"
    href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>💀</text></svg>"
  >
  {codeBlockTags["css"] or ""}
  {codeBlockTags["js"] or ""}
</head>
<body>

  <nav>
    <div class="nav-link">[ <a href="/">Home</a> ]</div>
    <div class="nav-link">[ <a href="/blog">Blog</a> ]</div>
    <div class="nav-link">[ <a href="/github" target="_blank" rel="noopener noreferrer">GitHub</a> ]</div>
    <div class="nav-link">[ <a href="/radio">Radio</a> ]</div>
  </nav>

  <div id="article">{articleHTML["article"]}</div>

  <hr class="footer-line" />
  
  <footer>
    <div>This website was crafted with the help of a lot of ☕ and 💪🏼</div>
    <div class="contact-links">
      <div><a href="mailto:viknegi0@gmail.com">Mail</a></div>
      <div><a href="https://github.com/lostvikx" target="_blank" rel="noopener noreferrer">GitHub</a></div>
      <div><a href="https://twitter.com/lostvikx" target="_blank" rel="noopener noreferrer">Twitter</a></div>
      <div><a href="https://linkedin.com/in/vikram-singh-negi/" target="_blank" rel="noopener noreferrer">Linkedin</a></div>
    </div>
  </footer>

  <script src="{javascriptPath}" type="module"></script>
</body>
</html>"""

  # rm article, html string, from the object
  articleHTML.pop("article", None)

  if isBlog:
    saveToBlogDB(articleHTML)

  return html

def saveHTMLFile(isBlog:bool, fileName:str)->None:
  """
  Creates an HTML file in either the ./blog or ./ directory
  """

  if isBlog:
    path = f"{os.getcwd()}/public/blog/{fileName}.html"
  else:
    path = f"{os.getcwd()}/public/{fileName}.html"

  try:
    HTMLString = makeHTMLString(isBlog, createArticle(f"{fileName}.md", isBlog))
  except:
    print("Couldn't create HTML String.")
    HTMLString = ""

  if HTMLString != "":
    with open(path, "w") as file_handle:
      file_handle.write(HTMLString)
      file_handle.close()

    print(f"Your HTML file: {path}")
  else:
    print(f"err: in writing {fileName}")

# Input md file
fileName = None
while True:

  # if blank
  fName = input("Enter md file to convert: ") or "test"

  fileCom = fName.split(".")

  # .md file
  if fileCom[-1] == "md":
    fileName = "".join(fileCom[:-1])
  else:
    fileName = fName

  # check for the .md fileName in both article and root dir
  articlePath = f"{os.getcwd()}/articles/{fileName}.md"
  rootFilePath = f"{os.getcwd()}/root_files/{fileName}.md"

  articlePathExists = os.path.exists(articlePath)
  rootFilePathExists = os.path.exists(rootFilePath)

  if articlePathExists and rootFilePathExists:
    print(f"\nfound [1]: {articlePath}")
    print(f"found [2]: {rootFilePath}\n")

    print("[1] -> blog\n[2] -> root_file")

    # Is a blog post or not
    while True:
      try:
        foundId = int(input("\nSelection: "))
        # print(foundId, type(foundId))

        if foundId == 1:
          saveHTMLFile(True, fileName)
        elif foundId == 2:
          saveHTMLFile(False, fileName)
        else:
          print("Enter a valid option!")
          continue

        break
      except:
        print("Enter a valid option!")
        continue

  elif articlePathExists:
    print(f"\nfound: {articlePath}")
    saveHTMLFile(True, fileName)
  elif rootFilePathExists:
    print(f"\nfound: {rootFilePath}")
    saveHTMLFile(False, fileName)
  else:
    print(f"Error: {fileName}.md not found!")

  if articlePathExists or rootFilePathExists:
    break
  else:
    continue

