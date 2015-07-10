"use strict";

/**
 * Main PiF JavaScript utility class.
 * @class
 * @param {Object}  hConfig Base configurations.
 * @param {Object}  hConfig.ajax Base AJAX calls configurations.
 * @param {String}  hConfig.ajax.url          The URL to send the request to.
 * @param {String}  hConfig.ajax.method       The HTTP method to use, such as "GET", "POST", "PUT", "DELETE", etc. Ignored for non-HTTP(S) URLs.
 * @param {Boolean} [hConfig.ajax.async=true] An optional boolean parameter indicating whether or not to perform the operation asynchronously.
 * @param {Number}  [hConfig.ajax.timeout=0]  A value of 0 (which is the default) means there is no timeout.
 */
function PiFQuery (hConfig) {
    var that = this;

    hConfig      = hConfig      || {};
    hConfig.ajax = hConfig.ajax || {};

    /**
     * The settings.
     * @type {{ajax: {url: string, method: string, async: boolean, timeout: number}}}
     */
    that.config = {
        ajax : {
            url     : hConfig.ajax.url,
            method  : hConfig.ajax.method || "GET",
            async   : (hConfig.ajax.async === undefined) ? true : hConfig.ajax.async,
            timeout : hConfig.ajax.timeout || 0
        }
    };

    that.encodeQueryData = function (mParams) {
        var aParams = [],
            mKey;

        if (typeof mParams === 'object') {
            for (mKey in mParams) {
                if (typeof mParams[mKey] === "object") {
                    mParams[mKey] = JSON.stringify(mParams[mKey]);
                }
                aParams.push(encodeURIComponent(mKey) + "=" + encodeURIComponent(mParams[mKey]));
            }
        } else {
            aParams.push(mParams);
        }

        return aParams.join("&");
    };

    /**
     * @callback AjaxSuccess
     * @param {(Object|String)} response The response. If the response is a valid JSON returns an object.
     */
    /**
     * @callback AjaxFailure
     * @param {Number} status The failure status.
     */
    /**
     * Utility to make AJAX call to server.
     *
     * @param {Object}      hParams          The parameters to make the call.
     * @param {String}      [hParams.url]    The url for the call.
     * @param {String}      [hParams.method] The method. Should be "POST" or "GET".
     * @param {AjaxSuccess} [fnSuccess]      The success callback function.
     * @param {AjaxFailure} [fnFailure]      The failure callback function.
     */
    that.ajaxCall = function (hParams, fnSuccess, fnFailure) {
        hParams = hParams || {};
        var hRequest    = new XMLHttpRequest(),
            ajaxCfg     = that.config.ajax,
            sUrl        = hParams.url    || ajaxCfg.url,
            sMethod     = hParams.method || ajaxCfg.method,
            bAsync      = hParams.async  || ajaxCfg.async,
            hCallParams = hParams.params || {},
            sCallParams = that.encodeQueryData(hCallParams),
            nTimeout    = (hParams.timeout > 0) ? hParams.timeout : ajaxCfg.timeout;
        if (!sUrl && sUrl !== '') {
            throw new Error("No URL specified for the AJAX call!");
        }

        sUrl = sUrl + ((hParams.params && sMethod === 'GET') ? '?' + sCallParams : '');

        hRequest.timeout = nTimeout;

        hRequest.onreadystatechange = function () {
            if (hRequest.readyState === 4) {
                if (hRequest.status === 200) {
                    if (fnSuccess) {
                        var mResults;
                        try {
                            mResults = JSON.parse(hRequest.responseText);
                        } catch (e) {
                            mResults = hRequest.responseText;
                        }
                        fnSuccess(mResults);
                    }
                } else {
                    if (fnFailure) {
                        fnFailure(hRequest.status);
                    }
                }
            }
        };
        hRequest.ontimeout = function () {
            if (fnFailure) {
                fnFailure();
            }
        };
        hRequest.open(sMethod, sUrl, bAsync);
        hRequest.setRequestHeader("HTTP_X_REQUESTED_WITH",'XMLHttpRequest');
        hRequest.setRequestHeader("X-CSRFToken", that.getCookie('csrftoken'));
        hRequest.send(sCallParams);
    };

    that.getCookie = function (sKey) {
        if (!sKey) {
            return null;
        }
        return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
    };

    /**
     * Format a price in the italian way (with comma and 2 decimals: 1,00).
     * @param {Number} fValue The number to format.
     * @return {String} The formatted price.
     */
    that.formatPrice = function (fValue) {
        return that.formatNumber(fValue, 2);
    };

    /**
     * Format (and round) a number in the italian way (with comma).
     * @param {Number} fValue        The number to format.
     * @param {Number} [nDecimals=0] The number of decimals.
     * @returns {String} The formatted number.
     */
    that.formatNumber = function (fValue, nDecimals) {
        nDecimals = (nDecimals >= 0) ? parseInt(nDecimals, 10) : 0;
        return parseFloat(fValue).toFixed(nDecimals).replace('.', ',');
    };

    /**
     * Execute a for cycle over an iterable object (array, collection, ...).
     * @param {(Object|Array)} mArray
     * @param {Function}       fnCallback
     */
    that.forEach = function (mArray, fnCallback) {
        if (mArray && mArray.prototype && mArray.prototype.forEach) {
            mArray.forEach(function (mElement) {
                fnCallback(mElement);
            })
        } else {
            var nLen = mArray.length,
                i;
            for (i = 0; i < nLen; i++) {
                fnCallback(mArray[i]);
            }
        }
    };

    /**
     * Hide an HTML element.
     * @param {HTMLElement} elNode
     */
    that.hide = function (elElement) {
        elElement.style.display = 'none';
        elElement.style.visibility = 'hidden';
        elElement.classList.add('hidden');
    };

    /**
     * Show an HTML element.
     * @param {HTMLElement} elNode
     */
    that.show = function (elElement) {
        //if (getComputedStyle(elElement).display === 'none') {
        //    elElement.style.display = 'block';
        //} else {
            elElement.style.display = '';
        //}
        elElement.style.visibility = 'visible';
        elElement.classList.remove('hidden');
    }
}

if (!window.$) {
    window.$ = {};
}
$.pif = new PiFQuery({
    ajax : {
        url     : '',
        timeout : 30 * 1000,// 30s,
        method  : 'POST'
    }
});
