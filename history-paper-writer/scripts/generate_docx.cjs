#!/usr/bin/env node

const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel, convertInchesToTwip, Footer, Header, PageNumber } = require('docx');

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { input: null, output: null };
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--input' && i + 1 < args.length) {
      result.input = args[i + 1];
      i++;
    } else if (args[i] === '--output' && i + 1 < args.length) {
      result.output = args[i + 1];
      i++;
    }
  }
  if (!result.input || !result.output) {
    console.error('Usage: node generate_docx.js --input <json> --output <docx>');
    process.exit(1);
  }
  return result;
}

function loadPaperContent(inputPath) {
  try {
    const content = fs.readFileSync(inputPath, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`Failed to load input file: ${err.message}`);
    process.exit(1);
  }
}

function createCoverPage(paper) {
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: convertInchesToTwip(2), after: convertInchesToTwip(1) },
      children: [
        new TextRun({
          text: paper.title,
          font: { name: '宋体', eastAsia: '宋体' },
          size: 52, // 1号 = 26pt = 52 half-points
          bold: true
        })
      ]
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: convertInchesToTwip(1) },
      children: [
        new TextRun({
          text: paper.author,
          font: { name: '仿宋', eastAsia: '仿宋' },
          size: 36 // 小2号 = 18pt = 36 half-points
        })
      ]
    })
  ];
}

function createAbstractCN(paper) {
  return [
    new Paragraph({
      spacing: { before: 240, after: 120 },
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5) },
      children: [
        new TextRun({
          text: '摘要:',
          font: { name: '黑体', eastAsia: '黑体' },
          size: 24, // 小4号 = 12pt = 24 half-points
          bold: true
        })
      ]
    }),
    new Paragraph({
      spacing: { line: 360, after: 120 }, // 17.9pt ≈ 360 twips
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5), firstLine: convertInchesToTwip(0.25) },
      children: [
        new TextRun({
          text: paper.abstract_cn,
          font: { name: '仿宋', eastAsia: '仿宋' },
          size: 24
        })
      ]
    }),
    new Paragraph({
      spacing: { before: 120, after: 240 },
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5) },
      children: [
        new TextRun({
          text: '关键词:',
          font: { name: '黑体', eastAsia: '黑体' },
          size: 24,
          bold: true
        }),
        new TextRun({
          text: ' ' + paper.keywords_cn.join('; '),
          font: { name: '仿宋', eastAsia: '仿宋' },
          size: 24
        })
      ]
    })
  ];
}

function createAbstractEN(paper) {
  return [
    new Paragraph({
      spacing: { before: 240, after: 120 },
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5) },
      children: [
        new TextRun({
          text: 'Abstract:',
          font: { name: 'Arial' },
          size: 24,
          bold: true
        })
      ]
    }),
    new Paragraph({
      spacing: { line: 360, after: 120 },
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5), firstLine: convertInchesToTwip(0.25) },
      children: [
        new TextRun({
          text: paper.abstract_en,
          font: { name: 'Arial' },
          size: 24
        })
      ]
    }),
    new Paragraph({
      spacing: { before: 120, after: 240 },
      indent: { left: convertInchesToTwip(0.5), right: convertInchesToTwip(0.5) },
      children: [
        new TextRun({
          text: 'Keywords:',
          font: { name: 'Arial' },
          size: 24,
          bold: true
        }),
        new TextRun({
          text: ' ' + paper.keywords_en.join('; '),
          font: { name: 'Arial' },
          size: 24
        })
      ]
    })
  ];
}

