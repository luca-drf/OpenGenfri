function OrderModel () {
    var that = riot.observable(this),
        hStore = {},
        hCategories = [];

    /**
     * Add a product to the store.
     *
     * @param object hProd The product object.
     * @param number hProd.id       The product ID.
     * @param number hProd.category The category ID.
     * @param string hProd.name     The product name.
     * @param number hProd.qty      The ordered quantity.
     * @param number hProd.price    The product price.
     */
    that.addProduct = function (hProd) {
        // Insert product into the store.
        if (!hStore[hProd.id]) {
            hStore[hProd.id] = hProd;
        } else {
            hStore[hProd.id].qty += hProd.qty;
        }

        triggerAddToBill();
    }

    that.incrementProduct = function (hProd) {
        // Increment product already in the store
        if (hStore[hProd.id]) {
            hStore[hProd.id].qty += hProd.qty;
            triggerAddToBill();
        }
    }
    
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
    }

    function deleteProduct (nId) {
        delete hStore[nId];
    }

    function triggerAddToBill () {
        that.trigger('addToBill', {
            items : hStore,
            total : calculateTotal(hStore)
        });
    }

    that.setCategories = function (hCat) {
        hCategories = hCat;
    }

    that.getCategories = function () {
        return hCategories;
    }

    function calculateTotal (hStore) {
        var nId,
            nTotal = 0;

        for (nId in hStore) {
            nTotal += hStore[nId].qty * hStore[nId].price;
        }

        return nTotal < 0 ? 0 : nTotal;
    }

    that.billIsEmpty = function () {
        var nId,
            nCounter = 0;
        for (nId in hStore) {
            nCounter++;
        }
        return nCounter === 0;
    }
}
