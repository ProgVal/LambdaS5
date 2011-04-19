// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/**
 * @name: S7.8.3_A6.2_T1;
 * @section: 7.8.3;
 * @assertion: 0xG is incorrect;
 * @description: Checking if execution of "0xG" fails;  
 * @negative
*/


// Converted for Test262 from original Sputnik source

ES5Harness.registerTest( {
id: "S7.8.3_A6.2_T1",

path: "7.8.3",

description: "Checking if execution of \"0xG\" fails",

test: function testcase() {
  try {
     (function() {
         eval("//CHECK#1\r\n0xG\r\n") })();
   } catch (__e__) {return true  /* failure is success */};
   return false /* but success is failure */
 }
});