function createBodyChapters(paper) {
  const elements = [];
  let footnoteCounter = 1;
  const allFootnotes = [];

  for (const chapter of paper.chapters) {
    // Chapter title
    elements.push(
      new Paragraph({
        spacing: { before: 360, after: 240 },
        indent: { firstLine: convertInchesToTwip(0.25) },
        children: [
          new TextRun({
            text: chapter.title,
            font: { name: '宋体', eastAsia: '宋体' },
            size: 32, // 3号 = 16pt = 32 half-points
            bold: true
          })
        ]
      })
    );

    // Process chapter content - split by footnote markers (①②③ etc)
    const contentParts = [];
    let currentText = '';
    const circledNumberPattern = /[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]/g;
    const matches = [...chapter.content.matchAll(circledNumberPattern)];
    
    if (matches.length === 0) {
      // No footnotes in this chapter
      contentParts.push(new TextRun({
        text: chapter.content,
        font: { name: '宋体', eastAsia: '宋体' },
        size: 24
      }));
    } else {
      let lastIndex = 0;
      for (let i = 0; i < matches.length; i++) {
        const match = matches[i];
        const matchIndex = match.index;
        
        // Add text before footnote marker
        if (matchIndex > lastIndex) {
          contentParts.push(new TextRun({
            text: chapter.content.substring(lastIndex, matchIndex),
            font: { name: '宋体', eastAsia: '宋体' },
            size: 24
          }));
        }
        
        // Add footnote reference (use superscript for now, post-processing will handle circled numbers)
        const footnoteIndex = i < chapter.footnotes.length ? i : chapter.footnotes.length - 1;
        if (footnoteIndex >= 0 && footnoteIndex < chapter.footnotes.length) {
          const footnote = chapter.footnotes[footnoteIndex];
          allFootnotes.push(footnote);
          
          // Use placeholder text with superscript (will be post-processed to circled numbers)
          contentParts.push(new TextRun({
            text: `[${footnoteCounter}]`,
            font: { name: '宋体', eastAsia: '宋体' },
            size: 24,
            superScript: true
          }));
          footnoteCounter++;
        }
        
        lastIndex = matchIndex + 1;
      }
      
      // Add remaining text
      if (lastIndex < chapter.content.length) {
        contentParts.push(new TextRun({
          text: chapter.content.substring(lastIndex),
          font: { name: '宋体', eastAsia: '宋体' },
          size: 24
        }));
      }
    }

    // Chapter content paragraph
    elements.push(
      new Paragraph({
        spacing: { line: 360 }, // 17.9pt ≈ 360 twips
        indent: { firstLine: convertInchesToTwip(0.25) },
        children: contentParts
      })
    );
  }

  // Add footnotes section at the end of body
  if (allFootnotes.length > 0) {
    elements.push(
      new Paragraph({
        spacing: { before: 480, after: 240 },
        children: [
          new TextRun({
            text: '脚注',
            font: { name: '黑体', eastAsia: '黑体' },
            size: 28,
            bold: true
          })
        ]
      })
    );

    for (let i = 0; i < allFootnotes.length; i++) {
      const footnote = allFootnotes[i];
      elements.push(
        new Paragraph({
          spacing: { line: 290, after: 120 }, // 14.5pt ≈ 290 twips
          indent: { left: convertInchesToTwip(0.1) },
          children: [
            new TextRun({
              text: `[${i + 1}] `,
              font: { name: '楷体', eastAsia: '楷体' },
              size: 21 // 5号 = 10.5pt = 21 half-points
            }),
            new TextRun({
              text: footnote.text,
              font: { name: '楷体', eastAsia: '楷体' },
              size: 21
            })
          ]
        })
      );
    }
  }

  return elements;
}

function createReferences(paper) {
  const elements = [];
  
  elements.push(
    new Paragraph({
      spacing: { before: 480, after: 240 },
      children: [
        new TextRun({
          text: '参考文献',
          font: { name: '黑体', eastAsia: '黑体' },
          size: 28,
          bold: true
        })
      ]
    })
  );

  for (let i = 0; i < paper.references.length; i++) {
    elements.push(
      new Paragraph({
        spacing: { line: 360, after: 120 },
        indent: { left: convertInchesToTwip(0.2), hanging: convertInchesToTwip(0.2) },
        children: [
          new TextRun({
            text: `[${i + 1}] ${paper.references[i]}`,
            font: { name: '宋体', eastAsia: '宋体' },
            size: 24
          })
        ]
      })
    );
  }

  return elements;
}

async function generateDocx(inputPath, outputPath) {
  const paper = loadPaperContent(inputPath);
  
  const doc = new Document({
    sections: [
      {
        properties: {
          page: {
            margin: {
              top: convertInchesToTwip(1.3), // 3.3cm ≈ 1.3 inches
              bottom: convertInchesToTwip(1.06), // 2.7cm ≈ 1.06 inches
              left: convertInchesToTwip(0.94), // 2.4cm ≈ 0.94 inches
              right: convertInchesToTwip(0.91) // 2.3cm ≈ 0.91 inches
            }
          }
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ children: [PageNumber.CURRENT] })
                ]
              })
            ]
          })
        },
        children: [
          ...createCoverPage(paper),
          ...createAbstractCN(paper),
          ...createAbstractEN(paper),
          ...createBodyChapters(paper),
          ...createReferences(paper)
        ]
      }
    ]
  });
  
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`Generated: ${outputPath}`);
  console.log(`Document contains ${paper.chapters.length} chapters`);
  console.log(`Total references: ${paper.references.length}`);
}

if (require.main === module) {
  const args = parseArgs();
  generateDocx(args.input, args.output)
    .then(() => {
      console.log('DOCX generation completed successfully');
      process.exit(0);
    })
    .catch(err => {
      console.error(`Error generating DOCX: ${err.message}`);
      console.error(err.stack);
      process.exit(1);
    });
}

module.exports = { generateDocx };
