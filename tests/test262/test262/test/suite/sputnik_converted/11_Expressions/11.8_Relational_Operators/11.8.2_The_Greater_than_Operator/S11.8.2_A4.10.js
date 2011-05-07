// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/**
* @name: S11.8.2_A4.10;
* @section: 11.8.2, 11.8.5;
* @assertion: If x is a prefix of y, return false;
* @description: x and y are string primitives;
*/


// Converted for Test262 from original Sputnik source

ES5Harness.registerTest( {
id: "S11.8.2_A4.10",

path: "11_Expressions\11.8_Relational_Operators\11.8.2_The_Greater_than_Operator\S11.8.2_A4.10.js",

assertion: "If x is a prefix of y, return false",

description: "x and y are string primitives",

test: function testcase() {
   //CHECK#1
if (("x" > "x") !== false) {
  $ERROR('#1: ("x" > "x") === false');
}

//CHECK#2
if (("" > "x") !== false) {
  $ERROR('#2: ("" > "x") === false');
}

//CHECK#3
if (("ab" > "abcd") !== false) {
  $ERROR('#3: ("ab" > abcd") === false');
}

//CHECK#4
if (("abcd" > "abc\u0064") !== false) {
  $ERROR('#4: ("abcd" > abc\\u0064") === false');
}

//CHECK#5
if (("x" > "x" + "y") !== false) {
  $ERROR('#5: ("x" > "x" + "y") === false');
}

//CHECK#6
var x = "x";
if ((x > x + "y") !== false) {
  $ERROR('#6: var x = "x"; (x > x + "y") === false');
}

 }
});
