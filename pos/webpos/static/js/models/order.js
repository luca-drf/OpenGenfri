/**
 * The model. Manage the store and the AJAX calls.
 * @class
 */
function OrderModel () {
    var that = riot.observable(this),
        /** @type {Object} The store. An object formatted as { id_item : { "category" : id_category, "id" : id_item, "name" : "item_name", "price" : item_price, "qty" : item_ordered_qty } } */
        hStore = {},
        /** @type {Object} The categories object formatted as { id_number : { "id" : number, "name" : string, "priority" : number } */
        hCategories = {};

    /**
     * Add a product to the store.
     *
     * @param {Object} hProd The product object.
     * @param {Number} hProd.id       The product ID.
     * @param {Number} hProd.category The category ID.
     * @param {String} hProd.name     The product name.
     * @param {Number} hProd.qty      The ordered quantity.
     * @param {Number} hProd.price    The product price.
     */
    that.addProduct = function (hProd) {
        // Insert product into the store.
        if (!hStore[hProd.id]) {
            hStore[hProd.id] = hProd;
        } else {
            hStore[hProd.id].qty += hProd.qty;
        }

        triggerAddToBill();
    };

    /**
     * Increment quantity of a product.
     * @param {Object} hProd     The product data.
     * @param {Number} hProd.id  The product ID.
     * @param {Number} hProd.qty The product quantity to add.
     */
    that.incrementProduct = function (hProd) {
        // Increment product already in the store
        if (hStore[hProd.id]) {
            hStore[hProd.id].qty += hProd.qty;
            triggerAddToBill();
        }
    };

    /**
     * Decrement quantity of a product.
     * @param {Object} hProd     The product data.
     * @param {Number} hProd.id  The product ID.
     * @param {Number} hProd.qty The product quantity to subtract.
     */
    that.decrementProduct = function (hProd) {
        var hStoreProd = hStore[hProd.id];

        // Decrement product already in the store. If the only delete it.
        if (hStoreProd) {
            if (hStoreProd.qty > 1) {
                hStoreProd.qty -= hProd.qty;
            } else {
                deleteProduct(hProd.id);
            }
            triggerAddToBill();
        }
    };

    /**
     * Delete a product from teh store.
     * @param {Number} nId The product ID.
     */
    function deleteProduct (nId) {
        delete hStore[nId];
    }

    /**
     * @fires OrderModel#addToBill
     */
    function triggerAddToBill () {
        /**
         * @event OrderModel#addToBill
         * @type {Object}
         * @property {Object} items The bill items.
         * @property {Number} total The bill total amount.
         */
        that.trigger('addToBill', {
            items : hStore,
            total : calculateTotal(hStore)
        });
    }

    that.setCategories = function (hCat) {
        hCategories = hCat;
    };

    that.getCategories = function () {
        return hCategories;
    };

    /**
     * Retrieve the total amount.
     * @returns {Number} The total amount.
     */
    that.getTotal = function () {
        return calculateTotal(hStore);
    };

    /**
     * Calculate the total amount.
     * @param {Object} hStore The store.
     * @returns {Number} The total amount.
     */
    function calculateTotal (hStore) {
        var nId,
            nTotal = 0;

        for (nId in hStore) {
            nTotal += hStore[nId].qty * hStore[nId].price;
        }

        return nTotal < 0 ? 0 : nTotal;
    }

    /**
     * Check if the bill is empty or not.
     * @returns {Boolean}
     */
    that.billIsEmpty = function () {
        var nId,
            nCounter = 0;
        for (nId in hStore) {
            nCounter++;
        }
        return nCounter === 0;
    };

    that.getBill = function () {
        return hStore;
    };

    /**
     * Commit the bill to the server.
     * @param {String}      sCustomerName The customer name.
     * @param {AjaxSuccess} fnSuccess     The success callback.
     * @param {AjaxFailure} fnFailure     The failure callback.
     */
    that.commitBill = function (sCustomerName, fnSuccess, fnFailure) {
        var nId,
            hData = {
                customer_name : sCustomerName,
                items         : {}
            };

        for (nId in hStore) {
            hData.items[hStore[nId].name] = hStore[nId].qty;
        }
        $.pif.ajaxCall({
            url : '/webpos/commit/',
            params : JSON.stringify(hData)
        }, fnSuccess, fnFailure);
    }
}