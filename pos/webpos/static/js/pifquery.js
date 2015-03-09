"use strict";

/**
 * Main PiF JavaScript utility class.
 *
 * @param object hConfig Base configurations.
 * @param object hConfig.ajax Base AJAX calls configurations.
 * @param string hConfig.ajax.url Url for the AJAX calls.
 */
function PiFQuery (hConfig) {
    var that = this;

    hConfig      = hConfig      || {};
    hConfig.ajax = hConfig.ajax || {};

    that.config = {
        ajax : {
            url     : hConfig.ajax.url,
            method  : hConfig.ajax.method || "POST",
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
    }

    /**
     * Utility to make AJAX call to server.
     *
     * @param object hParams The parameters to make the call.
     */
    that.ajaxCall = function (hParams, fnSuccess, fnFailure) {
        hParams = hParams || {};
        var hRequest = new XMLHttpRequest(),
            ajaxCfg = that.config.ajax,
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

        hRequest.onreadystatechange = function () {
            if (hRequest.readyState === 4) {
                if (hRequest.status === 200) {
                    if (fnSuccess) {
                        fnSuccess(hRequest.responseText);
                    }
                } else {
                    if (fnFailure) {
                        fnFailure(hRequest.status);
                    }
                }
            }
        }
        hRequest.ontimeout = function () {
            if (fnFailure) {
                fnFailure();
            }
        }
        hRequest.open(sMethod, sUrl, bAsync);
        hRequest.setRequestHeader("HTTP_X_REQUESTED_WITH",'XMLHttpRequest');
        hRequest.send(sCallParams);
    }

    that.formatPrice = function (nValue) {
        return that.formatNumber(nValue, 2);
    }

    that.formatNumber = function (nValue, nDecimals) {
        nDecimals = (nDecimals >= 0) ? nDecimals : 0;
        return parseFloat(nValue).toFixed(nDecimals).replace('.', ',');
    }

    that.forEach = function (mArray, fnCallback) {
        var len = mArray.length,
            i;
        for (i = 0; i < len; i++) {
            fnCallback(mArray[i]);
        }
    }

    that.hide = function (elNode) {
        elNode.style.display = 'none';
    }

    that.show = function (elNode) {
        elNode.style.display = '';
    }
}

if (!window.$) {
    window.$ = {};
}
$.pif = new PiFQuery({
    ajax : {
        url     : '',
        timeout : 30 * 1000// 30s
    }
});
