// Copyright 2009 the Sputnik authors.  All rights reserved.
// This code is governed by the BSD license found in the LICENSE file.

/**
* @name: S15.5.2.1_A1_T4;
* @section: 15.5.2.1;
* @assertion: When "String" is called as part of a new expression, it is a constructor: it initialises the newly created object and
* The [[Value]] property of the newly constructed object is set to ToString(value), or to the empty string if value is not supplied;
* @description: Create string object with "new String(1.0)"; 
*/

var __str = new String(1.0);

//////////////////////////////////////////////////////////////////////////////
//CHECK#1
if (typeof __str !== "object") {
  $ERROR('#1: __str = new String(1.0); typeof __str === "object". Actual: typeof __str ==='+typeof __str ); 
}
//
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//CHECK#1.5
if (__str.constructor !== String) {
  $ERROR('#1.5: __str = new String(1.0); __str.constructor === String. Actual: __str.constructor ==='+__str.constructor ); 
}
//
//////////////////////////////////////////////////////////////////////////////

//////////////////////////////////////////////////////////////////////////////
//CHECK#2
if (__str !=1.0+"") {
  $ERROR('#2: __str = new String(1.0); __str ==1.0+"". Actual: __str =='+__str ); 
}
//
//////////////////////////////////////////////////////////////////////////////
