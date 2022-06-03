import React, { useState } from "react";
import { Document, Page } from "react-pdf";


/**
 * Document panel in which the document can be scrolled to prevent page from becoming very long.
 * @property {String} path - File path of the document to be shown
 * @returns AllPages component
 */
function AllPages(props) {
  const [numPages, setNumPages] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  const { pdf } = props;

  return (
    <Document // render document using react-pdf
      file={pdf}
      options={{ workerSrc: "../pdf.worker.js" }}
      onLoadSuccess={onDocumentLoadSuccess}

    >

      {Array.from(new Array(numPages), (el, index) => ( // Render pages of document
        <Page key={`page_${index + 1}`} pageNumber={index + 1} renderAnnotationLayer={false} renderTextLayer={false} />
      ))}
    </Document>
  );
}

export default AllPages;