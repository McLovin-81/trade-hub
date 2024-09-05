"use strict";
exports.__esModule = true;
var $ = require("jquery");
require("jquery-ui/ui/widgets/autocomplete");
var daxSymbols = [
    "SAP.DE", "SIE.DE", "DTE.DE", "ALV.DE", "AIR.DE", "MRK.DE", "MBG.DE", "P911.DE",
    "MUV2.DE", "SHL.DE", "BMW.DE", "VOW3.DE", "DPW.DE", "IFX.DE", "BAS.DE", "ADS.DE",
    "DB1.DE", "EOAN.DE", "HEN3.DE", "DBK.DE", "BEI.DE", "DTG.DE", "HNR1.DE", "BAYN.DE",
    "VNA.DE", "RWE.DE", "RHM.DE", "ENR.DE", "HEI.DE", "SY1.DE"
];
$(function () {
    $("#searchInput").autocomplete({
        source: daxSymbols
    });
});
