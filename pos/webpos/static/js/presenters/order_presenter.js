'use strict';

function orderPresenter (hModel) {
    var hMod = hModel,
        elMain              = document.getElementsByTagName('main')[0],
        elAside             = document.getElementsByTagName('aside')[0],
        elCategoryContainer = document.getElementsByClassName('categories')[0],
        elProductsContainer = document.getElementsByClassName('products')[0],
        elNameInput         = document.getElementsByClassName('customer-name')[0],
        elPrintBtn          = document.getElementsByClassName('btn-print-bill')[0],
        elBillTable         = document.getElementsByClassName('billItems')[0],
        elBillTotal         = document.getElementsByClassName('billTotal')[0],
        sTplBillCategory    = document.getElementsByClassName('billCategoryRow')[0].innerHTML,
        sTplBillItem        = document.getElementsByClassName('billItemRow')[0].innerHTML,
        sTplBillSeparator   = document.getElementsByClassName('billSeparatorRow')[0].innerHTML;

    function addEventsListener(elNode, sTypes, fnListener) {
        var aTypes = sTypes.split(' '),
            lenTypes = aTypes.length,
            i;

        for (i = 0; i < lenTypes; i++) {
            elNode.addEventListener(aTypes[i], fnListener);
        }
    }

    /**
     * @private
     */
    function onClickBtnCategory (evt) {
        evt.preventDefault();
        if (evt.target.tagName === 'A') {
            filterCategory(evt.target);
        }
    }

    function onClickBtnProduct (evt) {
        evt.preventDefault();
        if (evt.target.tagName === 'A') {
            orderProduct(evt.target);
        }
    }

    function onClickMenu (evt) {
        evt.preventDefault();
        if (evt.target.tagName === 'A') {
            if (evt.target.classList.contains('add')) {
                incrementProduct(evt.target);
            } else if (evt.target.classList.contains('remove')) {
                decrementProduct(evt.target);
            } else if (evt.target === elPrintBtn) {
                printBill(evt.target);
            }
        }
    }

    function onWriteName (evt) {
        evt.preventDefault();
        if (evt.target.tagName === 'INPUT') {
            enablePrintButton(evt.target.value.length > 2);
        }
    }

    function enablePrintButton (bEnable) {
        if (bEnable === false) {
            elPrintBtn.classList.add('disabled');
        } else {
            elPrintBtn.classList.remove('disabled');
        }
    }

    function filterCategory (elButton) {
        var nId = parseInt(elButton.dataset.id, 10),
            aBtns = document.getElementsByClassName('products')[0].getElementsByClassName('category-' + nId);

        if (elButton.classList.contains('filtered')) {
            elButton.classList.remove('filtered');
            $.pif.forEach(aBtns, $.pif.show); 
        } else {
            elButton.classList.add('filtered');
            $.pif.forEach(aBtns, $.pif.hide); 
        }
    }

    function orderProduct (elButton) {
        var nId    = parseInt(elButton.dataset.id,       10),
            nIdCat = parseInt(elButton.dataset.category, 10);

        hMod.addProduct({
            id       : nId,
            category : nIdCat,
            name     : elButton.innerHTML,
            qty      : 1,
            price    : parseFloat(elButton.dataset.price)
        });
    }

    function incrementProduct (elButton) {
        var nId = parseInt(elButton.dataset.id, 10);

        hMod.incrementProduct({
            id  : nId,
            qty : 1
        });
    }

    function decrementProduct (elButton) {
        var nId = parseInt(elButton.dataset.id, 10);

        hMod.decrementProduct({
            id  : nId,
            qty : 1
        });
    }

    /**
     * Add the items to the right bill container.
     *
     * @param object hBill The biil data coming from the model.
     * @param object hBill.items An object containing the items as a value and their id as a key.
     * @param number hBill.total The total amount of the whole bill.
     */
    function addToBill (hBill) {
        elBillTable.innerHTML = '';
        var sHTMLRow,
            hCat = hModel.getCategories(), 
            i,
            hItem,
            elTr,
            nLastCategory,
            aOrderedBill = orderBillByCategories(hBill.items),
            billLen = aOrderedBill.length,
            elSeparator = document.createElement('tr');

        elSeparator.innerHTML =  riot.render(sTplBillSeparator);

        for (i = 0; i < billLen; i++) {
            hItem = aOrderedBill[i];
            if (nLastCategory !== hItem.category) {
                if (i > 0) {
                    elBillTable.appendChild(elSeparator.cloneNode(true));
                }
                if (hCat[hItem.category]) {
                    elTr = document.createElement('tr');
                    elTr.innerHTML = riot.render(sTplBillCategory, {
                        name : hCat[hItem.category].name
                    });
                    elBillTable.appendChild(elTr);
                }
            }

            sHTMLRow = riot.render(sTplBillItem, {
                id     : hItem.id,
                name   : hItem.name,
                amount : hItem.qty,
                price  : $.pif.formatPrice(hItem.qty * hItem.price)
            });
            elTr = document.createElement('tr');

            elTr.innerHTML = sHTMLRow;
            elBillTable.appendChild(elTr);

            nLastCategory = hItem.category
        }

        elBillTable.appendChild(elSeparator);

        // Total
        elBillTotal.innerHTML = $.pif.formatPrice(hBill.total) + ' &euro;';
    }

    /**
     * Group the bill items by category.
     *
     * @return object[] The items grouped by category.
     */
    function orderBillByCategories (hItems) {
        var aResults = [],
            nId,
            aExistCat = [],
            aCat = hModel.getCategories(),
            i;

        for (nId in hItems) {
            aResults.push(hItems[nId]);
        }
        aResults.sort(function (hItem1, hItem2) {
            if (!aCat[hItem1.category] || !aCat[hItem2.category]) {
                return 1;
            }
            var nPriority1 = aCat[hItem1.category].priority,
                nPriority2 = aCat[hItem2.category].priority,
                nReturn = 0;

            if (nPriority1 < nPriority2) {
                nReturn = -1;
            } else if (nPriority1 > nPriority2) {
                nReturn = 1;
            }

            return nReturn;
        });

        return aResults;
    }

    function printBill (elBtn) {
        if (elBtn.classList.contains('disabled') || hModel.billIsEmpty()) {
            return;
        }
        alert('BILL PRINTED');
        window.location.reload();
    }

    function disableEvent (evt) {
        evt.preventDefault();
    }

    function getCategories () {
        var hCat = {};
        $.pif.forEach(elCategoryContainer.children, function (elListItem) {
            var elButton = elListItem.getElementsByTagName('A')[0],
                nId = parseInt(elButton.dataset.id, 10);
            hCat[nId] = {
                id       : nId,
                name     : elButton.innerHTML,
                priority : parseInt(elButton.dataset.priority, 10)
            };
        });

        return hCat;
    }

    hMod.on('addToBill', addToBill);

    addEventsListener(elCategoryContainer, 'click touch', onClickBtnCategory);
    addEventsListener(elProductsContainer, 'click touch', onClickBtnProduct);
    addEventsListener(elAside,             'click touch', onClickMenu);
    addEventsListener(elNameInput,         'keyup',       onWriteName);
    addEventsListener(elMain,              'dragstart',   disableEvent);

    hMod.setCategories(getCategories());
}

orderPresenter(new OrderModel());
