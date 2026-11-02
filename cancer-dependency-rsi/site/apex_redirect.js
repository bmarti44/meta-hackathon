function handler(event) {
    var req = event.request;
    var host = req.headers.host.value;
    if (host === "itsthemedium.com") {
        var parts = [];
        var qs = req.querystring || {};
        Object.keys(qs).forEach(function (k) {
            var entry = qs[k];
            if (entry.multiValue) {
                entry.multiValue.forEach(function (mv) { parts.push(k + "=" + (mv.value || "")); });
            } else {
                parts.push(k + "=" + (entry.value || ""));
            }
        });
        var suffix = parts.length ? "?" + parts.join("&") : "";
        return {
            statusCode: 301,
            statusDescription: "Moved Permanently",
            headers: { location: { value: "https://www.itsthemedium.com" + req.uri + suffix } }
        };
    }
    return req;
}
