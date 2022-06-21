import React, { useState } from "react";
import { Document, Page } from "react-pdf";

// tracking
import { useContext, useEffect } from 'react';
import { TrackingContext } from '@vrbo/react-event-tracking';

/**
 * Document panel in which the document can be scrolled to prevent page from becoming very long.
 * @property {String} path - File path of the document to be shown
 * @returns AllPages component
 */
const AllPages = ({ pdf, docId=null, docName=null }) => {
  const [numPages, setNumPages] = useState(null);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  // context as given by the Tracking Provider
  const tc = useContext(TrackingContext);

  /**
   * 
   */
  const handleTracker = () => {
    // handle tracking when the document is viewed
    if (tc.hasProvider) {
      tc.trigger({
        eventType: 'view.document', //send eventType
        documentId: docId, //send documentId
        documentName: docName, //send documentName
      })
    }
  }

  // execute handleTracker once upon load
  useEffect( () => {
    handleTracker()
  }, []);



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