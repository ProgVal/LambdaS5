eval("var x = 22;");
if (typeof(window.x) === 'undefined') {
  console.log("Passed");
}