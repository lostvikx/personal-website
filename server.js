#!/usr/bin/env node

const express = require("express");
const app = express();

express.static("/", __dirname + "/public");
