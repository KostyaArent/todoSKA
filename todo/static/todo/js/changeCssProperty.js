function getCssProperty(elmId, property){
   var elem = document.getElementById(elmId);
   return window.getComputedStyle(elem,null).getPropertyValue(property);
};


function widthUpdate(elmId, propernyName, propertyValue) {
    var elem = document.getElementById(elmId);
    elem.style.setProperty(propernyName, propertyValue)
};

$(document).ready(function () {
  let contentWidth;
  if (document.getElementById("contentContainer")){
      contentWidth = getCssProperty("contentContainer", "height");
    widthUpdate("backgroundContainer", "height", contentWidth);
  } else if (document.getElementById("createDiv")) {
      contentWidth = getCssProperty("createDiv", "height");
      widthUpdate("createDivBackground", "height", contentWidth);
    };
  contentWidth = null;
});
