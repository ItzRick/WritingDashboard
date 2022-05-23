import React, { useState } from "react";
import { Document, Page } from "react-pdf";


export default function AllPages(props) {
  const [numPages, setNumPages] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

function removeTextLayerOffset() {
    const textLayers = document.querySelectorAll(".react-pdf__Page__textContent");
      textLayers.forEach(layer => {
        const { style } = layer;
        style.top = "0";
        style.left = "0";
        style.transform = "";
    });
  }


  const { pdf } = props;

  return (
    <Document
      file={pdf}
      options={{ workerSrc: "../pdf.worker.js" }}
      onLoadSuccess={onDocumentLoadSuccess}

    >
      {Array.from(new Array(numPages), (el, index) => (
        <Page key={`page_${index + 1}`} pageNumber={index + 1} renderAnnotationLayer={false} renderTextLayer={false} onLoadSuccess={removeTextLayerOffset} />
      ))}
    </Document>
  );
}