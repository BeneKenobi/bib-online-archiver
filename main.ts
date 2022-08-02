const puppeteer = require("puppeteer");
const bibtexParse = require("bibtex-parse");

const fs = require("fs");

const file = fs.readFileSync("./sources.bib", "utf8");
const bibJSON = bibtexParse.entries(file);

initBrowserandPage().then((inited) => {
  const { browser, page } = inited;

  printAll(page, bibJSON).then((f) => {
    console.log("PDF created");
    browser.close();
  });
});

async function initBrowserandPage() {
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: {
      width: 1920,
      height: 1080,
    },
  });
  const page = await browser.newPage();
  return { browser, page };
}

async function printAll(page, bibJSON) {
  for (const entry of bibJSON) {
    if (entry.type === "online") {
      await printPDF(page, entry.URL, entry.key + ".pdf");
    }
  }
}

async function printPDF(page, url, filename) {
  await page.goto(url, { waitUntil: "networkidle0" });
  await page.pdf({
    printBackground: true,
    path: filename,
    format: "a4",
    scale: 0.5,
    landscape: true,
    margin: {
      top: "20px",
      bottom: "20px",
      left: "20px",
      right: "20px",
    },
  });
  console.log("PDF " + filename + " created");
}
