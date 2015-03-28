'use strict';

/**
 * Create a PDF with the bill to print.
 * @class
 */
function PDFBillModel () {
    var that = riot.observable(this);

    that.createBill = function (hStore) {
        console.log(hStore);
        var hDoc = new jsPDF();
    };

    that.print = function () {
        // @TODO: Print the PDF?
    };
}