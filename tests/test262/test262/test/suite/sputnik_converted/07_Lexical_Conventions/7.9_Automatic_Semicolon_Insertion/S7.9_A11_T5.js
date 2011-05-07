// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/**
 * @name: S7.9_A11_T5;
 * @section: 7.9, 12.5;
 * @assertion: Check If Statement for automatic semicolon insertion;
 * @description: Use if (false) x = 1; else x=-1 and check x;
*/


// Converted for Test262 from original Sputnik source

ES5Harness.registerTest( {
id: "S7.9_A11_T5",

path: "07_Lexical_Conventions\7.9_Automatic_Semicolon_Insertion\S7.9_A11_T5.js",

assertion: "Check If Statement for automatic semicolon insertion",

description: "Use if (false) x = 1; else x=-1 and check x",

test: function testcase() {
   //CHECK#1
x = 0;
if (false) x = 1; else x = -1
if (x !== -1) {
  $ERROR('#1: Check If Statement for automatic semicolon insertion');
}

 }
});
